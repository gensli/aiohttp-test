from aiohttp import web
from aiojobs.aiohttp import setup

from message_queue import MessageQueue
from .routes import get_routes


async def startup_tasks(app):
    mq = MessageQueue()
    await mq.connect()
    app['mq'] = mq


async def cleanup_tasks(app):
    # BUG? Client tried to reconnect anyway
    await app['mq'].connection.close()


async def create_app():
    app = web.Application()
    setup(app)
    app.add_routes(get_routes())
    app.on_startup.append(startup_tasks)
    app.on_cleanup.append(cleanup_tasks)

    return app


async def start_servers(sites_count):
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()

    sites = []
    for i in range(1, sites_count + 1):
        # sites.append(web.UnixSite(runner, f'/tmp/aiohttp-test-{i}.sock'))
        sites.append(web.TCPSite(runner, '0.0.0.0', int(f'808{i}')))
    for site in sites:
        await site.start()
    # curl -i -X POST -d "text=abcdef" http://localhost:8081/queue_reverse_text

    return runner


__all__ = (
    'create_app',
    'start_servers',
)
