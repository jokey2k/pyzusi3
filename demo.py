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
LOG_MSG_UPDATES = False

STOPELEMENT = StopIteration

log = logging.getLogger("ZusiDemo")
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyzusi3.node").setLevel(logging.WARNING)
logging.getLogger("pyzusi3.streamdata").setLevel(logging.WARNING)
logging.getLogger("pyzusi3.messagecoders.MessageDecoder").setLevel(logging.WARNING)


def without_null_keys(dictionary):
    cleaned_collection = {}
    for key, value in dictionary.items():
        if value is not None:
            cleaned_collection[key] = value

    return cleaned_collection


async def decode_bytes(stream_bytes):
    decoder = AsyncStreamDecoder()
    decoded_tree = decoder.decode(stream_bytes)
    nodes = []
    async for node in decoded_tree:
        messagedecoder = MessageDecoder()
        yield messagedecoder.parse(node)      


async def zusi_writer(writer, to_zusi_queue):
    while True:
        msg = await to_zusi_queue.get()
        if msg == STOPELEMENT:
            break

        log.debug("Sending msg to Zusi: %s" % str(msg))
        writer.write(encode_obj(msg).encode())
        await asyncio.sleep(0.1)


async def zusi_reader(reader, from_zusi_queue):
    msg_reader = decode_bytes(reader)

    while True:
        basemessage, submessages = await msg_reader.__anext__()
        if basemessage is not None:
            log.debug("Got basemessage from Zusi: %s" % str(basemessage))
            await from_zusi_queue.put(basemessage)
        for message in submessages:
            log.debug("Got submessage from Zusi: %s" % str(message))
            await from_zusi_queue.put(message)
        await asyncio.sleep(0.1)


