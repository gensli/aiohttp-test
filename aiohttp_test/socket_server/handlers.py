import aiohttp
import logging


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


async def listen_results(request):
    res = aiohttp.web.WebSocketResponse()
    await res.prepare(request)
    await res.send_str("Salut, let's wait some text...")
    request.app['ws'].add(res)

    try:
        async for msg in res:
            if msg.type == aiohttp.WSMsgType.TEXT:
                logging.info(f"Websocket message: {msg.data}")
                for ws in request.app['ws']:
                    if ws is not res:
                        await ws.send_str(msg.data)
            else:
                logging.error(
                    f"Websocket connection closed: {ws.exception()}")
                break
    finally:
        logging.info("Someone disconnected")
        request.app['ws'].discard(res)

    return res
