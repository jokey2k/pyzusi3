import asyncio
import logging
import os.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pyzusi3 import messages
from pyzusi3.client import ZusiClient, suppress_none_values
import serial_asyncio

ZUSI_IP = "127.0.0.1"
ZUSI_PORT = "1436"
COM_PORT = "COM3"
COM_RATE = 115200

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("ZusiFahrpult")
log.setLevel(logging.DEBUG)
logging.getLogger("pyzusi3.client").setLevel(logging.ERROR)
logging.getLogger("pyzusi3.messagecoders.MessageDecoder").setLevel(logging.INFO)

#
# Static message mappings
#
class ZusiFahrpultInputMsgs:
    STOER_LZB_EIN = messages.INPUT(lzb_stoerschalter=messages.SCHALTER.EIN)
    STOER_LZB_AUS = messages.INPUT(lzb_stoerschalter=messages.SCHALTER.AUS)
    STOER_PZB_EIN = messages.INPUT(indusi_stoerschalter=messages.SCHALTER.EIN)
    STOER_PZB_AUS = messages.INPUT(indusi_stoerschalter=messages.SCHALTER.AUS)
    STOER_SIFA_EIN = messages.INPUT(sifa_stoerschalter=messages.SCHALTER.EIN)
    STOER_SIFA_AUS = messages.INPUT(sifa_stoerschalter=messages.SCHALTER.AUS)
    HAUPT_PZB_EIN = messages.INPUT(indusi_hauptschalter=messages.SCHALTER.EIN)
    HAUPT_PZB_AUS = messages.INPUT(indusi_hauptschalter=messages.SCHALTER.AUS)
    HAUPT_SIFA_EIN = messages.INPUT(sifa_hauptschalter=messages.SCHALTER.EIN)
    HAUPT_SIFA_AUS = messages.INPUT(sifa_hauptschalter=messages.SCHALTER.AUS)
    RISCHA_R = messages.INPUT(messages.INPUT_TASTATURZUORDNUNG.RICHTUNGSSCHALTER, messages.INPUT_TASTATURKOMMANDO.Unbestimmt, messages.INPUT_TASTATURAKTION.Absolut, tastatur_schalterposition=0)
    RISCHA_0 = messages.INPUT(messages.INPUT_TASTATURZUORDNUNG.RICHTUNGSSCHALTER, messages.INPUT_TASTATURKOMMANDO.Unbestimmt, messages.INPUT_TASTATURAKTION.Absolut, tastatur_schalterposition=1)
    RISCHA_M = messages.INPUT(messages.INPUT_TASTATURZUORDNUNG.RICHTUNGSSCHALTER, messages.INPUT_TASTATURKOMMANDO.Unbestimmt, messages.INPUT_TASTATURAKTION.Absolut, tastatur_schalterposition=2)
    RISCHA_V = messages.INPUT(messages.INPUT_TASTATURZUORDNUNG.RICHTUNGSSCHALTER, messages.INPUT_TASTATURKOMMANDO.Unbestimmt, messages.INPUT_TASTATURAKTION.Absolut, tastatur_schalterposition=3)


class ArduinoInputMsgs:
    HAUPT_SIFA_AUS = b"sifa-haupt_00"
    HAUPT_SIFA_EIN = b"sifa-haupt_01"
    STOER_SIFA_AUS = b"sifa-stoer_00"
    STOER_SIFA_EIN = b"sifa-stoer_01"
    HAUPT_PZB_AUS = b"pzb-haupt_00"
    HAUPT_PZB_EIN = b"pzb-haupt_01"
    STOER_PZB_AUS = b"pzb-stoer_00"
    STOER_PZB_EIN = b"pzb-stoer_01"
    STOER_LZB_AUS = b"lzb-stoer_00"
    STOER_LZB_EIN = b"lzb-stoer_01"
    RISCHA_R = b"rischa_00"
    RISCHA_0 = b"rischa_01"
    RISCHA_M = b"rischa_02"
    RISCHA_V = b"rischa_03"


