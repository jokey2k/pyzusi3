import asyncio
import logging
import os.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pyzusi3.messagecoders import MessageDecoder, encode_obj
from pyzusi3 import messages
from pyzusi3.nodes import AsyncStreamDecoder

ZUSI_IP = "127.0.0.1"
ZUSI_PORT = "1436"

log = logging.getLogger("ZusiDemo")
logging.basicConfig(level=logging.WARNING)

async def decode_bytes(stream_bytes):
    decoder = AsyncStreamDecoder()
    decoded_tree = await decoder.decode(stream_bytes)
    messagedecoder = MessageDecoder()
    decoded_messages = messagedecoder.parse(decoded_tree)  
    return decoded_messages

async def zusitalk(ip, port):
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
                                    messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_TUEREN,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_FAHRZEUG,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_ZUGVERBAND,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_WEICHEN,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_LM_ZUSIPISPLAY,
                                    messages.FAHRPULT_ANZEIGEN.STATUS_ZUGFAHRDATEN
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
                # messages.FAHRPULT_ANZEIGEN.STATUS_NOTBREMSSYSTEM
                if isinstance(submessage, messages.STATUS_NOTBREMSSYSTEM):
                    log.warning("New state for emer brakes: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_SIFA
                elif isinstance(submessage, messages.STATUS_SIFA):
                    log.warning("New state for Sifa: %s" % str(submessage))
                # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
                elif isinstance(submessage, messages.STATUS_ZUGBEEINFLUSSUNG_GRUND):
                    log.warning("New state for ZB basic: %s" % str(submessage))
                elif isinstance(submessage, messages.STATUS_INDUSI_EINSTELLUNGEN):
                    log.warning("New state for ZB settings: %s" % str(submessage))
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
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        pass
    log.info("Disconnecting")
    writer.close()

asyncio.run(zusitalk(ZUSI_IP, ZUSI_PORT))
