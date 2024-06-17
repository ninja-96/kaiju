from __future__ import annotations

from asyncio import Lock as AsyncLock
from queue import Queue
from concurrent.futures import Executor

from kaiju.runner import BaseRunner
from kaiju.item import BaseItem
from kaiju.handler import AsyncBaseHandler


__all__ = [
    'AsyncRunner'
]


class AsyncRunner(BaseRunner):
    _lock = AsyncLock()
    _critical_section = False

    def __init__(self, handler: AsyncBaseHandler) -> None:
        if not isinstance(handler, AsyncBaseHandler):
            raise TypeError(
                '\'handler\' must be inherited from the \'AsyncBaseHandler\' class'
            )

        self._handler = handler

    def start(self) -> AsyncRunner:
        return self

    def stop(self) -> AsyncRunner:
        return self

    def n_workers(self, n_workers: int) -> AsyncRunner:
        pass

    def critical_section(self, critical: bool = True) -> AsyncRunner:
        self._critical_section = critical
        return self

    def run(self, data: BaseItem) -> BaseItem:
        raise NotImplementedError()

    async def async_run(self, data: BaseItem) -> BaseItem:
        if self._critical_section:
            async with self._lock:
                return await self._handler.forward(data)

        return await self._handler.forward(data)

    @property
    def queue(self) -> Queue:
        raise NotImplementedError()

    @property
    def pool(self) -> Executor:
        raise NotImplementedError()
