# WARNING
Zusi 3.5 introduced breaking changes without increasing API version, so ensure to use pyzusi 1.2.1 for Zusi 3.4 and below

# pyzusi3
Library to talk to Zusi3 without any specialized purpose.

Intentionally the message parameters are taken almost word-by-word from Zusi documentation to make using the lib easier.
So be prepared for some mixing of code language (english) and zusi-lib language (german).

# Examples

## Minimal code example
```python
import asyncio

async def print_state(client):
    while True:
        print(client.local_state)
        asyncio.sleep(1)

tasks = []
async def main(ip, port):
    client = ZusiClient(ip, port, "pyzusi3 demo", "1.0")
    client.request_status(displays=[
            messages.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT,
            messages.FAHRPULT_ANZEIGEN.STATUS_SIFA
        ],
        programdata=[
            messages.PROGRAMMDATEN.ZUGDATEI,
            messages.PROGRAMMDATEN.ZUGNUMMER
        ]
    )

    main_task = asyncio.create_task(client.connect())
    tasks.append(main_task)

    watch_task = asyncio.create_task(print_state(client))
    tasks.append(watch_task)

if __name__ == "__main__":
    run_loop = asyncio.new_event_loop()
    run_loop.create_task(main(ZUSI_IP, ZUSI_PORT))
    run_loop.run_forever()
```

## Interaction simulation
see [interactiondemo.py](https://github.com/jokey2k/pyzusi3/blob/main/examples/interactiondemo.py)

## AutoSifa Tool
Can be downloaded here, built as one file python executable, digitally signed
![ZusiData](https://github.com/jokey2k/pyzusi3/blob/main/examples/autosifa/screenshot.png?raw=true)

## PySide6 UI
![ZusiData](https://github.com/jokey2k/pyzusi3/blob/main/examples/pyzusidisplay/screenshot.png?raw=true)
