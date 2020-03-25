import weakref
from aiohttp import web, WSCloseCode

from .routes import get_routes


async def startup_tasks(app):
    app['ws'] = weakref.WeakSet()


async def shutdown_tasks(app):
    for ws in set(app['ws']):
        await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')


async def create_app():
    app = web.Application()
    app.add_routes(get_routes())
    app.on_startup.append(startup_tasks)
    app.on_shutdown.append(shutdown_tasks)

    return app


async def start_servers(sites_count):
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()

    sites = []
    for i in range(1, sites_count + 1):
        # sites.append(web.UnixSite(runner, f'/tmp/aiohttp-test-{i}.sock'))
        sites.append(web.TCPSite(runner, '0.0.0.0', int(f'818{i}')))
    for site in sites:
        await site.start()

    return runner


__all__ = (
    'create_app',
    'start_servers',
)
