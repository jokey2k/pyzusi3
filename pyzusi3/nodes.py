from enum import Enum
import struct
import logging
import asyncio

from pyzusi3.exceptions import DecodeValueError, EncodingValueError, MissingBytesDecodeError, MissingContentTypeError

class ContentType(Enum):
    BYTE = 0
    SHORTINT = 1
    WORD = 2
    SMALLINT = 3
    INTEGER = 4
    CARDINAL = 5
    INTEGER64BIT = 6
    SINGLE = 7
    DOUBLE = 8
    STRING = 9
    FILE = 10
    RAW = 11 # same as file but used to indicate non-decoded content


class BasicNode:
    def __init__(self, id=None, content=None, contenttype=None, children=None, parent_node=None, nodeasbool=False) -> None:
        self.id = id
        self.content = content
        self.contenttype = contenttype
        if children is not None:
            self.children = children
        else:
            self.children = []
        self.parent_node = parent_node
        self.nodeasbool = nodeasbool

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return other is not None and self.id == other.id and self.content == other.content and self.contenttype == other.contenttype and self.children == other.children and self.nodeasbool == other.nodeasbool

    def __repr__(self):
        return "<%s id=%s content=%s contenttype=%s parent_node=%s children_len=%s, nodeasbool=%s>" % (self.__class__.__name__, self.id, self.content, self.contenttype, self.parent_node, len(self.children), self.nodeasbool)

    def _encodecontent(self):
        result = b''
        if self.contenttype is None:
            raise MissingContentTypeError("No contenttype has been given to encode to")
        if self.contenttype == ContentType.BYTE:
            try:
                if not 0 <= self.content <= 255:
                    raise EncodingValueError("Content %s exceeds limits of 0-255 for a byte" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range 0-255" % str(self.content))
            result += self.content.to_bytes(1, byteorder='little')
        elif self.contenttype == ContentType.SHORTINT:
            try:
                if not -128 <= self.content <= 127:
                    raise EncodingValueError("Content %s exceeds limits of -128 to 127 for a short int" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range -128 to 127" % str(self.content))
            result += self.content.to_bytes(1, byteorder='little')
        elif self.contenttype == ContentType.WORD:
            try:
                if not 0 <= self.content <= 65535:
                    raise EncodingValueError("Content %s exceeds limits of 0-65535 for a word" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range 0-65535" % str(self.content))
            result += self.content.to_bytes(2, byteorder='little')
        elif self.contenttype == ContentType.SMALLINT:
            try:
                if not -32768 <= self.content <= 32767:
                    raise EncodingValueError("Content %s exceeds limits of -32768 to 32767 for a small int" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range -32768 to 32767" % str(self.content))
            result += self.content.to_bytes(2, byteorder='little')
        elif self.contenttype == ContentType.INTEGER:
            try:
                if not -2147483648 <= self.content <= 2147483647:
                    raise EncodingValueError("Content %s exceeds limits of -2147483648 to 2147483647 for an int" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range -2147483648 to 2147483647" % str(self.content))
            result += self.content.to_bytes(4, byteorder='little')
        elif self.contenttype == ContentType.CARDINAL:
            try:
                if not 0 <= self.content <= 4294967295:
                    raise EncodingValueError("Content %s exceeds limits of 0 to 4294967295 for a cardinal" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range 0 to 4294967295" % str(self.content))
            result += self.content.to_bytes(4, byteorder='little')
        elif self.contenttype == ContentType.INTEGER64BIT:
            try:
                if not -9223372036854775808 <= self.content <= 9223372036854775807:
                    raise EncodingValueError("Content %s exceeds limits of -9223372036854775808 to 9223372036854775807 for an int64" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range -9223372036854775808 to 9223372036854775807" % str(self.content))
            result += self.content.to_bytes(8, byteorder='little')
        elif self.contenttype == ContentType.SINGLE:
            try:
                if not -3.4E38 <= self.content <= 3.4E38:
                    raise EncodingValueError("Content %s exceeds limits of -3.4E38 to 3.4E38 for a single" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range -3.4E38 to 3.4E38" % str(self.content))
            try:
                result += struct.pack("<f", self.content)
            except OverflowError as e:
                raise EncodingValueError("Content %s cannot be encoded: %s" % str(e))
        elif self.contenttype == ContentType.DOUBLE:
            try:
                if not -1.7E308 <= self.content <= 1.7E308:
                    raise EncodingValueError("Content %s exceeds limits of -1.7E308 to 1.7E308 for a double" % str(self.content))
            except TypeError:
                raise EncodingValueError("Content %s cannot be compared for range -1.7E308 to 1.7E308" % str(self.content))
            try:
                result += struct.pack("<d", self.content)
            except OverflowError as e:
                raise EncodingValueError("Content %s cannot be encoded: %s" % str(e))
        elif self.contenttype == ContentType.STRING:
            try:
                result += self.content.encode("latin1")
            except UnicodeEncodeError:
                raise EncodingValueError("Content %s cannot be encoded: %s" % str(e))
        elif self.contenttype == ContentType.FILE or self.contenttype == ContentType.RAW:
            if not isinstance(self.content, bytes):
                raise EncodingValueError("Content is not in bytes format")
            result += self.content
        else:
            raise MissingContentTypeError("Content of type %s is unknown in the encoder. Programming bug?" % (self.contenttype))

        return result

    def encode(self):
        result = b''

        if self.children or (not self.children and self.content is None) or self.nodeasbool:
            result = (0).to_bytes(4, byteorder='little') # Node start

        if self.content is not None:
            bytecontent = self._encodecontent()
            bytecontentlength = 2 + len(bytecontent) # add 2 for the content id
            result += bytecontentlength.to_bytes(4, byteorder='little')
        if self.id is not None:
            result += self.id.to_bytes(2, byteorder='little')
        if self.content is not None:
            result += bytecontent

        if self.children or (not self.children and self.content is None) or self.nodeasbool:
            for child in self.children:
                result += child.encode()
            result += (0xffffffff).to_bytes(4, byteorder='little') # Node end
        
        return result


class DecoderState(Enum):
    RESET = 0
    CONTRENTLENGTH = 1
    NODEID = 2
    NODEIDFORCONTENT = 3
    CONTENT = 4


class StreamDecoder:
    def __init__(self) -> None:
        self.log = logging.getLogger("pyzusi3.nodes.StreamDecoder")
        self.logstream = logging.getLogger("pyzusi3.nodes.StreamDecoder.streamdata")

    def reset(self):
        self.log.info("Resetting state")
        self.state = DecoderState.RESET
        self.root_node = None
        self.current_node = None
        self.content_length = None
        self.level = 1

    def decode(self, bytecontent):
        if not isinstance(bytecontent, bytes):
            raise ValueError("Need bytes to decode, not %s" % type(bytecontent))
        self.bytecontent = iter(bytecontent)
        self.log.info("Start decoding")
        while True:
            self.reset()
            self._decode_loop()
            self.log.debug("Decoding result:")
            self.log.debug(repr(self.root_node))
            if self.root_node is None:
                break
            yield self.root_node

    def _next_content_length(self):
        if self.state == DecoderState.RESET:
            length = 4
        elif self.state == DecoderState.NODEID or self.state == DecoderState.NODEIDFORCONTENT:
            length = 2
        elif self.state == DecoderState.CONTRENTLENGTH:
            length = 4
        elif self.state == DecoderState.CONTENT:
            length = self.content_length
        else:
            raise NotImplementedError("State %s not implemented in length check" % self.state)

        return length

    def _get_bytes(self):
        data = []
        for i in range(self._next_content_length()):
            try:
                data.append(next(self.bytecontent))
            except StopIteration:
                raise MissingBytesDecodeError("Not enough bytes to get from datastream")
        return bytes(data)

    def _decode_loop(self):
        while self.level > 0:
            try:
                incoming_bytes = self._get_bytes()
            except MissingBytesDecodeError as e:
                if self.level == 1:
                    break
                else:
                    raise MissingBytesDecodeError(str(e))
            self._decode_single_pass(incoming_bytes)
            if self.state == DecoderState.CONTRENTLENGTH and self.level == 1:
                # finished decoding
                break
        if self.current_node != self.root_node and self.current_node != None:
            raise DecodeValueError("Not all nodes have been closed, data incomplete")

    def _decode_single_pass(self, incoming_bytes):
        self.log.debug("Current state: %s" % self.state)
        if self.state == DecoderState.RESET:
            if incoming_bytes != (0).to_bytes(4, byteorder='little'):
                raise DecodeValueError("Expected 4 empty bytes for root node start but got %s" % incoming_bytes)
            self.root_node = self.current_node = BasicNode()
            self.log.debug("Created new node")
            self.state = DecoderState.NODEID
            self.level += 1
            self.log.debug("New level: %s" % self.level)

        elif self.state == DecoderState.NODEID or self.state == DecoderState.NODEIDFORCONTENT:
            self.current_node.id = struct.unpack("<H", incoming_bytes)[0]
            self.log.debug("Set node id to %s" % self.current_node.id)
            if self.state == DecoderState.NODEIDFORCONTENT:
                self.state = DecoderState.CONTENT
            else:
                self.state = DecoderState.CONTRENTLENGTH
        elif self.state == DecoderState.CONTRENTLENGTH:
            if incoming_bytes == (0xffffffff).to_bytes(4, byteorder='little'):
                # marks end of nodetree
                self.log.debug("Finished current node")
                if not self.current_node.children and self.current_node.content is None:
                    self.current_node.nodeasbool = True
                self.current_node = self.current_node.parent_node
                self.state = DecoderState.CONTRENTLENGTH
                self.level -= 1
                self.log.debug("New level: %s" % self.level)
                return
            self.log.debug("Creating new child node")
            new_node = BasicNode(parent_node=self.current_node)
            self.current_node.children.append(new_node)
            self.current_node = new_node
            content_length = struct.unpack("<I", incoming_bytes)[0]
            if content_length == 0:
                # just subnodes, possibly with children themselves
                self.state = DecoderState.NODEID
                self.log.debug("No content, just setting id afterwards")
                self.level += 1
                self.log.debug("New level: %s" % self.level)
            else:
                # real content follows after id
                self.content_length = struct.unpack("<I", incoming_bytes)[0] - 2
                self.log.debug("Setting id and adding content with length %s to node" % self.content_length)
                self.state = DecoderState.NODEIDFORCONTENT
        elif self.state == DecoderState.CONTENT:
            self.current_node.content = incoming_bytes
            self.current_node.contenttype = ContentType.RAW
            self.log.debug("Got content %s" % self.current_node.content)
            self.current_node = self.current_node.parent_node
            self.state = DecoderState.CONTRENTLENGTH

class AsyncStreamDecoder(StreamDecoder):

    async def _get_bytes(self):
        length = self._next_content_length()
        self.logstream.debug("Next content length: %s" % length)
        data = b''
        while len(data) != length:
            new_data = b''
            while True:
                new_data = await self.bytecontent.readexactly(length)
                break
            if new_data == b'':
                # eof
                break
            data += new_data
        self.logstream.debug("Got data: %s" % data)
        return data

    async def decode(self, stream):
        if not isinstance(stream, asyncio.StreamReader):
            raise ValueError("Need stream to decode, not %s" % type(stream))
        self.bytecontent = stream
        self.log.info("Start decoding")
        while True:
            self.reset()
            try:
                await self._decode_loop()
            except asyncio.exceptions.IncompleteReadError as e:
                if self.level == 1:
                    break
                else:
                    raise asyncio.exceptions.IncompleteReadError(str(e))                
            self.log.debug("Decoding result:")
            self.log.debug(repr(self.root_node))
            if self.root_node is None:
                break
            yield self.root_node

    async def _decode_loop(self):
        while self.level > 0:
            incoming_bytes = await self._get_bytes()
            self.log.debug("Next decode pass")
            self._decode_single_pass(incoming_bytes)
            if self.state == DecoderState.CONTRENTLENGTH and self.level == 1:
                # finished decoding
                break
        if self.current_node != self.root_node and self.current_node != None:
            raise DecodeValueError("Not all nodes have been closed, data incomplete")
