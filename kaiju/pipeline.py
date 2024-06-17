import asyncio
from typing import List

from kaiju.item import BaseItem
from kaiju.runner import Runner, AsyncRunner, AdvancedRunner
from kaiju.runner.advanced_runner import advanced_runner_call


__all__ = [
    'Pipeline'
]


class Pipeline:
    def __init__(self, runners: List[Runner]) -> None:
        if not isinstance(runners, List):
            raise TypeError(
                '\'runners\' must be list of \'Runner\'s'
            )

        if not all(isinstance(r, (Runner, AsyncRunner, AdvancedRunner)) for r in runners):
            raise TypeError(
                'all \'runners\' must be list of \'Runner\'s'
            )

        self._runners = runners
        for runner in self._runners:
            runner.start()

    async def __call__(self, item: BaseItem) -> BaseItem:
        if not isinstance(item, BaseItem):
            raise TypeError(
                '\'item\' must be inherited from the \'BaseItem\' class'
            )
        loop = asyncio.get_event_loop()
        for runner in self._runners:
            if isinstance(runner, Runner):
                item = await loop.run_in_executor(
                    runner.pool, runner.run, item
                )

            if isinstance(runner, AsyncRunner):
                item = await runner.async_run(item)

            if isinstance(runner, AdvancedRunner):
                item = await loop.run_in_executor(
                    runner.pool,
                    advanced_runner_call,
                    runner.queue,
                    item
                )

        return item

    def __del__(self) -> None:
        for runner in self._runners:
            runner.stop()