class ArduinoOutputMsgs:
    STOER_PZB_LM_AUS = "A_01_00"
    STOER_PZB_LM_EIN = "A_01_01"
    STOER_PZB_LM_BLINK = "A_01_02"
    STOER_LZB_LM_AUS = "A_02_00"
    STOER_LZB_LM_EIN = "A_02_01"
    STOER_LZB_LM_BLINK = "A_02_02"
    FEDERSPEICHERBREMSE_LM_AUS = "A_03_00"
    FEDERSPEICHERBREMSE_LM_EIN = "A_03_01"
    FEDERSPEICHERBREMSE_LM_BLINK = "A_03_02"
    TUER_LINKS_LM_AUS = "A_04_00"
    TUER_LINKS_LM_EIN = "A_04_01"
    TUER_LINKS_LM_BLINK = "A_04_02"
    TUER_RECHTS_LM_AUS = "A_05_00"
    TUER_RECHTS_LM_EIN = "A_05_01"
    TUER_RECHTS_LM_BLINK = "A_05_02"
    TUER_ZU_LM_AUS = "A_06_00"
    TUER_ZU_LM_EIN = "A_06_01"
    TUER_ZU_LM_BLINK = "A_06_02"
    AUSLOESEN_HAUTPSCHALTER_PZB = "A_07_01"
    FREIGEBEN_HAUTPSCHALTER_PZB = "A_07_00"
    AUSLOESEN_HAUTPSCHALTER_SIFA = "A_08_01"
    FREIGEBEN_HAUTPSCHALTER_SIFA = "A_08_00"

#
# Command message mapping
# Fahrpult -> Zusi
#
ArduinoSendQueue = asyncio.Queue()
class ArduinoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        log.info('Arduino on %s opened as %s' % (COM_PORT, transport))
        self.buffered_data = b''
        self.initial_data_received = False

    def data_received(self, data):
        log.info('got data from Arduino: %s', repr(data))

        self.initial_data_received = True

        # stop callbacks again immediately
        self.pause_reading()
        for single_byte in data:
            if single_byte != 13:
                self.buffered_data += bytes([single_byte])
            else:
                cmd = self.buffered_data.strip()
                log.info("Checking line for command: %s" % cmd)
                self.handle_received_command(cmd)
                self.buffered_data = b''

    def pause_reading(self):
        self.transport.pause_reading()

    def resume_reading(self):
        self.transport.resume_reading()

    def can_transmit(self):
        if not hasattr(self, 'initial_data_received'):
            return False

        return self.initial_data_received

    def handle_received_command(self, command):
        mapping = [
            (ArduinoInputMsgs.RISCHA_R, ZusiFahrpultInputMsgs.RISCHA_R),
            (ArduinoInputMsgs.RISCHA_0, ZusiFahrpultInputMsgs.RISCHA_0),
            (ArduinoInputMsgs.RISCHA_M, ZusiFahrpultInputMsgs.RISCHA_M),
            (ArduinoInputMsgs.RISCHA_V, ZusiFahrpultInputMsgs.RISCHA_V),
            (ArduinoInputMsgs.HAUPT_SIFA_AUS, ZusiFahrpultInputMsgs.HAUPT_SIFA_AUS),
            (ArduinoInputMsgs.HAUPT_SIFA_EIN, ZusiFahrpultInputMsgs.HAUPT_SIFA_EIN),
            (ArduinoInputMsgs.STOER_SIFA_AUS, ZusiFahrpultInputMsgs.STOER_SIFA_AUS),
            (ArduinoInputMsgs.STOER_SIFA_EIN, ZusiFahrpultInputMsgs.STOER_SIFA_EIN),
            (ArduinoInputMsgs.HAUPT_PZB_AUS, ZusiFahrpultInputMsgs.HAUPT_PZB_AUS),
            (ArduinoInputMsgs.HAUPT_PZB_EIN, ZusiFahrpultInputMsgs.HAUPT_PZB_EIN),
            (ArduinoInputMsgs.STOER_PZB_AUS, ZusiFahrpultInputMsgs.STOER_PZB_AUS),
            (ArduinoInputMsgs.STOER_PZB_EIN, ZusiFahrpultInputMsgs.STOER_PZB_EIN),
            (ArduinoInputMsgs.STOER_LZB_AUS, ZusiFahrpultInputMsgs.STOER_LZB_AUS),
            (ArduinoInputMsgs.STOER_LZB_EIN, ZusiFahrpultInputMsgs.STOER_LZB_EIN),
        ]

        for arduino_msg, zusi_msg in mapping:
            if command == arduino_msg:
                log.info("Queued command for Zusi")
                ZusiSendQueue.put_nowait(zusi_msg)
                return

        log.warning("Ignored command from Fahrpult: %s", command)
