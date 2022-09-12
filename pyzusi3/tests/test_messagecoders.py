import asyncio
import unittest

from pyzusi3.messagecoders import MessageDecoder, encode_obj
from pyzusi3 import messages
from pyzusi3.nodes import StreamDecoder, AsyncStreamDecoder

class TestMessageDecoder(unittest.TestCase):
    def testDecodeHello(self):
        bytes_written = b'' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x02\x00' + \
            b'\x0A\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x46\x61\x68\x72\x70\x75\x6C\x74' + \
            b'\x05\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x32\x2E\x30' + \
            b'\xFF\xFF\xFF\xFF' + \
            b'\xFF\xFF\xFF\xFF'
        decoder = StreamDecoder()
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)
        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])        
        self.assertEqual(type(basemessage), messages.HELLO)
        self.assertEqual(submessages, [])
        self.assertEqual(basemessage.protokollversion, 2)
        self.assertEqual(basemessage.clienttyp, messages.ClientTyp.FAHRPULT)
        self.assertEqual(basemessage.clientname, "Fahrpult")
        self.assertEqual(basemessage.clientversion, "2.0")

    def testDecodeAckHello(self):
        bytes_written = b'' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x09\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x33\x2E\x30\x2E\x31\x2E\x30' + \
            b'\x03\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x30' + \
            b'\x03\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00' + \
            b'\x0A\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00\x00\x00\xD0\x35\xE4\x40' + \
            b'\xFF\xFF\xFF\xFF' + \
            b'\xFF\xFF\xFF\xFF'
        decoder = StreamDecoder()
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)
        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])        
        self.assertTrue(isinstance(basemessage, messages.ACK_HELLO))
        self.assertEqual(submessages, [])
        self.assertEqual(basemessage.zusiversion, "3.0.1.0")
        self.assertEqual(basemessage.verbindungsinfo, "0")
        self.assertEqual(basemessage.status, 0)
        self.assertEqual(basemessage.startdatum, 41390.5)
        self.assertEqual(basemessage.protokollversion, None)

    def test_encodeObj(self):
        bytes_written = b'' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x09\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x33\x2E\x30\x2E\x31\x2E\x30' + \
            b'\x03\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x30' + \
            b'\x03\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00' + \
            b'\x0A\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00\x00\x00\xD0\x35\xE4\x40' + \
            b'\xFF\xFF\xFF\xFF' + \
            b'\xFF\xFF\xFF\xFF'

        ack_message = messages.ACK_HELLO(
            zusiversion = "3.0.1.0",
            verbindungsinfo = "0",
            status = 0,
            startdatum = 41390.5
        )
    
        encoded_obj = encode_obj(ack_message)
        result = encoded_obj.encode()
        self.assertEqual(result, bytes_written)
    
    def test_encode_complex_msg(self):
        msg = messages.STATUS_INDUSI_EINSTELLUNGEN(indusi_stoerschalter=messages.SCHALTER.EIN)
        msg_bytes = encode_obj(msg).encode()

class TestAsyncMessageDecoder(unittest. IsolatedAsyncioTestCase):
    async def testDecodeAckHello(self):
        bytes_written = b'' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x09\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x33\x2E\x30\x2E\x31\x2E\x30' + \
            b'\x03\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x30' + \
            b'\x03\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00' + \
            b'\x0A\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00\x00\x00\xD0\x35\xE4\x40' + \
            b'\xFF\xFF\xFF\xFF' + \
            b'\xFF\xFF\xFF\xFF'
        reader = asyncio.StreamReader()
        reader.feed_data(bytes_written)
        reader.feed_eof()
        decoder = AsyncStreamDecoder()
        decoded_tree = decoder.decode(reader)
        nodes = []
        async for node in decoded_tree:
            nodes.append(node)
        self.assertEqual(len(nodes), 1)
        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])        
        self.assertTrue(isinstance(basemessage, messages.ACK_HELLO))
        self.assertEqual(submessages, [])
        self.assertEqual(basemessage.zusiversion, "3.0.1.0")
        self.assertEqual(basemessage.verbindungsinfo, "0")
        self.assertEqual(basemessage.status, 0)
        self.assertEqual(basemessage.startdatum, 41390.5)
        self.assertEqual(basemessage.protokollversion, None)
