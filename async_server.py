from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio


def filter_handler(address, *args):
    print(f"{address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/accelerometer", filter_handler)

ip = "192.168.0.171"
port = 9000


async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    i = 0
    while(True):
        i += 1
        print(f"Loop {i}")
        await asyncio.sleep(0.1)


async def init_main():
    server = AsyncIOOSCUDPServer(
        (ip, port), dispatcher, asyncio.get_event_loop())
    # Create datagram endpoint and start serving
    transport, protocol = await server.create_serve_endpoint()
    await loop()  # Enter main loop of program
    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