#
# Status message mapping
# Zusi -> Fahrpult
#
ZusiSendQueue = asyncio.Queue()
zusi_status_mappings = {
    messages.DATA_FTD: [
        ('zustand_federspeicherbremse', [
            (1.0, ArduinoOutputMsgs.FEDERSPEICHERBREMSE_LM_EIN),
            (0.0, ArduinoOutputMsgs.FEDERSPEICHERBREMSE_LM_AUS)
        ])
    ],
    messages.STATUS_INDUSI_EINSTELLUNGEN: [
        ('indusi_stoerschalter', [
            (messages.SCHALTER.EIN, ArduinoOutputMsgs.STOER_PZB_LM_EIN),
            (messages.SCHALTER.AUS, ArduinoOutputMsgs.STOER_PZB_LM_AUS),
        ]),
        ('hauptschalter', [
            (messages.SCHALTER.EIN, ArduinoOutputMsgs.FREIGEBEN_HAUTPSCHALTER_PZB),
            (messages.SCHALTER.AUS, ArduinoOutputMsgs.AUSLOESEN_HAUTPSCHALTER_PZB),
        ]),
        ('lzb_stoerschalter', [
            (messages.SCHALTER.EIN, ArduinoOutputMsgs.STOER_LZB_LM_EIN),
            (messages.SCHALTER.AUS, ArduinoOutputMsgs.STOER_LZB_LM_AUS),
        ])
    ],
    messages.STATUS_SIFA: [
        ('hauptschalter', [
            (messages.SCHALTER.EIN, ArduinoOutputMsgs.FREIGEBEN_HAUTPSCHALTER_SIFA),
            (messages.SCHALTER.AUS, ArduinoOutputMsgs.AUSLOESEN_HAUTPSCHALTER_SIFA),
        ]),
    ],
    messages.STATUS_TUEREN: [
        ('lm_links', [
            (messages.LMZUSTAND.AN, ArduinoOutputMsgs.TUER_LINKS_LM_EIN),
            (messages.LMZUSTAND.AUS, ArduinoOutputMsgs.TUER_LINKS_LM_AUS),
            (messages.LMZUSTAND.BLINKEN, ArduinoOutputMsgs.TUER_LINKS_LM_BLINK),
        ]),
        ('lm_rechts', [
            (messages.LMZUSTAND.AN, ArduinoOutputMsgs.TUER_RECHTS_LM_EIN),
            (messages.LMZUSTAND.AUS, ArduinoOutputMsgs.TUER_RECHTS_LM_AUS),
            (messages.LMZUSTAND.BLINKEN, ArduinoOutputMsgs.TUER_RECHTS_LM_BLINK),
        ]),
        ('lm_zwangsschliessen', [
            (messages.LMZUSTAND.AN, ArduinoOutputMsgs.TUER_ZU_LM_EIN),
            (messages.LMZUSTAND.AUS, ArduinoOutputMsgs.TUER_ZU_LM_AUS),
            (messages.LMZUSTAND.BLINKEN, ArduinoOutputMsgs.TUER_ZU_LM_BLINK),
        ]),
    ]
}
async def handle_zusi_status_updates(changed_message, changed_parameters):
    if changed_message not in zusi_status_mappings:
        return

    if changed_message == messages.STATUS_TUEREN:
        pass

    for map_parameter, possible_states in zusi_status_mappings[changed_message]:
        # base messages contain list of states, submessages keys of states
        if isinstance(changed_parameters, list):
            for changed_parameter, new_value in changed_parameters:
                if map_parameter != changed_parameter:
                    continue

                for map_value, message_to_send in possible_states:
                    if new_value == map_value:
                        log.info("Mapped parameter: %s" % map_parameter)
                        await fahrpult_senden(message_to_send)
        if isinstance(changed_parameters, dict):
            if map_parameter not in changed_parameters:
                continue

            if changed_parameters[map_parameter] is None:
                continue

            for map_value, message_to_send in possible_states:
                if changed_parameters[map_parameter] == map_value:
                    log.info("Mapped parameter: %s" % map_parameter)
                    await fahrpult_senden(message_to_send)
