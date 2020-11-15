
import asyncio
from aioudp import *

UDP_IP = "0.0.0.0" # listen to everything
UDP_PORT = 1235 # port

async def main():
    local = await open_local_endpoint(UDP_IP, UDP_PORT)
    # The local endpoint receives the datagram, along with the address
    while 1:
        data, address = await local.receive()

        # Print: Got 'Hey Hey, My My' from 127.0.0.1 port 50603
        print(f"Got {data!r} from {address[0]} port {address[1]}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    print('helo')