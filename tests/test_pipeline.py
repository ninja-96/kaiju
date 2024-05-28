import asyncio

import pytest

from kaiju.pipeline import Pipeline
from kaiju.runner import Runner, AsyncRunner
from kaiju.item import BaseItem
from kaiju.handler import BaseHandler, AsyncBaseHandler


class TestItemWrong:
    x: int = 2
    y: int = 3


class TestItem(BaseItem):
    x: int = 0
    y: int = 1


class TestHandler(BaseHandler):
    def forward(self, data: TestItem) -> TestItem:
        data.y = data.x + 1
        return data


class AsyncTestHandler(AsyncBaseHandler):
    async def forward(self, data: TestItem) -> TestItem:
        await asyncio.sleep(1)  # write file simulation
        return data


def test_correct_pipeline():
    pipeline = Pipeline(
        [
            Runner(TestHandler()).n_workers(2),
            AsyncRunner(AsyncTestHandler())
        ]
    )

    assert isinstance(pipeline, Pipeline)

    item = TestItem()
    res_item = asyncio.run(pipeline(item))
    assert isinstance(res_item, TestItem)
    assert res_item.x == 0
    assert res_item.y == 1


def test_wrong_pipeline_runners():
    with pytest.raises(TypeError):
        Pipeline(
            [
                Runner(TestHandler()).n_workers(2),
                TestHandler(),
                3,
            ]
        )


def test_wrong_pipeline_input():
    pipeline = Pipeline(
        [
            Runner(TestHandler()).n_workers(2)
        ]
    )

    item = TestItemWrong()

    with pytest.raises(TypeError):
        asyncio.run(pipeline(item))
