import asyncio
from typing import List

from kaiju.item import BaseItem
from kaiju.runner import Runner


__all__ = [
    'Pipeline'
]


class Pipeline:
    def __init__(self, runners: List[Runner]) -> None:
        if not isinstance(runners, List):
            raise TypeError(
                '\'runners\' must be list of \'Runner\'s'
            )

        if not all(isinstance(r, Runner) for r in runners):
            raise TypeError(
                'all \'runners\' must be list of \'Runner\'s'
            )

        self._runners = runners

    async def __call__(self, item: BaseItem) -> BaseItem:
        if not isinstance(item, BaseItem):
            raise TypeError(
                '\'item\' must be inherited from the \'BaseItem\' class'
            )
        loop = asyncio.get_event_loop()
        for runner in self._runners:
            item = await loop.run_in_executor(
                runner.pool, runner, item
            )

        return item
