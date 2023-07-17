import functools
import logging

from crjbsim import des_aware_logging, sim, time_provider

logger = logging.getLogger(__name__)


def test_sim():
    test_list = []
    sim.run_sim(lambda: test_list.append(1))
    assert test_list == [1]


def test_sim_post_process():
    test_list = []
    sim.run_sim(lambda: test_list.append(1), lambda: test_list.append(2))
    assert test_list == [1, 2]


def test_sim_do_at():
    test_list = []
    sim.run_sim(lambda: sim.scheduler.do_at(5, lambda: test_list.append(1)))
    assert test_list == [1]
    assert time_provider.get_time() == 5


def test_sim_do_in():
    test_list = []
    sim.run_sim(lambda: sim.scheduler.do_in(5, lambda: sim.scheduler.do_in(5, lambda: test_list.append(1))))
    assert test_list == [1]
    assert time_provider.get_time() == 10


class Conveyor:
    def __init__(self):
        self.downstream_space = True
        self.containers_waiting = []

    def container_arrived(self, container_id):
        logger.info(f"container {container_id} arrived")
        self.containers_waiting.append(container_id)
        if self.downstream_space:
            self.move_container()

    def move_container(self):
        container_id = self.containers_waiting.pop(0)
        logger.info(f"container {container_id} moving")
        self.downstream_space = False
        sim.scheduler.do_in(1, functools.partial(self.container_moved, container_id))

    def container_moved(self, container_id):
        logger.info(f"container {container_id} moved")
        notify(container_id)
        self.downstream_space = True
        if self.containers_waiting:
            self.move_container()


def add_container(conveyor, container_id):
    conveyor.container_arrived(container_id)


def conveyor_sim():
    conveyor = Conveyor()

    sim.scheduler.do_in(0, functools.partial(conveyor.container_arrived, 0)),
    sim.scheduler.do_in(0.5, functools.partial(conveyor.container_arrived, 1)),
    sim.scheduler.do_in(1.75, functools.partial(conveyor.container_arrived, 2)),
    sim.scheduler.do_in(10, functools.partial(conveyor.container_arrived, 3)),


data = []


def notify(container_id):
    global data
    data.append((time_provider.get_time(), container_id))


def test_sim_realistic():
    des_aware_logging.setup()
    time_provider.set_time(0)
    sim.run_sim(conveyor_sim)
    assert data[0] == (1, 0)
    assert data[1] == (2, 1)
    assert data[2] == (3, 2)
    assert data[3] == (11, 3)
