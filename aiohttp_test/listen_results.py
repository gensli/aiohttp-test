import aiohttp
import asyncio
from argparse import ArgumentParser


async def main(host, port):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(
            f'http://{host}:{port}/listen-results'
        ) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(msg.data)
                else:
                    if msg.type == aiohttp.WSMsgType.CLOSE:
                        await ws.close()
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print('Error during receive %s' % ws.exception())
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        pass
                    break


if __name__ == '__main__':
    parser = ArgumentParser(description='Aiohttp sandbox socket client')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host')
    parser.add_argument(
        '--port',
        default=8181,
        type=int,
        help='Port')
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port))
