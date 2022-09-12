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
        result = b''
        for decoded_tree in decoder.decode(self.bytes_written):
            result += decoded_tree.encode()
        self.assertEqual(self.bytes_written, result)

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
        result = b''
        for decoded_tree in decoder.decode(self.bytes_written):
            result += decoded_tree.encode()
        self.assertEqual(self.bytes_written, result)


class TestRealWorldStreamdata(unittest.TestCase):
    def test_zusilm_message(self):
        bytes_written = b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xa9\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x08\x00\x00\x00' + \
            b'\x01\x00' + \
            b'ZD_MTD' + \
            b'\x03\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x02' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\xe8\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\xa9\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xa9\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\n\x00\x00\x00' + \
            b'\x01\x00' + \
            b'ZD_EBuLa' + \
            b'\x03\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x02' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\xaa\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'v\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xa9\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x0c\x00\x00\x00' + \
            b'\x01\x00' + \
            b'ZD_Zugfunk' + \
            b'\x03\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x02' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\xc9\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'h\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff'
        decoder = StreamDecoder()
        result = b''
        for decoded_tree in decoder.decode(bytes_written):
            result += decoded_tree.encode()
        self.assertEqual(bytes_written, result)

    def test_zusilm2_msg(self):
        bytes_written = b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\n\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\xa9\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff'
        decoder = StreamDecoder()
        result = b''
        for decoded_tree in decoder.decode(bytes_written):
            result += decoded_tree.encode()
        self.assertEqual(bytes_written, result)
