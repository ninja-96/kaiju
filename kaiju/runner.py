from __future__ import annotations

import asyncio
from asyncio import Lock as AsyncLock

from threading import Lock as ThreadLock
from concurrent.futures import ThreadPoolExecutor

from kaiju.item import BaseItem
from kaiju.handler import BaseHandler, AsyncBaseHandler


__all__ = [
    'Runner',
    'AsyncRunner'
]


class Runner:
    _lock = ThreadLock()
    _critical_section = False
    _pool = ThreadPoolExecutor(1)

    def __init__(self, handler: BaseHandler) -> None:
        if not isinstance(handler, BaseHandler):
            raise TypeError(
                '\'handler\' must be inherited from the \'BaseHandler\' class'
            )

        self._handler = handler

    def n_workers(self, n_workers: int) -> Runner:
        if not isinstance(n_workers, int):
            raise TypeError('\'n_workers\' must be int')

        if n_workers <= 0:
            raise RuntimeError(
                '\'n_workers\' must be >= 1'
            )

        self._pool = ThreadPoolExecutor(n_workers)
        return self

    def critical_section(self, critical: bool = True) -> Runner:
        self._critical_section = critical
        return self

    def __call__(self, data: BaseItem) -> BaseItem:
        if self._critical_section:
            with self._lock:
                return self._handler.forward(data)

        return self._handler.forward(data)

    @property
    def pool(self) -> ThreadPoolExecutor:
        return self._pool


class AsyncRunner:
    _lock = AsyncLock()
    _critical_section = False

    def __init__(self, handler: AsyncBaseHandler) -> None:
        if not isinstance(handler, AsyncBaseHandler):
            raise TypeError(
                '\'handler\' must be inherited from the \'AsyncBaseHandler\' class'
            )

        self._handler = handler

    def critical_section(self, critical: bool = True) -> Runner:
        self._critical_section = critical
        return self

    async def __call__(self, data: BaseItem) -> BaseItem:
        if self._critical_section:
            async with self._lock:
                return await self._handler.forward(data)

        return await self._handler.forward(data)

    @property
    def pool(self) -> None:
        return None
