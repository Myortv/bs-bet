import logging
import json
import asyncio

from collections.abc import Iterator
from typing import Any, Callable, Optional, Generator, ContextManager


from contextlib import asynccontextmanager


from aio_pika.pool import Pool
import aio_pika


from app.core.config import configs


class RabbitMQ:
    def __init__(self):
        self.url = None
        self.pool_size = None
        self.connection_pool = None
        self.channel_pool = None
        self.subscibed_functions = dict()

    async def initialize(
        self,
        url: str,
        pool_size: Optional[int] = 10,
    ) -> None:
        self.url = url
        self.pool_size = pool_size
        self.connection_pool = Pool(self._get_connection, max_size=self.pool_size)
        self.channel_pool = Pool(self._get_channel, max_size=self.pool_size)

    async def stop(
        self,
    ) -> None:
        if self.channel_pool:
            if not self.channel_pool.is_closed:
                await asyncio.ensure_future(self.channel_pool.close())
        if self.connection_pool:
            if not self.connection_pool.is_closed:
                await asyncio.ensure_future(self.connection_pool.close())

    async def _get_connection(self):
        return await aio_pika.connect_robust(self.url)

    async def _get_channel(self):
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    @asynccontextmanager
    async def get_channel(self) -> ContextManager[aio_pika.Channel]:
        async with self.channel_pool.acquire() as channel:
            yield channel

    async def publish(
        self,
        exchange_name: str,
        routing_key: str,
        message: aio_pika.Message,
    ):
        async with self.get_channel() as channel:
            exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)
            await exchange.publish(message, routing_key)

    def subscribe(
        self,
        exchange_name: str,
        routing_key: str,
        func: Callable,
    ) -> None:
        self.subscibed_functions[(exchange_name, routing_key)] = func

    async def start_consuming(self) -> None:
        async with self.get_channel() as channel:

            for exchange, message_key in self.subscibed_functions.keys():
                queue = await channel.declare_queue(auto_delete=True)
                exchange_obj = await channel.declare_exchange(
                    exchange,
                    aio_pika.ExchangeType.DIRECT,
                )
                await queue.bind(exchange_obj, routing_key=message_key)

                async def callback(message: aio_pika.Message):
                    async with message.process():
                        info = message.info()
                        func = self.subscibed_functions[
                            (info.get('exchange'), info.get('routing_key'))
                        ]
                        await func(
                            json.loads(message.body.decode())
                        )

                await queue.consume(callback)
                logging.debug(
                    "Fuction "
                    f"{self.subscibed_functions[(exchange, message_key)]} "
                    f"{(exchange, message_key)} "
                    "starts consuming"
                )




rabbit_manager = RabbitMQ()
