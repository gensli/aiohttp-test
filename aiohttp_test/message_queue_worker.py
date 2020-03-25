import aiohttp
import asyncio
import logging
# import signal

from message_queue import MessageQueue


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


# Handler for tasks in message queue
async def mq_handler(msg):
    logging.info(f"-- Received msg: {msg}. Let's sleep {len(msg)} seconds...")
    await asyncio.sleep(len(msg))

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(
            'http://socket_server:8181/listen-results'
        ) as ws:
            await ws.send_str(msg[::-1])


# One does not simple exit from aio_pika and asyncio!
# https://github.com/mosquito/aio-pika/issues/160
# https://github.com/mosquito/aio-pika/issues/230
# https://github.com/mosquito/aio-pika/issues/253
# https://github.com/mosquito/aiormq/issues/70
# Dirty version (two interrupts, a lot of errors after interrupt)
async def main():
    logging.info("-- Starting message queue... To exit press CTRL+C")
    mq = MessageQueue(handler=mq_handler)

    await mq.connect()
    await mq.listen()

if __name__ == '__main__':
    asyncio.run(main())


# Two interrupts too, less errors but whatever...
# shutdown: https://www.roguelynn.com/words/asyncio-graceful-shutdowns/
# (deprecated?)
# async def main():
#     logging.info("-- Starting message queue... To exit press CTRL+C")
#     mq = MessageQueue()

#     await mq.connect()
#     await mq.listen(handle_message)


# async def shutdown(signal, loop):
#     logging.info(f"Received exit signal {signal.name}...")
#     tasks = [t for t in asyncio.all_tasks() if t is not
#              asyncio.current_task()]

#     for task in tasks:
#         # skipping over shielded coro still does not help
#         if task._coro.__name__ == "cant_stop_me":
#             continue
#         task.cancel()

#     logging.info("Cancelling outstanding tasks")
#     await asyncio.gather(*tasks, return_exceptions=True)
#     loop.stop()


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()

#     signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
#     for s in signals:
#         loop.add_signal_handler(
#             s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

#     try:
#         loop.run_until_complete(main())
#     finally:
#         logging.info("Successfully shutdown service")
#         loop.close()


# Doesn't shutdown gracefully:
# def main():
#     logging.info("-- Starting message queue... To exit press CTRL+C")
#     loop = asyncio.get_event_loop()
#     mq = MessageQueue()
#     loop.run_until_complete(mq.connect())
#     loop.run_until_complete(mq.listen(handle_message))
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         # BUG? Exception raised at the top level
#         logging.info("-- Interrupted by user")
#     finally:
#         loop.run_until_complete(mq.connection.close())
#         loop.close()
#         logging.info("Bye")


# if __name__ == '__main__':
#     main()
