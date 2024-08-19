from __future__ import annotations

from abc import ABCMeta, abstractmethod


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
