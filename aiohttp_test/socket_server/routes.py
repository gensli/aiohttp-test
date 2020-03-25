from aiohttp import web
from . import handlers


def get_routes():
    return [
        web.get('/listen-results', handlers.listen_results)
    ]
