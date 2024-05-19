import asyncio
from typing import List

from kaiju.item import BaseItem
from kaiju.runner import Runner


__all__ = [
    'Pipeline'
]


class Pipeline:
    def __init__(self, runners: List[Runner]) -> None:
        self._runners = runners

    async def __call__(self, item: BaseItem) -> BaseItem:
        loop = asyncio.get_event_loop()
        for runner in self._runners:
            item = await loop.run_in_executor(
                runner.pool, runner, item
            )

        return item
