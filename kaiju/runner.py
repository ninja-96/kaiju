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
        super().__init__()
        self._handler = handler

    def n_workers(self, n_workers: int) -> Runner:
        self._pool = ThreadPoolExecutor(n_workers)
        return self

    def critical_section(self) -> Runner:
        self._critical_section = True
        return self

    def __call__(self, data: BaseItem) -> None:
        if self._critical_section:
            with self._rlock:
                return self._handler.forward(data)

        return self._handler.forward(data)

    @property
    def pool(self) -> ThreadPoolExecutor:
        return self._pool
