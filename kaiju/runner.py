from __future__ import annotations

from threading import RLock
from concurrent.futures import ThreadPoolExecutor

from kaiju.item import BaseItem
from kaiju.handler import BaseHandler


__all__ = [
    'Runner'
]


class Runner:
    _rlock = RLock()
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

    def critical_section(self) -> Runner:
        self._critical_section = True
        return self

    def __call__(self, data: BaseItem) -> BaseItem:
        if self._critical_section:
            with self._rlock:
                return self._handler.forward(data)

        return self._handler.forward(data)

    @property
    def pool(self) -> ThreadPoolExecutor:
        return self._pool
