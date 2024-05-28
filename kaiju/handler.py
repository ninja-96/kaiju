from abc import ABCMeta, abstractmethod
from kaiju.item import BaseItem


__all__ = [
    'BaseHandler',
    'AsyncBaseHandler'
]


class BaseHandler(metaclass=ABCMeta):
    @abstractmethod
    def forward(self, data: BaseItem) -> BaseItem:
        pass


class AsyncBaseHandler(metaclass=ABCMeta):
    @abstractmethod
    async def forward(self, data: BaseItem) -> BaseItem:
        pass
