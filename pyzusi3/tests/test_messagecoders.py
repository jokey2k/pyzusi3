import unittest

from pyzusi3.messagecoders import MessageDecoder, encode_obj
from pyzusi3 import messages
from pyzusi3.nodes import StreamDecoder

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
        messagedecoder = MessageDecoder()
        decoded_message = messagedecoder.parse(decoded_tree)        
        self.assertEqual(type(decoded_message), messages.HELLO)
        self.assertEqual(decoded_message.protokollversion, 2)
        self.assertEqual(decoded_message.clienttyp, messages.ClientTyp.FAHRPULT)
        self.assertEqual(decoded_message.clientname, "Fahrpult")
        self.assertEqual(decoded_message.clientversion, "2.0")

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
        messagedecoder = MessageDecoder()
        decoded_message = messagedecoder.parse(decoded_tree)        
        self.assertEqual(type(decoded_message), messages.ACK_HELLO)
        self.assertEqual(decoded_message.zusiversion, "3.0.1.0")
        self.assertEqual(decoded_message.verbindungsinfo, "0")
        self.assertEqual(decoded_message.status, b'\x00')
        self.assertEqual(decoded_message.startdatum, 41390.5)
        self.assertEqual(decoded_message.protokollversion, None)

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
            status = b'\x00',
            startdatum = 41390.5
        )
    
        result = encode_obj(ack_message).encode()
        self.assertEqual(result, bytes_written)
    