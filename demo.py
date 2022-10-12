import asyncio
import logging
import os.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import serial
import socket
from pyzusi3.messagecoders import MessageDecoder, encode_obj
from pyzusi3 import messages
from pyzusi3.nodes import AsyncStreamDecoder

ZUSI_IP = "127.0.0.1"
ZUSI_PORT = "1436"
ZUSI2_PORT = 1436
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ZUSI_IP, ZUSI2_PORT))


states = {'lzb-stoer': 0, 'pzb-stoer': 0}



ser = serial.Serial('COM3', baudrate=115200, timeout= 1)
log = logging.getLogger("ZusiDemo")
logging.basicConfig(level=logging.INFO)
log.debug("Preparing client hello")
message = b"\x00\x00\x00\x00" # Knoten Start
message += b"\x01\x00" # ID 1 Verbindungsaufbau
message += b"\x00\x00\x00\x00" # Knoten Start
message += b"\x01\x00" # HELLO
message += b"\x04\x00\x00\x00" # 4 Byte folgen (2 byte befehlstyp 2 byte daten)
message += b"\x01\x00" # Protokollversion
message += b"\x02\x00" # 2
message += b"\x04\x00\x00\x00" # 4 Byte folgen
message += b"\x02\x00" # Clienttyp
message += b"\x02\x00" # 2 : Fahrpult
message += b"\x0a\x00\x00\x00" # 10 byte folgen
message += b"\x03\x00" # Clientversion
message += b"Fahrpult" # 2 : Fahrpult
message += b"\x07\x00\x00\x00" # 7 byte folgen
message += b"\x04\x00" # Clientversion
message += b"2.0.1" # 2 : Fahrpult
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende


log.info("Sending client hello")
sock.sendall(message)

log.info("Waiting for response")
data = b""
while True:
    data += sock.recv(1)
    if data.endswith(b"\xFF\xFF\xFF\xFF"):
        break

log.debug("Got response with length %s" % len(data))
log.debug("Preparing to send LZB empty message")
message = b"\x00\x00\x00\x00" # Knoten Start
message += b"\x02\x00" # ID 2 CLient Anwendung
message += b"\x00\x00\x00\x00" # Knoten Start
message += b"\x0a\x01" # Input Befehl
message += b"\x00\x00\x00\x00" # Knoten Start
message += b"\x02\x00" # Zugbeeinflussung einstellen x0002
message += b"\x00\x00\x00\x00" # Knoten Start
message += b"\x02\x00" # System aus der Indusi-Familie
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x07\x00" # Hauptschalter
message += b"\x00" # XXX Don't change?
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x08\x00" # Störschalter
message += b"\x00" # XXX Don't change?
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x09\x00" # LZB Störschalter
message += b"\x00" # XXX Don't change?
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x0a\x00" # Luftabsperrhahn
message += b"\x00" # XXX Don't change?
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
log.info("Sending LZB empty message")
sock.sendall(message)

log.info("Waiting for response")
data = b""
while True:
    data += sock.recv(4096)
    if data.endswith(b"\xFF\xFF\xFF\xFF"):
        break

log.debug("Got response with length %s" % len(data))


message = b"\x00\x00\x00\x00" # Knoten Start
message += b"\x02\x00" # ID 2 CLient Anwendung
message += b"\x00\x00\x00\x00" # Knoten Start
message += b"\x0a\x01" # Input Befehl
message += b"\x00\x00\x00\x00" # Knoten Start
message += b"\x04\x00" # Zugbeeinflussung einstellen x0002
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x01\x00" # hauptschalter
message += b"\x00" # XXX Don't change?
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x02\x00" # störscahlter
message += b"\x00" # XXX Don't change?
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x03\x00" # sifa_hupe
message += b"\x00" # XXX Don't change?
message += b"\x03\x00\x00\x00" # 3 byte folgen
message += b"\x04\x00" # wegmesser
message += b"\x00" # XXX Don't change?
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende
message += b"\xFF\xFF\xFF\xFF" # Knoten Ende

log.info("Sending LZB empty message")
sock.sendall(message)
log.info("Waiting for response")
data = b""
while True:
    data += sock.recv(1)
    if data.endswith(b"\xFF\xFF\xFF\xFF"):
        break


