"""Async scheduler orchestrating periodic tasks for audio, vision, and summarization."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Awaitable, Callable

import anyio


@dataclass
class PeriodicTask:
    name: str
    interval: timedelta
    coro_factory: Callable[[], Awaitable[None]]


@dataclass
class SchedulerService:
    tasks: list[PeriodicTask]

    async def start(self) -> None:
        async with anyio.create_task_group() as tg:
            for task in self.tasks:
                tg.start_soon(self._run_task, task)

    async def _run_task(self, task: PeriodicTask) -> None:
        while True:
            await task.coro_factory()
            await anyio.sleep(task.interval.total_seconds())
