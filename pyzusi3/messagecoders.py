import logging
import struct

from pyzusi3.messages import ParameterId, message_index, lowlevel_parameters, ContentType

def decode_data(data, contenttype, enumtype):
    if contenttype == ContentType.BYTE:
        result = struct.unpack("<c", data)[0]
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

    def reset(self):
        self.message_class = None
    
    def parse(self, root_node):
        self.message_class, self.message_pid = self.find_messageclass(root_node)
        self.mapped_parameters = {}
        self.lowlevel_parameter = lowlevel_parameters[self.message_class]
        self.map_parameters(root_node, ParameterId(root_node.id), 1)
        return self.message_class(**self.mapped_parameters)

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
            raise NotImplementedError("Message for index %s not yet implemented" % current_pid)
        
        return message_index[current_pid], current_pid

    def map_parameters(self, current_node, current_pid, current_level):
        if current_node.content is not None:
            mapping_parameter = [param for param in self.lowlevel_parameter if param.parameterid == current_pid]
            if not len(mapping_parameter):
                self.log.debug("Parameter %s is not known for %s, skipping" % (current_pid, self.message_class))
            if len(mapping_parameter) > 1:
                raise NotImplementedError("Parameter %s is not unique for %s, programming error!" % (current_pid, self.message_class))
            mapping_parameter = mapping_parameter[0]
            self.mapped_parameters[mapping_parameter.parametername] = decode_data(current_node.content, mapping_parameter.contenttype, mapping_parameter.enumtype)
        for child_node in current_node.children:
            params = {'id' + str(current_level + 1): child_node.id}
            child_pid = current_pid._replace(**params)
            self.map_parameters(child_node, child_pid, current_level + 1)