import asyncio
import logging
import os.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pyzusi3 import messages
from pyzusi3.client import ZusiClient, suppress_none_values

ZUSI_IP = "127.0.0.1"
ZUSI_PORT = "1436"

WAIT_MAX = 3000 # keep running for 5 minutes

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("ZusiDemo")
log.setLevel(logging.INFO)
logging.getLogger("pyzusi3.client").setLevel(logging.INFO)
logging.getLogger("pyzusi3.messagecoders.MessageDecoder").setLevel(logging.ERROR)


def handle_exception(loop, context):
    """Dummy handler to log errors in demo to console"""
    msg = context.get("exception", context["message"])
    log.error(f"Caught exception: {msg}")


async def zusi_user_interact(client: ZusiClient):
    """Simulation for some random user input to be sent to Zusi"""

    zuord = messages.INPUT_TASTATURZUORDNUNG
    komm = messages.INPUT_TASTATURKOMMANDO
    aktion = messages.INPUT_TASTATURAKTION

    simulated_interactions = {
        100: messages.INPUT(zuord.FAHRSCHALTER, komm.Unbestimmt, aktion.Absolut, tastatur_schalterposition=5),
        109: messages.INPUT(zuord.SIFA, komm.Unbestimmt, aktion.Down, tastatur_schalterposition=0),
        110: messages.INPUT(zuord.SIFA, komm.Unbestimmt, aktion.Up, tastatur_schalterposition=0),
        150: messages.INPUT(zuord.FAHRSCHALTER, komm.Unbestimmt, aktion.Absolut, tastatur_schalterposition=0),
        160: messages.INPUT(zuord.SIFA, komm.Unbestimmt, aktion.Down, tastatur_schalterposition=0),
        165: messages.INPUT(zuord.SIFA, komm.Unbestimmt, aktion.Up, tastatur_schalterposition=0),
        170: messages.INPUT(indusi_stoerschalter=messages.SCHALTER.AUS),
        180: messages.INPUT(lzb_stoerschalter=messages.SCHALTER.AUS),
        210: messages.INPUT(lzb_stoerschalter=messages.SCHALTER.EIN),
        220: messages.INPUT(indusi_stoerschalter=messages.SCHALTER.EIN),
    }

    known_states = {}
    wait_cur = 0
    while True:
        # handle incremental updates from Zusi to print only changed state to console
        if client.local_state_changed.is_set():
            client.local_state_changed.clear()
            for message, state in client.local_state.items():
                current_state = state._asdict()
                if message not in known_states:
                    known_states[message] = current_state
                    log.info("%s state: %s" % (message.__name__, suppress_none_values(current_state)))
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
                    log.info("%s changes: %s" % (message.__name__, updates))
        await asyncio.sleep(0.1)
        wait_cur += 1
        if wait_cur in simulated_interactions:
            msg = simulated_interactions[wait_cur]
            log.info("Sending new action %s: %s" % (msg.__class__.__name__, str(suppress_none_values(msg._asdict()))))
            client.send_input(msg)
        if wait_cur > WAIT_MAX:
            log.info("Time is up, leaving")
            break

tasks = []
async def main(ip, port):
    client = ZusiClient(ip, port, "pyzusi3 demo", "1.0")
    client.request_status(displays=[
            messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT,
            messages.FAHRPULT_ANZEIGEN.STATUS_SIFA,
            messages.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
        ],
        control=True,
        programdata=[
            messages.PROGRAMMDATEN.ZUGDATEI,
            messages.PROGRAMMDATEN.ZUGNUMMER,
            messages.PROGRAMMDATEN.LADEPAUSE,
        ]
    )

    main_task = asyncio.create_task(client.connect())
    tasks.append(main_task)

    interact_task = asyncio.create_task(zusi_user_interact(client))
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
    run_loop.create_task(main(ZUSI_IP, ZUSI_PORT))
    run_loop.run_forever()