async def update_local_state(local_state, update_event, from_zusi_queue):
    log.info("Awaiting new states")
    while True:
        msg = await from_zusi_queue.get()
        log.debug("Got new data for %s" % str(type(msg)))
        if msg is STOPELEMENT:
            break
        if msg is None:
            continue

        log.debug("Checking for known state")
        msgtype = type(msg)
        if msgtype not in local_state:
            log.debug("Just saving whole state, was unknown")
            local_state[msgtype] = msg
            update_event.set()
            continue

        log.debug("Checking for state increment updates")
        updated_keys = without_null_keys(msg._asdict())
        if not updated_keys:
            log.debug("None found, skipping")
            continue
        known_msg_state = local_state[msgtype]
        unchanged_keys = []
        for key in updated_keys.keys():
            if getattr(known_msg_state, key) == updated_keys[key]:
                unchanged_keys.append(key)
        for key in unchanged_keys:
            del updated_keys[key]
        if not updated_keys:
            log.debug("Just same content, skipping")
            continue

        log.debug("Updated keys: %s" % updated_keys)
        local_state[msgtype] = known_msg_state._replace(**updated_keys)
        update_event.set()

        if not LOG_MSG_UPDATES:
            continue

        # normal messages.FAHRPULT_ANZEIGEN states
        data = str(without_null_keys(local_state[msgtype]._asdict()))
        if isinstance(msg, messages.DATA_FTD):
            log.warning("Updated general train data: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_NOTBREMSSYSTEM
        elif isinstance(msg, messages.STATUS_NOTBREMSSYSTEM):
            log.warning("Updated state for emer brakes: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_SIFA
        elif isinstance(msg, messages.STATUS_SIFA):
            log.warning("Updated state for Sifa: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
        elif isinstance(msg, messages.STATUS_ZUGBEEINFLUSSUNG_GRUND):
            log.warning("Updated state for ZB basic: %s" % data)
        elif isinstance(msg, messages.STATUS_INDUSI_EINSTELLUNGEN):
            log.warning("Updated state for ZB settings: %s" % data)
        elif isinstance(msg, messages.STATUS_INDUSI_BETRIEBSDATEN):
            log.warning("Updated state for ZB state: %s" % data)
        elif isinstance(msg, messages.STATUS_ETCS_EINSTELLUNGEN):
            log.warning("Updated state for ETCS settings: %s" % data)
        elif isinstance(msg, messages.STATUS_ETCS_BETRIEBSDATEN):
            log.warning("Updated state for ETCS state: %s" % data)
        elif isinstance(msg, messages.STATUS_ZUB_EINSTELLUNGEN):
            log.warning("Updated state for ZUB settings: %s" % data)
        elif isinstance(msg, messages.STATUS_ZUB_BETRIEBSDATEN):
            log.warning("Updated state for ZUB state: %s" % data)
        elif isinstance(msg, messages.STATUS_ZBS_EINSTELLUNGEN):
            log.warning("Updated state for ZBS settings: %s" % data)
        elif isinstance(msg, messages.STATUS_ZBS_BETRIEBSDATEN):
            log.warning("Updated state for ZBS state: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_TUEREN
        elif isinstance(msg, messages.STATUS_TUEREN):
            log.warning("Updated state for doors: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_FAHRZEUG
        elif isinstance(msg, messages.STATUS_FAHRZEUG):
            log.warning("Updated state for vehicle: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGVERBAND
        elif isinstance(msg, messages.STATUS_ZUGVERBAND):
            log.warning("Updated state for train: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_WEICHEN
        elif isinstance(msg, messages.STATUS_WEICHEN):
            log.warning("Updated state for switch: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_LM_ZUSIPISPLAY
        elif isinstance(msg, messages.STATUS_LM_ZUSIDISPLAY):
            log.warning("Updated state for zusidisplay buttons: %s" % data)
        # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGFAHRDATEN
        elif isinstance(msg, messages.STATUS_ZUGFAHRDATEN):
            log.warning("Updated state for train wagon data: %s" % data)


async def zusi_user_interact(local_state, update_event, to_zusi_queue):
    wait_max = 3000
    wait_cur = 0

    zuord = messages.INPUT_TASTATURZUORDNUNG
    komm = messages.INPUT_TASTATURKOMMANDO
    aktion = messages.INPUT_TASTATURAKTION

    simulated_interactions = {
        100: messages.INPUT(
            tastatur_zuordnung=zuord.FAHRSCHALTER,
            tastatur_kommando=komm.Unbestimmt,
            tastatur_aktion=aktion.Absolut,
            tastatur_schalterposition=5,
            ),
        109: messages.INPUT(
            tastatur_zuordnung=zuord.SIFA,
            tastatur_kommando=komm.Unbestimmt,
            tastatur_aktion=aktion.Down,
            tastatur_schalterposition=0,
            ),
        110: messages.INPUT(
            tastatur_zuordnung=zuord.SIFA,
            tastatur_kommando=komm.Unbestimmt,
            tastatur_aktion=aktion.Up,
            tastatur_schalterposition=0,
            ),
        150: messages.INPUT(
            tastatur_zuordnung=zuord.FAHRSCHALTER,
            tastatur_kommando=komm.Unbestimmt,
            tastatur_aktion=aktion.Absolut,
            tastatur_schalterposition=0,
            ),
        160: messages.INPUT(
            tastatur_zuordnung=zuord.SIFA,
            tastatur_kommando=komm.Unbestimmt,
            tastatur_aktion=aktion.Down,
            tastatur_schalterposition=0,
            ),
        169: messages.INPUT(
            tastatur_zuordnung=zuord.SIFA,
            tastatur_kommando=komm.Unbestimmt,
            tastatur_aktion=aktion.Up,
            tastatur_schalterposition=0,
            )
    }

    known_states = {}
    while True:
        # do not wait here, we do that below to have ~5 mins runtime
        if update_event.is_set():
            update_event.clear()
            for message in [messages.DATA_FTD, messages.STATUS_SIFA, messages.STATUS_INDUSI_BETRIEBSDATEN]:
                current_state = local_state[message]._asdict()
                if message not in known_states:
                    known_states[message] = current_state
                    log.info("%s state: %s" % (message.__name__, without_null_keys(current_state)))
                    continue
                updates = set(current_state.items()) - set(known_states[message].items())
                if updates:
                    known_states[message] = current_state
                    log.info("%s changes: %s" % (message.__name__, updates))
        await asyncio.sleep(0.1)
        wait_cur += 1
        if wait_cur in simulated_interactions:
            msg = simulated_interactions[wait_cur]
            log.info("Sending new action %s: %s" % (msg.__class__.__name__, str(without_null_keys(msg._asdict()))))
            await to_zusi_queue.put(msg)
        if wait_cur > wait_max:
            break


async def main(ip, port):
    log.info("Connecting to Zusi3")
    tcpreader, tcpwriter = await asyncio.open_connection(
        ip, port)

    log.info("Starting reader and writer task")
    from_zusi_queue = asyncio.Queue()
    to_zusi_queue = asyncio.Queue()
    
    reader_task = asyncio.create_task(zusi_reader(tcpreader, from_zusi_queue))
    writer_task = asyncio.create_task(zusi_writer(tcpwriter, to_zusi_queue))

    log.info("Sending HELLO message")
    msg = messages.HELLO(2, messages.ClientTyp.FAHRPULT, "Schlumpfpult", "1.0")
    await to_zusi_queue.put(msg)

    log.info("Waiting for response")
    msg = await from_zusi_queue.get()
    if not (isinstance(msg, messages.ACK_HELLO) and msg.status == 0):
        log.error("Zusi did not report success for HELLO")
        return

    log.info("Request some regular status updates from Zusi")
    msg = messages.NEEDED_DATA(
        anzeigen=[
            messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT_ABSOLUT,
            messages.FAHRPULT_ANZEIGEN.STATUS_SIFA,
            messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
        ],
        bedienung=True,
        #programmdaten=[
        #    messages.PROGRAMMDATEN.ZUGDATEI,
        #    messages.PROGRAMMDATEN.ZUGNUMMER,
        #    messages.PROGRAMMDATEN.LADEPAUSE,
        #    messages.PROGRAMMDATEN.BUCHFAHRPLAN_PDF
        #]
    )
    await to_zusi_queue.put(msg)

    log.info("Awaiting status request ok")
    msg = await from_zusi_queue.get()
    if not (isinstance(msg, messages.ACK_NEEDED_DATA) and msg.status == 0):
        log.error("Zusi did not report success for NEEDED_DATA")
        return

    log.info("Creating task to update local state when Zusi reports data")
    local_state = {}
    update_event = asyncio.Event()
    update_task = asyncio.create_task(update_local_state(local_state, update_event, from_zusi_queue))

    log.info("Creating task to simulate interaction with Zusi")
    interact_task = asyncio.create_task(zusi_user_interact(local_state, update_event, to_zusi_queue))

    # wait until interact finishes, either getting the stop element or CTRL-C
    try:
        await asyncio.gather(interact_task, return_exceptions=True)
    except KeyboardInterrupt:
        pass

    # cancel all other tasks
    reader_task.cancel()
    writer_task.cancel()
    update_task.cancel()
    await asyncio.gather(reader_task, writer_task, update_task, return_exceptions=True)
    
    tcpwriter.close()

    log.info("All done")

asyncio.run(main(ZUSI_IP, ZUSI_PORT))
