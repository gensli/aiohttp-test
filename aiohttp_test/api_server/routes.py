from aiohttp import web
from . import handlers


def get_routes():
    return [
        web.post('/queue_reverse_text', handlers.queue_reverse_text)
    ]
