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
logging.basicConfig(level=logging.DEBUG)

async def decode_bytes(stream_bytes):
    decoder = AsyncStreamDecoder()
    decoded_tree = await decoder.decode(stream_bytes)
    messagedecoder = MessageDecoder()
    decoded_message = messagedecoder.parse(decoded_tree)  
    return decoded_message

async def zusitalk(ip, port):
    log.info("Connecting to Zusi3")
    reader, writer = await asyncio.open_connection(
        ip, port)

    log.info("Sending HELLO message")
    hello_msg = messages.HELLO(2, messages.ClientTyp.FAHRPULT, "Schlumpfpult", "1.0")
    log.debug(hello_msg)
    writer.write(encode_obj(hello_msg).encode())

    log.info("Waiting for response")
    response = await decode_bytes(reader)
    log.debug(response)
    if not (isinstance(response, messages.ACK_HELLO) and response.status == b'\x00'):
        log.error("Zusi did not report success for HELLO")

    log.info("Request train speed")
    need_msg = messages.NEEDED_DATA([0x01])
    writer.write(encode_obj(need_msg).encode())
    response = await decode_bytes(reader)
    log.debug(response)

    try:
        while True:
            response = await decode_bytes(reader)
            log.info("Got response: %s" % response)
            asyncio.sleep(0.1)
    except KeyboardInterrupt:
        pass
    log.info("Disconnecting")
    writer.close()

asyncio.run(zusitalk(ZUSI_IP, ZUSI_PORT))
