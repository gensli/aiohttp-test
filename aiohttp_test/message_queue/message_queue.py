import asyncio
from aio_pika import connect_robust, Message, DeliveryMode


class MessageQueue():
    """ Message queue for working with RabbitMQ """

    def __init__(
        self,
        user='guest',
        password='guest',
        host='rabbitmq',
        port='5672',
        queue_name='message-queue',
        handler=None
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.handler = handler
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        self.connection = await connect_robust(
            f'amqp://{self.user}:{self.password}@{self.host}:{self.port}/')
        self.channel = await self.connection.channel()
        # limit to send to consumer only single task at the one moment
        await self.channel.set_qos(prefetch_count=1)
        self.queue = await self.channel.declare_queue(
            self.queue_name, durable=True)

    async def send(self, msg):
        # Rabbit will save message to disk (delivery_mode) and
        # client will wait for confirmation about successful saving
        # (managed by aio_pika)
        message = Message(
            str(msg).encode(),
            delivery_mode=DeliveryMode.PERSISTENT)

        await self.channel.default_exchange.publish(
            message,
            routing_key=self.queue_name)

    async def listen(self):
        # async with self.connection:
        async with self.queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for msg in queue_iter:
                async with msg.process():
                    # Only when there is no exception aio_pika will
                    # send aknowledgment
                    # try:
                    asyncio.create_task(self.handler(msg.body.decode()))
                    # except asyncio.CancelledError:
                    # break
