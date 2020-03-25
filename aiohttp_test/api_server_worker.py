import asyncio
import logging
from argparse import ArgumentParser

from api_server import start_servers


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


if __name__ == '__main__':
    parser = ArgumentParser(description='Aiohttp sandbox api server')
    parser.add_argument(
        '--sites',
        type=int,
        default=1,
        help='count of sites (workers?) (default: 1)')
    args = parser.parse_args()

    logging.info("-- Starting api server... To exit press CTRL+C")
    # rework to asyncio.run?
    loop = asyncio.get_event_loop()
    runner = loop.run_until_complete(start_servers(args.sites))
    logging.info(f"-- Listening at addresses: {runner.addresses}")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("-- Interrupted by user")
        # runner.cancel()
        loop.run_until_complete(runner.cleanup())
        loop.close()
