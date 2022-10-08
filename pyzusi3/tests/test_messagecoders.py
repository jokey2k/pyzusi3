import asyncio
import unittest

from pyzusi3.messagecoders import MessageDecoder, encode_obj
from pyzusi3 import messages
from pyzusi3.nodes import StreamDecoder, AsyncStreamDecoder

class TestMessageDecoderSimple(unittest.TestCase):
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
        self.assertEqual(submessages, [])

        expected_message = messages.HELLO(
            protokollversion=2,
            clienttyp=messages.ClientTyp.FAHRPULT,
            clientname="Fahrpult",
            clientversion="2.0"
        )
        self.assertEqual(basemessage, expected_message)

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
        self.assertEqual(submessages, [])

        expected_message = messages.ACK_HELLO(
            zusiversion = "3.0.1.0",
            verbindungsinfo = "0",
            status = 0,
            startdatum = 41390.5,
            protokollversion = None
        )
        self.assertEqual(basemessage, expected_message)


class TestMessageEncoderSimple(unittest.TestCase):
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


class TestMessageDecoderEdgeCases(unittest.TestCase):
    def test_ftd169bug(self):
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
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 2)
        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[1])        
        # should not raise any issue


class TestMessageEncoderDecoderRoundtrips(unittest.TestCase):
    def test_bool_nodes(self):
        bytes_written = b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x0a\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x01\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x0b\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x0c\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x03\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x04\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff'

        decoder = StreamDecoder()
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])
        self.assertEqual(submessages, [])

        expected_basemessage = messages.NEEDED_DATA(
            anzeigen=[messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT],
            bedienung=True,
            programmdaten=[
                messages.PROGRAMMDATEN.ZUGDATEI,
                messages.PROGRAMMDATEN.ZUGNUMMER,
                messages.PROGRAMMDATEN.LADEPAUSE,
                messages.PROGRAMMDATEN.BUCHFAHRPLAN_XML
            ]
        )
        self.assertEqual(basemessage, expected_basemessage)

        encoded_obj = encode_obj(expected_basemessage)
        result = encoded_obj.encode()
        self.assertEqual(result, bytes_written)        

    def test_single_bool_false_msg_reverse(self):
        msg = messages.NEEDED_DATA(
            anzeigen=[
                messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT,
                messages.FAHRPULT_ANZEIGEN.STATUS_SIFA,
                messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
            ],
        )

        encoded_obj = encode_obj(msg)
        encoded_bytes = encoded_obj.encode()

        decoder = StreamDecoder()
        decoded_tree = decoder.decode(encoded_bytes)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])
        self.assertEqual(submessages, [])
        self.assertEqual(basemessage, msg)

    def test_single_bool_true_msg_reverse(self):
        msg = messages.NEEDED_DATA(
            anzeigen=[
                messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT,
                messages.FAHRPULT_ANZEIGEN.STATUS_SIFA,
                messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
            ],
            bedienung=True,
        )

        encoded_obj = encode_obj(msg)
        encoded_bytes = encoded_obj.encode()

        decoder = StreamDecoder()
        decoded_tree = decoder.decode(encoded_bytes)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])
        self.assertEqual(submessages, [])
        self.assertEqual(basemessage, msg)

    def test_msg_nonunique_nodes(self):
        bytes_written = b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xab\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\xb4\xcc\x0c@' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\xa0@' + \
            b'\x06\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\xff.!G' + \
            b'\x06\x00\x00\x00' + \
            b'\x06\x00' + \
            b'\x00\xa0\x8cF' + \
            b'\x03\x00\x00\x00' + \
            b'\x07\x00' + \
            b'\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\xb4\xcc\x0c@' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\xa0@' + \
            b'\x06\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\xff.!G' + \
            b'\x06\x00\x00\x00' + \
            b'\x06\x00' + \
            b'\x00\xa0\x8cF' + \
            b'\x03\x00\x00\x00' + \
            b'\x07\x00' + \
            b'\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\n\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff'
        decoder = StreamDecoder()
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])

        expected_basemessage = messages.DATA_FTD()
        expected_submessage = messages.STATUS_ZUGFAHRDATEN(
            fahrzeuge = [
                messages.STATUS_ZUGFAHRDATEN_FAHRZEUG(
                    absperrhaehne_hll = messages.ZUGFAHRDATEN_ABSPERRHAEHNE_HLL.STANDARD,
                    bremszylinderdruck=2.1999940872192383,
                    hll_druck=5.0,
                    maximal_moegliche_zugkraft=41262.99609375,
                    maximale_dynamische_bremskraft=18000.0,
                    motordrehzahl_1=0.0,
                    motordrehzahl_2=0.0,
                    zugkraft=0.0),
                messages.STATUS_ZUGFAHRDATEN_FAHRZEUG(
                    absperrhaehne_hll = messages.ZUGFAHRDATEN_ABSPERRHAEHNE_HLL.STANDARD,
                    bremszylinderdruck=2.1999940872192383,
                    hll_druck=5.0,
                    maximal_moegliche_zugkraft=41262.99609375,
                    maximale_dynamische_bremskraft=18000.0,
                    motordrehzahl_1=0.0,
                    motordrehzahl_2=0.0,
                    zugkraft=0.0),
            ]
        )
        self.assertEqual(basemessage, expected_basemessage)
        self.assertEqual(submessages[0], expected_submessage)

        encoded_obj = encode_obj(submessages[0])
        result = encoded_obj.encode()
        self.assertEqual(result, bytes_written)

        encoded_obj = encode_obj(expected_submessage)
        result = encoded_obj.encode()
        self.assertEqual(result, bytes_written)

    def test_lzb_off(self):
        bytes_written = b"\x00\x00\x00\x00" + \
            b"\x02\x00" + \
            b"\x00\x00\x00\x00" + \
            b"\x0a\x01" + \
            b"\x00\x00\x00\x00" + \
            b"\x02\x00" + \
            b"\x00\x00\x00\x00" + \
            b"\x02\x00" + \
            b"\x03\x00\x00\x00" + \
            b"\x07\x00" + \
            b"\x00" + \
            b"\x03\x00\x00\x00" + \
            b"\x08\x00" + \
            b"\x00" + \
            b"\x03\x00\x00\x00" + \
            b"\x09\x00" + \
            b"\x01" + \
            b"\x03\x00\x00\x00" + \
            b"\x0a\x00" + \
            b"\x00" + \
            b"\xFF\xFF\xFF\xFF" + \
            b"\xFF\xFF\xFF\xFF" + \
            b"\xFF\xFF\xFF\xFF" + \
            b"\xFF\xFF\xFF\xFF"

        decoder = StreamDecoder()
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)        

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])
        self.assertEqual(submessages, [])

        expected_basemessage = messages.INPUT(
            indusi_hauptschalter=messages.SCHALTER.UNBEKANNT,
            indusi_stoerschalter=messages.SCHALTER.UNBEKANNT,
            indusi_luftabsperrhahn=messages.SCHALTER.UNBEKANNT,
            lzb_stoerschalter=messages.SCHALTER.AUS,
        )
        self.assertEqual(basemessage, expected_basemessage)

        encoded_obj = encode_obj(expected_basemessage)
        result = encoded_obj.encode()
        self.assertEqual(result, bytes_written)

    def test_multisubmessages(self):
        bytes_written = b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x0b\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x05\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Fbv' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x03\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x03\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x16\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\xa0@' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'v\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00@@' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x14\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Fahr-Bremsschalter' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x0e\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'n\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x80?' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'u\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00@\xc0' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'N\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x80?' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b't\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x80?' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x13\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Richtungsschalter' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'#\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'r\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x80?' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x0c\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Wagenlicht' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x02\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x11\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Gruppenschalter' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x10\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Schluesselbund' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b's\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x80?' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x1d\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Federspeicherbremse_Anlegen' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x1c\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Federspeicherbremse_Loesen' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x0b\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Fernlicht' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'x\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff'
        bytes_written += b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x15\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Schlusslicht_Direkt' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x10\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Fenster_Rechts' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x01\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'w\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x80?' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x18\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Trittstufenanforderung' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x11\x00\x00\x00' + \
            b'\x01\x00' + \
            b'Scheibenheizung' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x10\x00\x00\x00' + \
            b'\x01\x00' + \
            b'FstBeleuchtung' + \
            b'\x04\x00\x00\x00' + \
            b'\x03\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x04\x00' + \
            b'\x00\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x05\x00' + \
            b'\x01\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x04\x00\x00\x00' + \
            b'\x01\x00' + \
            b'\x00\x00' + \
            b'\x06\x00\x00\x00' + \
            b'\x02\x00' + \
            b'\x00\x00\x00\x00' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff'

        decoder = StreamDecoder()
        decoded_tree = decoder.decode(bytes_written)
        nodes = [node for node in decoded_tree]
        self.assertEqual(len(nodes), 1)        

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])
        pass


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
        self.assertEqual(submessages, [])

        expected_message = messages.ACK_HELLO(
            zusiversion = "3.0.1.0",
            verbindungsinfo = "0",
            status = 0,
            startdatum = 41390.5,
            protokollversion = None
        )
        self.assertEqual(basemessage, expected_message)

    async def test_message_with_empty_strings(self):
        bytes_written = b'\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x0a\x00\x00\x00\x00\x00' + \
            b'\x64\x00\x10\x00\x00\x00\x01\x00\x5a\x65\x69\x74\x2d\x5a\x65\x69' + \
            b'\x74\x2d\x53\x69\x66\x61\x03\x00\x00\x00\x02\x00\x00\x03\x00\x00' + \
            b'\x00\x03\x00\x00\x03\x00\x00\x00\x04\x00\x02\x03\x00\x00\x00\x05' + \
            b'\x00\x02\x03\x00\x00\x00\x06\x00\x02\xff\xff\xff\xff\x00\x00\x00' + \
            b'\x00\x65\x00\x13\x00\x00\x00\x01\x00\x50\x5a\x42\x39\x30\x2f\x49' + \
            b'\x36\x30\x52\x20\x2d\x20\x56\x32\x2e\x30\xff\xff\xff\xff\x00\x00' + \
            b'\x00\x00\x65\x00\x00\x00\x00\x00\x02\x00\x03\x00\x00\x00\x01\x00' + \
            b'\x04\x03\x00\x00\x00\x07\x00\x02\x03\x00\x00\x00\x08\x00\x02\x03' + \
            b'\x00\x00\x00\x0a\x00\x02\x03\x00\x00\x00\x0d\x00\x03\x13\x00\x00' + \
            b'\x00\x0e\x00\x50\x5a\x42\x39\x30\x2f\x49\x36\x30\x52\x20\x2d\x20' + \
            b'\x56\x32\x2e\x30\xff\xff\xff\xff\x00\x00\x00\x00\x03\x00\x04\x00' + \
            b'\x00\x00\x02\x00\x05\x00\x04\x00\x00\x00\x03\x00\x00\x00\x03\x00' + \
            b'\x00\x00\x05\x00\x00\x03\x00\x00\x00\x09\x00\x00\x03\x00\x00\x00' + \
            b'\x2f\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x65' + \
            b'\x00\x00\x00\x00\x00\x02\x00\x02\x00\x00\x00\x02\x00\x02\x00\x00' + \
            b'\x00\x03\x00\x03\x00\x00\x00\x0b\x00\x00\x03\x00\x00\x00\x0f\x00' + \
            b'\x00\x00\x00\x00\x00\x05\x00\x04\x00\x00\x00\x01\x00\xa0\x00\x04' + \
            b'\x00\x00\x00\x02\x00\x09\x00\x03\x00\x00\x00\x05\x00\x04\xff\xff' + \
            b'\xff\xff\x00\x00\x00\x00\x06\x00\x04\x00\x00\x00\x01\x00\xa2\x00' + \
            b'\x04\x00\x00\x00\x02\x00\x08\x00\x03\x00\x00\x00\x05\x00\x04\x03' + \
            b'\x00\x00\x00\x06\x00\x06\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00' + \
            b'\x00\x00\x03\x00\x03\x00\x00\x00\x06\x00\x00\x03\x00\x00\x00\x07' + \
            b'\x00\x00\x03\x00\x00\x00\x08\x00\x01\x03\x00\x00\x00\x0a\x00\x00' + \
            b'\x03\x00\x00\x00\x0b\x00\x00\x03\x00\x00\x00\x30\x00\x02\x03\x00' + \
            b'\x00\x00\x31\x00\x03\x03\x00\x00\x00\x32\x00\x00\x03\x00\x00\x00' + \
            b'\x33\x00\x00\x03\x00\x00\x00\x34\x00\x00\xff\xff\xff\xff\xff\xff' + \
            b'\xff\xff\x00\x00\x00\x00\x65\x00\x00\x00\x00\x00\x03\x00\x03\x00' + \
            b'\x00\x00\x0c\x00\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' + \
            b'\xff\xff\xff\xff\xff\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x0a' + \
            b'\x00\x06\x00\x00\x00\x01\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff' + \
            b'\xff\xff\xff'
        reader = asyncio.StreamReader()
        reader.feed_data(bytes_written)
        reader.feed_eof()

        decoder = AsyncStreamDecoder()
        decoded_tree = decoder.decode(reader)
        nodes = []
        async for node in decoded_tree:
            nodes.append(node)

        self.assertEqual(len(nodes), 2)

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[0])

        messagedecoder = MessageDecoder()
        basemessage, submessages = messagedecoder.parse(nodes[1])
        