import asyncio

import pytest

from kaiju.runner import AsyncRunner
from kaiju.item import BaseItem
from kaiju.handler import AsyncBaseHandler


class TestItem(BaseItem):
    a: float = 42.5
    b: float = 2.12


class AsyncTestHandler(AsyncBaseHandler):
    async def forward(self, data: TestItem) -> TestItem:
        data.b = data.a - 0.51
        return data


@pytest.mark.parametrize('critical', [True, False])
@pytest.mark.parametrize('n_workers', [1, 2, 4])
def test_correct_runner(critical: bool, n_workers: int):
    runner = AsyncRunner(
        AsyncTestHandler()
    ).critical_section(critical)

    if critical:
        runner = runner.critical_section()

    assert runner._critical_section == critical

    item = TestItem()
    res_item = asyncio.run(runner.async_run(item))

    assert isinstance(res_item, TestItem)
    assert res_item.a == 42.5
    assert res_item.b == 41.99
