import aiohttp
import asyncio
from argparse import ArgumentParser


async def main(host, port, text):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'http://{host}:{port}/queue_reverse_text',
            data={
                'text': text
            }
        ) as resp:
            print(await resp.text())

        await session.close()


if __name__ == '__main__':
    parser = ArgumentParser(description='Aiohttp sandbox client')
    parser.add_argument(
        '--text',
        required=True,
        help='Text that will be reversed')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host')
    parser.add_argument(
        '--port',
        default=8081,
        type=int,
        help='Port')
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.text))
