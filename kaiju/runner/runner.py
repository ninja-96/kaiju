from __future__ import annotations

from queue import Queue
from threading import Lock as ThreadLock
from concurrent.futures import ThreadPoolExecutor

from kaiju.runner import BaseRunner
from kaiju.item import BaseItem
from kaiju.handler import BaseHandler


__all__ = [
    'Runner'
]


class Runner(BaseRunner):
    _lock = ThreadLock()
    _critical_section = False
    _pool = ThreadPoolExecutor(1)

    def __init__(self, handler: BaseHandler) -> None:
        if not isinstance(handler, BaseHandler):
            raise TypeError(
                '\'handler\' must be inherited from the \'BaseHandler\' class'
            )

        self._handler = handler

    def start(self) -> Runner:
        return self

    def stop(self) -> Runner:
        return self

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

    def run(self, data: BaseItem) -> BaseItem:
        if self._critical_section:
            with self._lock:
                return self._handler.forward(data)

        return self._handler.forward(data)

    async def async_run(self, data: BaseItem) -> BaseItem:
        raise NotImplementedError()

    @property
    def queue(self) -> Queue:
        raise NotImplementedError()

    @property
    def pool(self) -> ThreadPoolExecutor:
        return self._pool
