import asyncio
import logging
import time
from asyncio import DefaultEventLoopPolicy, events
from datetime import datetime

from crjbsim import des_aware_logging, sim, time_provider
from crjbsim.asncio_des import DiscreteEventLoopPolicy

logger = logging.getLogger(__name__)


async def action(name, delay, repetition):
    logger.info(f"{name} started at {datetime.now()}")
    for i in range(repetition):
        await asyncio.sleep(delay)
        logger.info(f"{name} repetition {i} done at {datetime.now()}")
    logger.info(f"{name} finished at {datetime.now()}")


async def asyncfn():
    await asyncio.gather(
        action("A", 0.1, 3),
        action("B", 0.15, 3),
    )


def test_async_des():
    des_aware_logging.setup()
    try:
        asyncio.set_event_loop_policy(DiscreteEventLoopPolicy())
        asyncio.run(asyncfn())
    finally:
        asyncio.set_event_loop_policy(DefaultEventLoopPolicy())

    assert time_provider.get_time() == 3 * 0.15


def test_async_des_for_leaking_state_between_runs():
    des_aware_logging.setup()
    try:
        asyncio.set_event_loop_policy(DiscreteEventLoopPolicy())
        asyncio.run(asyncfn())
    finally:
        asyncio.set_event_loop_policy(DefaultEventLoopPolicy())

    assert time_provider.get_time() == 3 * 0.15


def test_async_realtime_sim():
    """Without overriding the event loop, this should function as a real-time simulation"""
    start_time = time.time()
    asyncio.run(asyncfn())
    end_time = time.time()
    duration = end_time - start_time
    assert duration >= 3 * 0.15


class Conveyor:
    def __init__(self):
        self.downstream_space = asyncio.Event()
        self.downstream_space.set()

    async def container_arrived(self, container_id):
        logger.info(f"container {container_id} arrived")

        await self.downstream_space.wait()

        logger.info(f"container {container_id} moving")
        self.downstream_space.clear()

        await asyncio.sleep(1)  # simulated movement time

        logger.info(f"container {container_id} moved")
        notify(container_id)
        self.downstream_space.set()


async def add_container(conveyor, container_id, entry_time):
    await asyncio.sleep(entry_time)
    await conveyor.container_arrived(container_id)


async def conveyor_sim():
    conveyor = Conveyor()
    await asyncio.gather(
        add_container(conveyor, 0, 0),
        add_container(conveyor, 1, 0.5),
        add_container(conveyor, 2, 1.75),
        add_container(conveyor, 3, 10),
    )


data = []


def notify(container_id):
    global data
    data.append((time_provider.get_time(), container_id))


def test_async_des_realistic():
    des_aware_logging.setup()
    try:
        asyncio.set_event_loop_policy(DiscreteEventLoopPolicy())
        asyncio.run(conveyor_sim())
    finally:
        asyncio.set_event_loop_policy(DefaultEventLoopPolicy())

    assert data[0] == (1, 0)
    assert data[1] == (2, 1)
    assert data[2] == (3, 2)
    assert data[3] == (11, 3)


def test_async_des_mixed():
    """Tests that we can run a single simulation using both direct scheduler calls and asyncio awaits. Aids migration."""

    test_list = []

    async def mixed_sim():
        await asyncio.sleep(1)
        events.get_running_loop().scheduler.do_in(2, lambda: test_list.append(1))

    des_aware_logging.setup()
    try:
        asyncio.set_event_loop_policy(DiscreteEventLoopPolicy())
        asyncio.run(mixed_sim())
    finally:
        asyncio.set_event_loop_policy(DefaultEventLoopPolicy())

    assert test_list == [1]
    assert time_provider.get_time() == 3
