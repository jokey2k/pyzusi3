from collections import defaultdict
import logging
from enum import Enum
from operator import attrgetter
import struct
from pyzusi3.exceptions import MissingLowLevelParameterError

from pyzusi3.messages import ParameterId, message_index, lowlevel_parameters, ContentType
from pyzusi3.nodes import BasicNode

def print_nodetree(node, level=0):
    print("%s%s:%s" % (" " * level, node.id, node.content))
    for child in node.children:
        print_nodetree(child, level + 1)


def decode_data(data, contenttype, enumtype):
    if data is None:
        return

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
        self.submessages = []
        self.mapped_parameters = {}
        self.lowlevel_parameter = None
    
    def parse(self, root_node, start_level=1):
        if not self.message_class:
            self.init_msg_params(root_node)

        self.map_parameters(root_node, self.message_pid, start_level)

        return self.finalize()

    def init_msg_params(self, root_node):
        self.message_class, self.message_pid = self.find_messageclass(root_node)
        self.lowlevel_parameter = lowlevel_parameters[self.message_class]

    def finalize(self):
        basemessage = self.message_class(**self.mapped_parameters)
        return basemessage, self.submessages

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

    def map_parameters(self, current_node, current_pid, current_level):
        if current_pid == ParameterId(2, 10, 169) and current_node.content:
            # whitelist bug in FTD message
            # https://forum.zusi.de/viewtopic.php?f=55&t=18246
            return

        mapping_parameter = sorted([param for param in self.lowlevel_parameter if param.parameterid == current_pid])
        if len(mapping_parameter) > 1:
            raise NotImplementedError("Parameter %s is not unique for %s, programming error!" % (current_pid, self.message_class))
        if not len(mapping_parameter):
            self.log.debug("Parameter %s is not known for %s, checking for submessage" % (current_pid, self.message_class))
            check_param_index = None
            submessage_class = None
            for i in range(len(current_pid), 1, -1):
                check_param_index = ParameterId(*current_pid[:i])
                if check_param_index in message_index:
                    submessage_class = message_index[check_param_index]
                    if submessage_class == self.message_class:
                        submessage_class = None
                        break
                    self.log.debug("Found submessage of type %s" % submessage_class)
                    break
            if submessage_class is None:
                self.log.warning("Parameter %s is not known for %s and no submessage, discarding" % (current_pid, self.message_class))
                return

            # Handle submessage as we found a new root id for it
            submsg_decoder = MessageDecoder()
            submsg_decoder.message_class = submessage_class
            submsg_decoder.message_pid = check_param_index
            submsg_decoder.lowlevel_parameter = lowlevel_parameters[submessage_class]
            basemsg, submsgs = submsg_decoder.parse(current_node, current_level)
            self.submessages.append(basemsg)
            if submsgs:
                self.submessages.extend(submsgs)
            return

        mapping_parameter = mapping_parameter[0]
        if mapping_parameter.contenttype is BasicNode and mapping_parameter.multipletimes is not None:
            # handle multipletimes-style submessages
            multi_msg_class = mapping_parameter.multipletimes
            multi_msg_decoder = MessageDecoder()
            multi_msg_decoder.message_class = multi_msg_class
            multi_msg_decoder.message_pid = current_pid
            multi_msg_decoder.lowlevel_parameter = lowlevel_parameters[multi_msg_class]

            for child_node in current_node.children:
                sub_pid = {'id' + str(current_level + 1): child_node.id}          
                multi_msg_decoder.map_parameters(child_node, current_pid._replace(**sub_pid), current_level + 1)
            basemsg, submsgs = multi_msg_decoder.finalize()

            paramname = mapping_parameter.parametername
            if paramname not in self.mapped_parameters:
                self.mapped_parameters[paramname] = []
            self.mapped_parameters[paramname].append(basemsg)

            return
        if current_node.content:
            # Decode binary content
            decoded_content = decode_data(current_node.content, mapping_parameter.contenttype, mapping_parameter.enumtype)
            if mapping_parameter.multipletimes == True:
                if mapping_parameter.parametername not in self.mapped_parameters:
                    self.mapped_parameters[mapping_parameter.parametername] = []
                self.mapped_parameters[mapping_parameter.parametername].append(decoded_content)
            else:
                self.mapped_parameters[mapping_parameter.parametername] = decoded_content
        elif current_node.nodeasbool:
            # Tree just has an empty node but acts as True value
            if mapping_parameter.nodeasbool == True:
                self.mapped_parameters[mapping_parameter.parametername] = True
        for child_node in current_node.children:
            params = {'id' + str(current_level + 1): child_node.id}
            child_pid = current_pid._replace(**params)
            self.map_parameters(child_node, child_pid, current_level + 1)


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
    if parametertree is not None:
        parametertree = sorted(parametertree, key=attrgetter('parameterid'))

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
            if parameter.multipletimes is None or \
                (parameter.multipletimes is not None and parameter.multipletimes == type(obj)):
                if parameter.nodeasbool and getattr(obj, parameter.parametername, False) != True:
                    continue
                current_node = BasicNode(id=getattr(parameter.parameterid, 'id' + str(current_level)), parent_node=parent_node, nodeasbool=parameter.nodeasbool)
                if current_node.parent_node is None:
                    root_node = current_node
                else:
                    current_node.parent_node.children.append(current_node)
                seen_treenodes[parameter.parameterid] = current_node
                continue

            parent_tree_pid = parameter.parameterid
            for item in getattr(obj, parameter.parametername, []):
                encoded_item = encode_obj(item)
                def locate_subtree(tree, built_parameterid):
                    tree_level = level_for_parameterid(built_parameterid)
                    new_pidindex = {'id' + str(tree_level + 1): tree.id}
                    new_parameterid = built_parameterid._replace(**new_pidindex)
                    if new_parameterid == parent_tree_pid:
                        return tree
                    found_subtree = None
                    for child_tree in tree.children:
                        found_subtree = found_subtree or locate_subtree(child_tree, new_parameterid)
                        if found_subtree is not None:
                            break
                    return found_subtree

                subtree = locate_subtree(encoded_item, ParameterId())
                if subtree is None:
                    raise ValueError("Tree for parameter %s inconsistent, did not find common root" % str(item))
                subtree.parent_node = current_node
                current_node.children.append(subtree)
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
        if isinstance(node_content, list) and parameter.contenttype is not BasicNode and parameter.multipletimes is True:
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
            selected_parentnode = seen_treenodes[parent_paramid]                
            new_node = BasicNode(id=node_id, content=node_content, contenttype=node_contenttype, parent_node=selected_parentnode)
            if new_node.content is not None:
                selected_parentnode.children.append(new_node)

    def optimize_tree(node):
        """Removes all empty child nodes"""

        tree_has_changed = False

        new_children = []
        for child in node.children:
            if child.children:
                tree_has_changed = optimize_tree(child) or tree_has_changed
            if child.children or child.content is not None or child.nodeasbool:
               new_children.append(child)

        tree_has_changed = tree_has_changed or len(node.children) != len(new_children)
        node.children = new_children
    
        return tree_has_changed

    changed = True
    while changed:
        changed = optimize_tree(root_node)

    return root_node
