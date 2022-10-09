import asyncio
import logging
import threading

from pyzusi3.nodes import AsyncStreamDecoder
from pyzusi3 import messages
from pyzusi3.messagecoders import MessageDecoder, encode_obj

reader_log = logging.getLogger("pyzusi3.client.reader")
writer_log = logging.getLogger("pyzusi3.client.writer")
updater_log = logging.getLogger("pyzusi3.client.updater")
client_log = logging.getLogger("pyzusi3.client")


# Debug function
LOG_MSG_UPDATES = False


def suppress_none_values(dictionary):
    """Helper to just return items from dictionary where the value is not None"""

    cleaned_collection = {}
    for key, value in dictionary.items():
        if value is not None:
            cleaned_collection[key] = value

    return cleaned_collection


class ZusiClient:
    def __init__(self, ip, port, clientname="pyZusi3 Fahrpult", clientversion="1.0"):
        self.ip = ip
        self.port = port
        self.clientname = clientname
        self.clientversion = clientversion

        self.task_registry = {}
        
        self.send_messagequeue = asyncio.Queue()
        self.receive_messagequeue = asyncio.Queue()
        self.send_messagequeue_lock = threading.Lock()

        self.local_state = {}
        self.message_update_events = {}
        self.local_state_changed = asyncio.Event()

        self.connected = False
        self.requested_status = None

    async def _decode_bytes(self, stream_bytes):
        """Generator to get decoded messages from a stream"""

        decoder = AsyncStreamDecoder()
        decoded_tree = decoder.decode(stream_bytes)
        nodes = []
        async for node in decoded_tree:
            messagedecoder = MessageDecoder()
            yield messagedecoder.parse(node)      

    async def _zusi_writer(self, write_stream):
        """Queue worker to send messages to Zusi on the stream"""

        while True:
            msg = await self.send_messagequeue.get()
            writer_log.debug("Sending msg to Zusi: %s %s" % (msg.__class__.__name__, str(suppress_none_values(msg._asdict()))))
            write_stream.write(encode_obj(msg).encode())
            await asyncio.sleep(0.1)

    async def _zusi_reader(self, reader):
        """Queue worker to process received messages from Zusi on given stream"""

        msg_reader = self._decode_bytes(reader)

        while True:
            basemessage, submessages = await msg_reader.__anext__()
            if basemessage is not None:
                reader_log.debug("Got basemessage from Zusi: %s %s" % (basemessage.__class__.__name__, str(suppress_none_values(basemessage._asdict()))))
                self.receive_messagequeue.put_nowait(basemessage)
            for message in submessages:
                reader_log.debug("Got submessage from Zusi: %s %s" % (message.__class__.__name__, str(suppress_none_values(message._asdict()))))
                self.receive_messagequeue.put_nowait(message)
            await asyncio.sleep(0.1)

    async def _update_local_state(self):
        updater_log.info("Awaiting new states")
        while True:
            msg = await self.receive_messagequeue.get()
            updater_log.debug("Got new data for %s" % str(type(msg)))
            if msg is None:
                continue

            updater_log.debug("Checking for known state")
            msgtype = type(msg)
            if msgtype not in self.local_state:
                updater_log.debug("Just saving whole state, was unknown")
                self.local_state[msgtype] = msg
                self.message_update_events[msgtype] = asyncio.Event()
                self.local_state_changed.set()
                continue

            updater_log.debug("Checking for state increment updates")
            updated_keys = suppress_none_values(msg._asdict())
            if not updated_keys:
                updater_log.debug("None found, skipping")
                continue
            known_msg_state = self.local_state[msgtype]
            unchanged_keys = []
            for key in updated_keys.keys():
                if getattr(known_msg_state, key) == updated_keys[key]:
                    unchanged_keys.append(key)
            for key in unchanged_keys:
                del updated_keys[key]
            if not updated_keys:
                updater_log.debug("Just same content, skipping")
                continue

            updater_log.debug("Updated keys: %s" % updated_keys)
            self.local_state[msgtype] = known_msg_state._replace(**updated_keys)
            self.message_update_events[msgtype].set()
            self.local_state_changed.set()

            if not LOG_MSG_UPDATES:
                continue

            # normal messages.FAHRPULT_ANZEIGEN states
            data = str(suppress_none_values(self.local_state[msgtype]._asdict()))
            if isinstance(msg, messages.DATA_FTD):
                updater_log.warning("Updated general train data: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_NOTBREMSSYSTEM
            elif isinstance(msg, messages.STATUS_NOTBREMSSYSTEM):
                updater_log.warning("Updated state for emer brakes: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_SIFA
            elif isinstance(msg, messages.STATUS_SIFA):
                updater_log.warning("Updated state for Sifa: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
            elif isinstance(msg, messages.STATUS_ZUGBEEINFLUSSUNG_GRUND):
                updater_log.warning("Updated state for ZB basic: %s" % data)
            elif isinstance(msg, messages.STATUS_INDUSI_EINSTELLUNGEN):
                updater_log.warning("Updated state for ZB settings: %s" % data)
            elif isinstance(msg, messages.STATUS_INDUSI_BETRIEBSDATEN):
                updater_log.warning("Updated state for ZB state: %s" % data)
            elif isinstance(msg, messages.STATUS_ETCS_EINSTELLUNGEN):
                updater_log.warning("Updated state for ETCS settings: %s" % data)
            elif isinstance(msg, messages.STATUS_ETCS_BETRIEBSDATEN):
                updater_log.warning("Updated state for ETCS state: %s" % data)
            elif isinstance(msg, messages.STATUS_ZUB_EINSTELLUNGEN):
                updater_log.warning("Updated state for ZUB settings: %s" % data)
            elif isinstance(msg, messages.STATUS_ZUB_BETRIEBSDATEN):
                updater_log.warning("Updated state for ZUB state: %s" % data)
            elif isinstance(msg, messages.STATUS_ZBS_EINSTELLUNGEN):
                updater_log.warning("Updated state for ZBS settings: %s" % data)
            elif isinstance(msg, messages.STATUS_ZBS_BETRIEBSDATEN):
                updater_log.warning("Updated state for ZBS state: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_TUEREN
            elif isinstance(msg, messages.STATUS_TUEREN):
                updater_log.warning("Updated state for doors: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_FAHRZEUG
            elif isinstance(msg, messages.STATUS_FAHRZEUG):
                updater_log.warning("Updated state for vehicle: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGVERBAND
            elif isinstance(msg, messages.STATUS_ZUGVERBAND):
                updater_log.warning("Updated state for train: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_WEICHEN
            elif isinstance(msg, messages.STATUS_WEICHEN):
                updater_log.warning("Updated state for switch: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_LM_ZUSIPISPLAY
            elif isinstance(msg, messages.STATUS_LM_ZUSIDISPLAY):
                updater_log.warning("Updated state for zusidisplay buttons: %s" % data)
            # messages.FAHRPULT_ANZEIGEN.STATUS_ZUGFAHRDATEN
            elif isinstance(msg, messages.STATUS_ZUGFAHRDATEN):
                updater_log.warning("Updated state for train wagon data: %s" % data)
            elif isinstance(msg, messages.DATA_PROG):
                updater_log.warning("Updated simulation data: %s" % data)
            # messages.bedienung = True
            elif isinstance(msg, messages.DATA_OPERATION):
                updater_log.warning("Updated input data: %s" % data)
            else:
                updater_log.error("Unsorted message: type: %s content: %s" % (type(msg), data))

    def request_status(self, displays=[], control=False, programdata=[]):
        self.requested_status = messages.NEEDED_DATA(
            anzeigen=displays,
            bedienung=control,
            programmdaten=programdata
        )
        if self.connected and 'updater' in self.task_registry:
            self.send_messagequeue.put_nowait(self.requested_status)

    def send_input(self, input):
        if not isinstance(input, messages.INPUT):
            raise ValueError("Input needs to be in message INPUT format")
        
        if not self.connected:
            raise ConnectionError("Not connected to Zusi")
        with self.send_messagequeue_lock:
            self.send_messagequeue.put_nowait(input)

    async def connect(self):
        client_log.info("Connecting to Zusi3")
        tcpreader, tcpwriter = await asyncio.open_connection(self.ip, self.port)
        self.connected = True

        client_log.info("Starting reader and writer task")
        reader_task = asyncio.create_task(self._zusi_reader(tcpreader))
        self.task_registry['reader'] = reader_task
        writer_task = asyncio.create_task(self._zusi_writer(tcpwriter))
        self.task_registry['writer'] = writer_task

        client_log.info("Sending HELLO message")
        msg = messages.HELLO(2, messages.ClientTyp.FAHRPULT, self.clientname, self.clientversion)
        self.send_messagequeue.put_nowait(msg)

        client_log.info("Waiting for response")
        msg = await self.receive_messagequeue.get()
        if not (isinstance(msg, messages.ACK_HELLO) and msg.status == 0):
            client_log.error("Zusi did not report success for HELLO")
            return

        client_log.info("Waiting for user status to request content")
        while self.requested_status is None:
            await asyncio.sleep(0.1)
        self.send_messagequeue.put_nowait(self.requested_status)

        client_log.info("Awaiting status response ok from Zusi")
        msg = await self.receive_messagequeue.get()
        if not (isinstance(msg, messages.ACK_NEEDED_DATA) and msg.status == 0):
            client_log.error("Zusi did not report success for NEEDED_DATA")
            return

        client_log.info("Creating task to update local state when Zusi reports data")
        update_task = asyncio.create_task(self._update_local_state())
        self.task_registry['updater'] = update_task

        # wait for communication to finish
        await asyncio.wait([reader_task])

        # cancel all other tasks and close connection
        writer_task.cancel()
        update_task.cancel()

        tcpwriter.close()
        await tcpwriter.wait_closed()

        self.connected = False

        client_log.info("Connection closed")