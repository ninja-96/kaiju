from abc import ABCMeta, abstractmethod
from kaiju.item import BaseItem


__all__ = [
    'BaseHandler'
]


class BaseHandler(metaclass=ABCMeta):
    @abstractmethod
    def forward(self, data: BaseItem) -> BaseItem:
        pass