async def decode_bytes(stream_bytes):
    decoder = AsyncStreamDecoder()
    decoded_tree = await decoder.decode(stream_bytes)
    messagedecoder = MessageDecoder()
    decoded_messages = messagedecoder.parse(decoded_tree)  
    return decoded_messages

async def zusitalk(ip, port):
    definition = 0
    pzb_haupt_gesendet = 0
    pzb_stoer_gesendet = 0
    lzb_stoer_gesendet = 0
    sifa_haupt_gesendet = 0
    log.info("Connecting to Zusi3")
    reader, writer = await asyncio.open_connection(
        ip, port)

    log.info("Sending HELLO message")
    hello_msg = messages.HELLO(2, messages.ClientTyp.FAHRPULT, "Schlumpfpult", "1.0")
    log.debug(hello_msg)
    writer.write(encode_obj(hello_msg).encode())

    log.info("Waiting for response")
    basemessage, submessages = await decode_bytes(reader)
    log.debug(basemessage)
    if not (isinstance(basemessage, messages.ACK_HELLO) and basemessage.status == 0):
        log.error("Zusi did not report success for HELLO")
        return

    log.info("Request train speed and emer brake status")
    need_msg = messages.NEEDED_DATA([messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT_ABSOLUT,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_NOTBREMSSYSTEM,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_SIFA,
                                    #messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_TUEREN,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_FAHRZEUG,
                                    #messages.FAHRPULT_ANZEIGEN.STATUS_ZUGVERBAND,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_WEICHEN,
                                    #messages.FAHRPULT_ANZEIGEN.STATUS_LM_ZUSIPISPLAY,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_ZUGFAHRDATEN,
                                    0x57
                                    ])
    writer.write(encode_obj(need_msg).encode())
    basemessage, submessages = await decode_bytes(reader)
    log.debug(basemessage)
    if not (isinstance(basemessage, messages.ACK_NEEDED_DATA) and basemessage.status == 0):
        log.error("Zusi did not report success for HELLO")

    try:
        while True:
            basemessage, submessages = await decode_bytes(reader)
            # normal messages.FAHRPULT_ANZEIGEN
            if isinstance(basemessage, messages.DATA_FTD) and basemessage.geschwindigkeit_absolut is not None:
                log.warning("Got new speed info: %s" % str(basemessage.geschwindigkeit_absolut))
            for submessage in submessages:
                #print(submessage)
                # messages.FAHRPULT_ANZEIGEN.STATUS_NOTBREMSSYSTEM
                if isinstance(submessage, messages.STATUS_NOTBREMSSYSTEM):
                    log.warning("New state for emer brakes: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_SIFA
                elif isinstance(submessage, messages.STATUS_SIFA):
                    log.warning("New state for Sifa: %s" % str(submessage))
                    if submessage.hauptschalter is not None and submessage.hauptschalter == messages.SCHALTER.AUS:
                        ser.write(b"A_08_00\n")
                        ser.write(b"ende\n")
                    if submessage.hauptschalter is not None and submessage.hauptschalter == messages.SCHALTER.EIN:
                        ser.write(b"A_08_01\n")
                        ser.write(b"ende\n")


                # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
                elif isinstance(submessage, messages.STATUS_ZUGBEEINFLUSSUNG_GRUND):
                    log.warning("New state for ZB basic: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_INDUSI_EINSTELLUNGEN):
                    log.warning("New state for ZB settings: %s" % str(submessage))
                    print(submessage.indusi_stoerschalter)
                    print(submessage.hauptschalter)
                    #if submessage.indusi_stoerschalter is not None and submessage.indusi_stoerschalter == messages.SCHALTER.AUS:
                    #    ser.write(b"A_02_00\n")
                    #if submessage.indusi_stoerschalter is not None and submessage.indusi_stoerschalter == messages.SCHALTER.EIN:
                    #    ser.write(b"A_02_01\n")

                    #if submessage.hauptschalter == messages.SCHALTER.AUS:
                    #    ser.write(b"A_07_01\n")
                    #    ser.write(b"A_09_00\n")

                elif isinstance(submessage, messages.STATUS_INDUSI_BETRIEBSDATEN):
                    log.warning("New state for ZB state: %s" % str(submessage))

                elif isinstance(submessage, messages.STATUS_ETCS_EINSTELLUNGEN):
                    log.warning("New state for ETCS settings: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_ETCS_BETRIEBSDATEN):
                    log.warning("New state for ETCS state: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_ZUB_EINSTELLUNGEN):
                    log.warning("New state for ZUB settings: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_ZUB_BETRIEBSDATEN):
                    log.warning("New state for ZUB state: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_ZBS_EINSTELLUNGEN):
                    log.warning("New state for ZBS settings: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_ZBS_BETRIEBSDATEN):
                    log.warning("New state for ZBS state: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_TUEREN
                elif isinstance(submessage, messages.STATUS_TUEREN):
                    log.warning("New state for doors: %s" % str(submessage))

                    if submessage.lm_links == messages.LMZUSTAND.AUS:
                        ser.write(b"A_04_00\n")
                    if submessage.lm_links == messages.LMZUSTAND.AN:
                        ser.write(b"A_04_01\n")
                    if submessage.lm_links == messages.LMZUSTAND.BLINKEN:
                        ser.write(b"A_04_02\n")

                    if submessage.lm_rechts == messages.LMZUSTAND.AUS:
                        ser.write(b"A_05_00\n")
                    if submessage.lm_rechts == messages.LMZUSTAND.AN:
                        ser.write(b"A_05_01\n")
                    if submessage.lm_rechts == messages.LMZUSTAND.BLINKEN:
                        ser.write(b"A_05_02\n")

                    if submessage.lm_zwangsschliessen == messages.LMZUSTAND.AUS:
                        ser.write(b"A_06_00\n")
                    if submessage.lm_zwangsschliessen == messages.LMZUSTAND.AN:
                        ser.write(b"A_06_01\n")
                    if submessage.lm_zwangsschliessen == messages.LMZUSTAND.BLINKEN:
                        ser.write(b"A_06_02\n")

                # messages.FAHRPULT_ANZEIGEN.STATUS_FAHRZEUG
                elif isinstance(submessage, messages.STATUS_FAHRZEUG):
                    log.warning("New state for vehicle: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGVERBAND
                elif isinstance(submessage, messages.STATUS_ZUGVERBAND):
                    log.warning("New state for train: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_WEICHEN
                elif isinstance(submessage, messages.STATUS_WEICHEN):
                    log.warning("New state for switch: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_LM_ZUSIPISPLAY
                elif isinstance(submessage, messages.STATUS_LM_ZUSIDISPLAY):
                    log.warning("New state for zusidisplay buttons: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGFAHRDATEN
                elif isinstance(submessage, messages.STATUS_ZUGFAHRDATEN):
                    log.warning("New state for train wagon data: %s" % str(submessage))
            if basemessage.zustand_federspeicherbremse == 0:
                print("0")
                ser.write(b"A_03_00\n")
            if basemessage.zustand_federspeicherbremse == 1:
                ser.write(b"A_03_01\n")

                print("1")
            if basemessage.zustand_federspeicherbremse == 2:
                ser.write(b"A_03_02\n")
                print("2")







            if (ser.inWaiting() > 0):
                eingang = ser.readline().decode("utf8").strip()

                parts = eingang.split("_")
                name = parts[0]
                zustand = int(parts[1])
                if name in states and states[name] == zustand:
                    continue
                states[name] = zustand
            if definition == 0:
                lzb_stoer_gesendet = 0
                pzb_stoer_gesendet = 0
                pzb_haupt_gesendet = 0
                sifa_haupt_gesendet = 0
                sifa_stoer_gesendet = 0
                definition = 1

            print(states)
            # print(states_alt)
            name = "lzb-stoer"
            if name in states and states[name] == 1 and lzb_stoer_gesendet == 1:
                lzb_stoer_gesendet = 0
                print("lzbstoer1")
                ser.write(b"A_01_01\n")
                log.debug("Preparing to send LZB off message")
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # System aus der Indusi-Familie
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x07\x00"  # Hauptschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x08\x00"  # Störschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x09\x00"  # LZB Störschalter
                message += b"\x01"  # LZB ausgeschaltet
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x0a\x00"  # Luftabsperrhahn
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende

                log.info("Sending LZB off message")
                # if name in states_alt and states_alt[name] == 1:
                sock.sendall(message)
            if name in states and states[name] == 0 and lzb_stoer_gesendet == 0:
                lzb_stoer_gesendet = 1
                ser.write(b"A_01_00\n")
                log.debug("Preparing to send LZB on message")
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # System aus der Indusi-Familie
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x07\x00"  # Hauptschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x08\x00"  # Störschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x09\x00"  # LZB Störschalter
                message += b"\x02"  # LZB eingeschaltet
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x0a\x00"  # Luftabsperrhahn
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                log.info("Sending LZB onf message")
                # if name in states_alt and states_alt[name] == 0:
                sock.sendall(message)
            name = "pzb-stoer"
            if name in states and states[name] == 1 and pzb_stoer_gesendet == 1:
                pzb_stoer_gesendet = 0
                ser.write(b"A_02_01\n")
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # System aus der Indusi-Familie
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x07\x00"  # Hauptschalter
                message += b"\x02"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x08\x00"  # Störschalter
                message += b"\x01"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x09\x00"  # LZB Störschalter
                message += b"\x00"  # LZB eingeschaltet
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x0a\x00"  # Luftabsperrhahn
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            if name in states and states[name] == 0 and pzb_stoer_gesendet == 0:
                pzb_stoer_gesendet = 1
                ser.write(b"A_02_00\n")
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # System aus der Indusi-Familie
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x07\x00"  # Hauptschalter
                message += b"\x02"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x08\x00"  # Störschalter
                message += b"\x02"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x09\x00"  # LZB Störschalter
                message += b"\x00"  # LZB eingeschaltet
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x0a\x00"  # Luftabsperrhahn
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            name = "pzb-haupt"
            if name in states and states[name] == 1 and pzb_haupt_gesendet == 1:
                pzb_haupt_gesendet = 0
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # System aus der Indusi-Familie
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x07\x00"  # Hauptschalter
                message += b"\x02"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x08\x00"  # Störschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x09\x00"  # LZB Störschalter
                message += b"\x00"  # LZB eingeschaltet
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x0a\x00"  # Luftabsperrhahn
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            if name in states and states[name] == 0 and pzb_haupt_gesendet == 0:
                pzb_haupt_gesendet = 1
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # System aus der Indusi-Familie
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x07\x00"  # Hauptschalter
                message += b"\x01"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x08\x00"  # Störschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x09\x00"  # LZB Störschalter
                message += b"\x00"  # LZB eingeschaltet
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x0a\x00"  # Luftabsperrhahn
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            name = "sifa-haupt"
            if name in states and states[name] == 1 and sifa_haupt_gesendet == 1:
                sifa_haupt_gesendet = 0
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x04\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x01\x00"  # hauptschalter
                message += b"\x02"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x02\x00"  # störscahlter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x03\x00"  # sifa_hupe
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x04\x00"  # wegmesser
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            if name in states and states[name] == 0 and sifa_haupt_gesendet == 0:
                sifa_haupt_gesendet = 1
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x04\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x01\x00"  # hauptschalter
                message += b"\x01"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x02\x00"  # störscahlter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x03\x00"  # sifa_hupe
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x04\x00"  # wegmesser
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            name = "sifa-stoer"
            if name in states and states[name] == 1 and sifa_stoer_gesendet == 1:
                sifa_stoer_gesendet = 0
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x04\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x01\x00"  # hauptschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x02\x00"  # störscahlter
                message += b"\x02"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x03\x00"  # sifa_hupe
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x04\x00"  # wegmesser
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)
            if name in states and states[name] == 0 and sifa_stoer_gesendet == 0:
                sifa_stoer_gesendet = 1
                message = b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x02\x00"  # ID 2 CLient Anwendung
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x0a\x01"  # Input Befehl
                message += b"\x00\x00\x00\x00"  # Knoten Start
                message += b"\x04\x00"  # Zugbeeinflussung einstellen x0002
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x01\x00"  # hauptschalter
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x02\x00"  # störscahlter
                message += b"\x01"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x03\x00"  # sifa_hupe
                message += b"\x00"  # XXX Don't change?
                message += b"\x03\x00\x00\x00"  # 3 byte folgen
                message += b"\x04\x00"  # wegmesser
                message += b"\x00"  # XXX Don't change?
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                message += b"\xFF\xFF\xFF\xFF"  # Knoten Ende
                sock.sendall(message)








            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        pass
    log.info("Disconnecting")
    writer.close()

asyncio.run(zusitalk(ZUSI_IP, ZUSI_PORT))
