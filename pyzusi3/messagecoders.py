from collections import defaultdict
import logging
from enum import Enum
import struct
from pyzusi3.exceptions import MissingLowLevelParameterError

from pyzusi3.messages import ParameterId, message_index, lowlevel_parameters, ContentType
from pyzusi3.nodes import BasicNode

def decode_data(data, contenttype, enumtype):
    if contenttype == ContentType.BYTE:
        result = int.from_bytes(data, byteorder='little')
    elif contenttype == ContentType.SHORTINT:
        result = struct.unpack("<b", data)[0]
    elif contenttype == ContentType.WORD:
        result = struct.unpack("<H", data)[0]
    elif contenttype == ContentType.SMALLINT:
        result = struct.unpack("<h", data)[0]
    elif contenttype == ContentType.INTEGER:
        result = struct.unpack("<i", data)[0]
    elif contenttype == ContentType.CARDINAL:
        result = struct.unpack("<I", data)[0]
    elif contenttype == ContentType.INTEGER64BIT:
        result = struct.unpack("<q", data)[0]
    elif contenttype == ContentType.SINGLE:
        result = struct.unpack("<f", data)[0]
    elif contenttype == ContentType.DOUBLE:
        result = struct.unpack("<d", data)[0]
    elif contenttype == ContentType.STRING:
        result = data.decode("latin1")
    elif contenttype == ContentType.FILE or contenttype == ContentType.RAW:
        result = data
    else:
        raise NotImplementedError("Unknown content type %s given" % contenttype)

    if enumtype is not None:
        result = enumtype(result)

    return result


class MessageDecoder:
    def __init__(self) -> None:
        self.log = logging.getLogger("pyzusi3.messagecoders.MessageDecoder")
        self.reset()

    def reset(self):
        self.message_class = None
        self.submessage_prefixes = {}
        self.multimessages = defaultdict(list)
        self.current_multimessage = {}
        self.mapped_parameters = {}
    
    def parse(self, root_node):
        self.message_class, self.message_pid = self.find_messageclass(root_node)
        self.lowlevel_parameter = lowlevel_parameters[self.message_class]
        self.map_parameters(root_node, ParameterId(root_node.id), 1)

        if not self.submessage_prefixes:
            return (self.message_class(**self.mapped_parameters), [])

        used_prefixes = {prefix: msgclass for prefix, msgclass in self.submessage_prefixes.values()}
        submessages = []
        for prefix, msgclass in used_prefixes.items():
            msgclass_params = {key[key.find("::")+2:]: value for key, value in self.mapped_parameters.items() if key.startswith(prefix)}            
            multimsg_params = {key[key.find("::")+2:]: value for key, value in self.multimessages.items() if key.startswith(prefix)}
            msgclass_params.update(multimsg_params)
            submessage = msgclass(**msgclass_params)
            submessages.append(submessage)

            for msgkey in msgclass_params.keys():
                prefixed_key = prefix + msgkey
                if prefixed_key in self.multimessages:
                    del self.multimessages[prefixed_key]
                if prefixed_key in self.mapped_parameters:
                    del self.mapped_parameters[prefixed_key]

        basemessage = self.message_class(**self.mapped_parameters)
        return (basemessage, submessages)

    def find_messageclass(self, root_node):
        current_pid = ParameterId()
        current_node = root_node
        current_level = 1

        while current_level < 7:
            params = {'id' + str(current_level): current_node.id}
            current_pid = current_pid._replace(**params)
            if current_pid in message_index:
                break
            current_level += 1
            if len(current_node.children) == 0:
                # bug detector, should never happen
                break
            current_node = current_node.children[0]

        if current_pid not in message_index:
            raise NotImplementedError("Message for index %s not yet implemented" % str(current_pid))
        
        return message_index[current_pid], current_pid

    def finalize_multimessage(self):
        cls = self.current_multimessage['class']
        kwargs = self.current_multimessage['mapped_parameters']
        prefix_name = self.current_multimessage['prefix_name']
        paramname = self.current_multimessage['parent_parametername']

        message = cls(**kwargs)
        self.multimessages[prefix_name + paramname].append(message)

        self.current_multimessage['mapped_parameters'] = {}

    def map_parameters(self, current_node, current_pid, current_level):
        if current_pid == ParameterId(2, 10, 169) and current_node.content:
            # whitelist bug in FTD message
            # https://forum.zusi.de/viewtopic.php?f=55&t=18246
            return

        submessage_class = None
        mapping_parameter = [param for param in self.lowlevel_parameter if param.parameterid == current_pid]
        if len(mapping_parameter) > 1:
            raise NotImplementedError("Parameter %s is not unique for %s, programming error!" % (current_pid, self.message_class))

        if not len(mapping_parameter):
            self.log.debug("Parameter %s is not known for %s, checking for submessage" % (current_pid, self.message_class))
            for i in range(len(current_pid), 1, -1):
                check_param_index = ParameterId(*current_pid[:i])
                if check_param_index in message_index:
                    submessage_class = message_index[check_param_index]
                    self.log.debug("Found submessage of type %s" % submessage_class)
                    break
            if submessage_class is None:
                self.log.warning("Parameter %s is not known for %s and no submessage, discarding" % (current_pid, self.message_class))
                return

        if submessage_class is not None:
            prefix_name = "%s::" % submessage_class
            self.submessage_prefixes[check_param_index] = (prefix_name, submessage_class)

            mapping_parameter = [param for param in lowlevel_parameters[submessage_class] if param.parameterid == current_pid]
            if len(mapping_parameter) > 1:
                raise NotImplementedError("Parameter %s is not unique for %s, programming error!" % (current_pid, submessage_class))
            elif not len(mapping_parameter):
                raise NotImplementedError("Parameter %s is unknown for %s, programming error!" % (current_pid, submessage_class))
            mapping_parameter = mapping_parameter[0]

            if mapping_parameter.multipletimes is not None and mapping_parameter.contenttype is BasicNode:
                if self.current_multimessage:
                    self.finalize_multimessage()
                self.current_multimessage = {
                    'class': mapping_parameter.multipletimes,
                    'parent_pid': mapping_parameter.parameterid,
                    'parent_parametername': mapping_parameter.parametername,
                    'prefix_name': prefix_name,
                    'mapped_parameters': {}
                }

            if mapping_parameter.contenttype is BasicNode:
                if self.current_multimessage:
                    if not is_subparameter(self.current_multimessage['parent_pid'], mapping_parameter.parameterid):
                        self.finalize_multimessage()
                        self.current_multimessage = {}
            else:
                decoded_data = decode_data(current_node.content, mapping_parameter.contenttype, mapping_parameter.enumtype)
                if self.current_multimessage:
                    if mapping_parameter.parametername in self.current_multimessage['mapped_parameters']:
                        self.finalize_multimessage()
                    self.current_multimessage['mapped_parameters'][mapping_parameter.parametername] = decoded_data
                else:
                    mapping_parameter_name = prefix_name + mapping_parameter.parametername
                    self.mapped_parameters[mapping_parameter_name] = decoded_data
                return
        elif current_node.content:
            mapping_parameter = mapping_parameter[0]
            self.mapped_parameters[mapping_parameter.parametername] = decode_data(current_node.content, mapping_parameter.contenttype, mapping_parameter.enumtype)
        for child_node in current_node.children:
            params = {'id' + str(current_level + 1): child_node.id}
            child_pid = current_pid._replace(**params)
            self.map_parameters(child_node, child_pid, current_level + 1)
        if self.current_multimessage and current_pid == self.current_multimessage['parent_pid']:
            self.finalize_multimessage()
            self.current_multimessage = {}

