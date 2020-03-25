import logging
from aiohttp import web
from aiojobs.aiohttp import atomic


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


@atomic
async def queue_reverse_text(request):
    data = await request.post()
    text = data.get('text', None)

    if text is None:
        return web.Response(status=400, reason='Text is required')

    await request.app['mq'].send(text)

    return web.Response(text='Got it')
