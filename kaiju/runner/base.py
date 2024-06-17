from __future__ import annotations

from abc import ABCMeta, abstractmethod
from queue import Queue
from concurrent.futures import Executor

from kaiju.item import BaseItem


__all__ = [
    'BaseRunner'
]


class BaseRunner(metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> BaseRunner:
        pass

    @abstractmethod
    def stop(self) -> BaseRunner:
        pass

    @abstractmethod
    def n_workers(self, n_workers: int) -> BaseRunner:
        pass

    @abstractmethod
    def critical_section(self, critical: bool = True) -> BaseRunner:
        pass

    @abstractmethod
    def run(self, data: BaseItem) -> BaseItem:
        pass

    @abstractmethod
    async def async_run(self, data: BaseItem) -> BaseItem:
        pass

    @property
    @abstractmethod
    def queue(self) -> Queue:
        pass

    @property
    @abstractmethod
    def pool(self) -> Executor:
        pass
