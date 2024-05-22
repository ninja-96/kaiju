from typing import Any

import pytest

from kaiju.runner import Runner
from kaiju.item import BaseItem
from kaiju.handler import BaseHandler


class TestItem(BaseItem):
    a: float = 42.5
    b: float = 2.12


class TestHandler(BaseHandler):
    def forward(self, data: TestItem) -> TestItem:
        data.b = data.a - 0.51
        return data


@pytest.mark.parametrize('critical', [True, False])
@pytest.mark.parametrize('n_workers', [1, 2, 4])
def test_correct_runner(critical: bool, n_workers: int):
    runner = Runner(
        TestHandler()
    ).n_workers(n_workers)

    if critical:
        runner = runner.critical_section()

    assert runner._pool._max_workers == n_workers
    assert runner._critical_section == critical

    item = TestItem()
    res_item = runner(item)

    assert isinstance(res_item, TestItem)
    assert res_item.a == 42.5
    assert res_item.b == 41.99


@pytest.mark.parametrize('n_workers', [1.3, None, '4', '4.2'])
def test_wrong_n_workers(n_workers: Any):
    with pytest.raises(TypeError):
        Runner(
            TestHandler()
        ).n_workers(n_workers)


@pytest.mark.parametrize('n_workers', [-1, 0])
def test_low_n_workers(n_workers: Any):
    with pytest.raises(RuntimeError):
        Runner(
            TestHandler()
        ).n_workers(n_workers)
