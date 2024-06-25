import aio_pika

from config import log


class RMQConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.queues = {}

    async def __aenter__(self):
        log.info(f"Connecting to RabbitMQ at {self.host}:{self.port}.")
        self.connection = await aio_pika.connect_robust(
            f"amqp://{self.username}:{self.password}@{self.host}:{self.port}",
            login=self.username,
            password=self.password,
        )
        self.channel = await self.connection.channel()
        return self

    async def add_queue(self, queue_name):
        self.queues[queue_name] = await self.channel.declare_queue(queue_name)

    async def publish_message(self, queue_name, message):
        queue = self.queues.get(queue_name)
        if not queue:
            raise ValueError(f"Queue {queue_name} not yet declared")
        ...
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()), routing_key=self.queue_name
        )
        print(f"Message published to {self.queue_name}: {message}")

    async def receive(self, queue_name):
        queue = self.queues.get(queue_name)
        if not queue:
            raise ValueError(f"Queue {queue_name} not yet declared")
        return await queue.get(fail=False)

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection is not None:
            await self.connection.close()
            log.info(f"Connection to RabbitMQ at {self.host}:{self.port} is closed.")