def level_for_parameterid(parameterid):
    for i in range(6, 0, -1):
        if getattr(parameterid, "id" + str(i), None) is not None:
            return i
    return 0

def strip_level_from_parameterid(level, parameterid):
    new_paramid = parameterid
    for i in range(6, level-1, -1):
        nulled_id = {'id' + str(i): None}
        new_paramid = new_paramid._replace(**nulled_id)
    return new_paramid

def is_subparameter(parentparameterid, subparameterid):
    parent_level = level_for_parameterid(parentparameterid)
    stripped_subparameterid = strip_level_from_parameterid(parent_level + 1, subparameterid)
    return parentparameterid == stripped_subparameterid

def encode_obj(obj):
    if type(obj) not in lowlevel_parameters:
        raise MissingLowLevelParameterError("No known %s in low level parameter encoding list" % type(obj))

    parametertree = lowlevel_parameters[type(obj)]
    
    root_node = None
    current_node = None
    current_level = 1
    seen_treenodes = {}
    for parameter in parametertree:
        # find parent node to attach to
        parent_node = None
        for i in range(level_for_parameterid(parameter.parameterid), 0, -1):
            parent_paramid = strip_level_from_parameterid(i, parameter.parameterid)
            if parent_paramid in seen_treenodes:
                parent_node = seen_treenodes[parent_paramid]
                current_level = i
                break

        if parameter.contenttype is BasicNode:
            current_node = BasicNode(id=getattr(parameter.parameterid, 'id' + str(current_level)), parent_node=parent_node)
            if current_node.parent_node is None:
                root_node = current_node
            else:
                current_node.parent_node.children.append(current_node)
            seen_treenodes[parameter.parameterid] = current_node
            continue
        parameter_value = getattr(obj, parameter.parametername, None)
        if parameter_value is None:
            continue
        node_id = getattr(parameter.parameterid, "id" + str(current_level))
        node_content = parameter_value
        if type(node_content) == bytes and parameter.contenttype not in [ContentType.FILE, ContentType.RAW]:
            node_contenttype = ContentType.RAW
        else:
            node_contenttype = parameter.contenttype
        if isinstance(node_content, list):
           # So far only used in needed_data
           for entry in node_content:
               if isinstance(entry, Enum):
                   entry_content = entry.value
               else:
                   entry_content = entry
               new_node = BasicNode(id=node_id, content=entry_content, contenttype=node_contenttype, parent_node=current_node)
               if new_node.content is not None:
                   current_node.children.append(new_node)
        else:
            if isinstance(node_content, Enum):
                node_content = node_content.value
            new_node = BasicNode(id=node_id, content=node_content, contenttype=node_contenttype, parent_node=current_node)
            if new_node.content is not None:
                current_node.children.append(new_node)

    def optimize_tree(node):
        """Removes all empty child nodes"""

        tree_has_changed = False

        new_children = []
        for child in node.children:
            if child.children:
                tree_has_changed = optimize_tree(child) or tree_has_changed
            if child.children or child.content is not None:
               new_children.append(child)

        tree_has_changed = tree_has_changed or len(node.children) != len(new_children)
        node.children = new_children
    
        return tree_has_changed

    changed = True
    while changed:
        changed = optimize_tree(root_node)

    return root_node
