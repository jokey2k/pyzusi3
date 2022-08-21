import unittest

from pyzusi3.nodes import BasicNode, ContentType, StreamDecoder

class TestManualExample1(unittest.TestCase):
    def setUp(self):
        self.bytes_written = b'' + \
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
        self.command = BasicNode(id=1) # Verbindungsaufbau
        hellonode = BasicNode(id=1) # HELLO-Befehl
        self.command.children.append(hellonode)
        hellonode.children.append(BasicNode(id=1, content=2, contenttype=ContentType.WORD)) # Protokollversion
        hellonode.children.append(BasicNode(id=2, content=2, contenttype=ContentType.WORD)) # Clienttyp Fahrpult
        hellonode.children.append(BasicNode(id=3, content="Fahrpult", contenttype=ContentType.STRING)) # Clientname
        hellonode.children.append(BasicNode(id=4, content="2.0", contenttype=ContentType.STRING)) # Clientversion

    def test_encoding(self):
        self.assertEqual(self.command.encode(), self.bytes_written)

    def test_msg_decoding(self):
        decoder = StreamDecoder()
        result = decoder.decode(self.bytes_written)
        self.assertEqual(result.encode(), self.bytes_written)


class TestManualExample2(unittest.TestCase):
    def setUp(self):
        self.bytes_written = b'' + \
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

        self.command = BasicNode(id=1) # Verbindungsaufbau
        hellonode = BasicNode(id=2) # ACK_HELLO-Befehl
        self.command.children.append(hellonode)
        hellonode.children.append(BasicNode(id=1, content="3.0.1.0", contenttype=ContentType.STRING)) # Zusi Version
        hellonode.children.append(BasicNode(id=2, content="0", contenttype=ContentType.STRING)) # Verbindungsinfo
        hellonode.children.append(BasicNode(id=3, content=0, contenttype=ContentType.SHORTINT)) # Ergebnis: 0=OK
        hellonode.children.append(BasicNode(id=4, content=41390.5, contenttype=ContentType.DOUBLE)) # Fahrplananfangszeit

    def test_encoding(self):
        self.assertEqual(self.command.encode(), self.bytes_written)

    def test_msg_decoding(self):
        decoder = StreamDecoder()
        result = decoder.decode(self.bytes_written)
        self.assertEqual(result.encode(), self.bytes_written)