async def fahrpult_senden(message):
    await ArduinoSendQueue.put(message)

#
# Zusi Gateway function
#
async def zusi_fahrpult_interact(client: ZusiClient, protcol: ArduinoProtocol):
    """Simulation for some random user input to be sent to Zusi"""

    known_states = {}
    while True:
        # handle incremental updates from Zusi
        if client.local_state_changed.is_set():
            client.local_state_changed.clear()
            for message, state in client.local_state.items():
                current_state = state._asdict()
                if message not in known_states:
                    known_states[message] = current_state
                    log.info("%s state: %s" % (message.__name__, suppress_none_values(current_state)))
                    await handle_zusi_status_updates(message, current_state)
                    continue
                try:
                    updates = sorted(set(current_state.items()) - set(known_states[message].items()))
                except TypeError:
                    # Happens when submessages have lists, assume all changed if one part changed
                    if known_states[message] != current_state:
                        updates = current_state
                    else:
                        continue
                if updates:
                    known_states[message] = current_state
                    log.info("%s changed state: %s" % (message.__name__, updates))
                    await handle_zusi_status_updates(message, updates)
        # check for queued messages to zusi and send them
        while not ZusiSendQueue.empty():
            item = await ZusiSendQueue.get()
            log.info("Sending new action %s: %s" % (item.__class__.__name__, str(suppress_none_values(item._asdict()))))
            client.send_input(item)
        # check for queued serial commands and send them
        while not ArduinoSendQueue.empty():
            if not protcol.can_transmit():
                break
            item = await ArduinoSendQueue.get()
            send_data = f"{item}\n".encode("utf-8")
            log.info("Sending to Arduino: %s" % send_data)
            protcol.transport.write(send_data)
        # pass time to other tasks
        protcol.resume_reading()
        await asyncio.sleep(0.1)

#
# Event loop
#

def handle_exception(loop, context):
    """Dummy handler to log errors in demo to console"""
    msg = context.get("exception", context["message"])
    log.error(f"Caught exception: {msg}")


tasks = []
async def main(ip, port, arduino_protocol):
    client = ZusiClient(ip, port, "ArduinoZusiPult", "1.0")
    client.request_status(displays=[
            messages.FAHRPULT_ANZEIGEN.ZUSTAND_FEDERSPEICHERBREMSE,
            messages.FAHRPULT_ANZEIGEN.STATUS_SIFA,
            messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG,
            messages.FAHRPULT_ANZEIGEN.STATUS_TUEREN
        ],
        control=True,
    )

    main_task = asyncio.create_task(client.connect())
    tasks.append(main_task)

    interact_task = asyncio.create_task(zusi_fahrpult_interact(client, arduino_protocol))
    tasks.append(interact_task)

    while True:
        all_tasks_done = True
        for task in tasks:
            if task.done():
                exc = task.exception()
                if exc:
                    log.exception(exc, exc_info=exc)
                    pass
            else:
                all_tasks_done = False
        if all_tasks_done:
            break
        await asyncio.sleep(1)

if __name__ == "__main__":
    run_loop = asyncio.new_event_loop()
    run_loop.set_exception_handler(handle_exception)
    coro = serial_asyncio.create_serial_connection(run_loop, ArduinoProtocol, COM_PORT, baudrate=COM_RATE)
    transport, arduino_protocol = run_loop.run_until_complete(coro)
    run_loop.create_task(main(ZUSI_IP, ZUSI_PORT, arduino_protocol))
    run_loop.run_forever()
