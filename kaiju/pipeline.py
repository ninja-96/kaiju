from __future__ import annotations

import asyncio
from typing import List

from kaiju.item import BaseItem
from kaiju.runner import Runner, AsyncRunner, AdvancedRunner
from kaiju.runner.advanced_runner import advanced_runner_call


__all__ = [
    '_infinity_run',
    'Pipeline'
]


async def _infinity_run(
    pipeline: Pipeline,
    item: BaseItem,
    batch_size: int
) -> None:
    while True:
        futures = [
            asyncio.create_task(
                pipeline(item.__class__())
            )
            for _ in range(batch_size)
        ]

        await asyncio.gather(*futures)


class Pipeline:
    def __init__(self, *runners: List[Runner]) -> None:
        if len(runners) == 1 and isinstance(runners[0], List):
            runners = runners[0]

        if not all(
            isinstance(r, (Runner, AsyncRunner, AdvancedRunner))
            for r in runners
        ):
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

    def start(self, item: BaseItem, batch_size: int = 4) -> None:
        asyncio.run(_infinity_run(self, item, batch_size))

    def __del__(self) -> None:
        for runner in self._runners:
            runner.stop()
