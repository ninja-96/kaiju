from __future__ import annotations

import multiprocessing as mp
from multiprocessing import Process, Queue
from multiprocessing import Lock
from concurrent.futures import ProcessPoolExecutor

from kaiju.runner import BaseRunner
from kaiju.item import BaseItem
from kaiju.handler import BaseHandler


__all__ = [
    'AdvancedRunner'
]


def _advanced_runner_process(
    lock: Lock,
    queue: Queue,
    critical: bool,
    handler_cls: BaseHandler,
    handler_args,
    handler_kwargs
):
    handler = handler_cls(*handler_args, **handler_kwargs)

    while True:
        pipe = queue.get()
        if pipe is None:
            break

        data = pipe.recv()

        if critical:
            with lock:
                result = handler.forward(data)
        else:
            result = handler.forward(data)

        pipe.send(result)
        pipe.close()


def advanced_runner_call(
    queue: Queue,
    item: BaseItem
):
    parent_conn, child_conn = mp.Pipe()

    queue.put(child_conn)
    parent_conn.send(item)

    data = parent_conn.recv()

    parent_conn.close()
    child_conn.close()
    return data


class AdvancedRunner(BaseRunner):
    _lock = None
    _critical_section = False

    _n_workers = 1
    _pool = None

    _queue = None
    _processes = []

    def __init__(
        self,
        handler_cls: type,
        *args,
        **handler_kwargs
    ) -> None:
        if not issubclass(handler_cls, BaseHandler):
            raise TypeError(
                '\'handler\' must be inherited from the \'BaseHandler\' class'
            )

        self._handler_cls = handler_cls
        self._handler_args = args
        self._handler_kwargs = handler_kwargs

    def start(self) -> AdvancedRunner:
        ctx = mp.get_context()

        self._pool = ProcessPoolExecutor(
            self._n_workers, mp_context=ctx
        )

        manager = ctx.Manager()
        self._lock = manager.Lock()
        self._queue = manager.Queue()

        for _ in range(self._n_workers):
            tmp = Process(
                target=_advanced_runner_process,
                args=(
                    self._lock,
                    self._queue,
                    self._critical_section,
                    self._handler_cls,
                    self._handler_args,
                    self._handler_kwargs
                )
            )
            tmp.start()
            self._processes.append(tmp)

        return self

    def stop(self) -> AdvancedRunner:
        for p in self._processes:
            self._queue.put(None)

        for p in self._processes:
            p.join()

        return self

    def n_workers(self, n_workers: int) -> AdvancedRunner:
        if not isinstance(n_workers, int):
            raise TypeError('\'n_workers\' must be int')

        if n_workers <= 0:
            raise RuntimeError(
                '\'n_workers\' must be >= 1'
            )

        self._n_workers = n_workers
        return self

    def critical_section(self, critical: bool = True) -> AdvancedRunner:
        self._critical_section = critical
        return self

    def run(self, data: BaseItem) -> BaseItem:
        raise NotImplementedError(
            'Use \'advanced_runner_call(...) ',
            'function in \'loop.run_in_executor(...)\''
        )

    @property
    def pool(self) -> ProcessPoolExecutor:
        return self._pool

    @property
    def queue(self) -> Queue:
        return self._queue
