import asyncio
import inspect
import logging
from asyncio import DefaultEventLoopPolicy

from crjbsim import sim, time_provider
from crjbsim.asncio_des import DiscreteEventLoopPolicy

logger = logging.getLogger(__name__)


class ExecuteStep:
    def __init__(self, runnable):
        self.runnable = runnable

    def __call__(self):
        result = self.runnable()
        if inspect.iscoroutine(result):
            asyncio.create_task(result)
        return True


class ChangesToStep:
    def __init__(self, get_data, target_data):
        self.target_data = target_data
        self.get_data = get_data
        self.previous_data = None
        self.first_execution = True

    def __call__(self):
        data = self.get_data()
        if not self.first_execution and data != self.previous_data and data == self.target_data:
            return True

        self.first_execution = False
        self.previous_data = data


class DelayStep:
    def __init__(self, time_in_seconds):
        assert time_in_seconds > 0
        self.time_in_seconds = time_in_seconds
        self.start_time = None
        self.end_time = None
        self.task = None

    def __call__(self):
        if self.task:
            if self.task.done():
                self.end_time = time_provider.get_time()
                return True
        else:
            self.start_time = time_provider.get_time()
            self.task = asyncio.create_task(self._delay())

    async def _delay(self):
        await asyncio.sleep(self.time_in_seconds)


class ThenSteps:
    def __init__(self, step_manager):
        self.step_manager = step_manager

    def time_passes(self, time_in_seconds):
        self.step_manager.add_step(DelayStep(time_in_seconds))


class StepManager:
    def __init__(self):
        self.steps = []
        self.position = 0

    def add_step(self, step):
        self.steps.append(step)

    def _post_event_callback(self):
        while self.position < len(self.steps):
            step = self.steps[self.position]
            result = step()
            if result:
                logger.debug(f"Step {self.position} finished: {step}")
                self.position += 1
            else:
                return

    def _trigger(self):
        sim.set_up()

        sim.scheduler.register_post_event_callback(self._post_event_callback)

        self._post_event_callback()

    async def _trigger_async(self):
        return self._trigger()

    def run(self):
        try:
            asyncio.set_event_loop_policy(DiscreteEventLoopPolicy())
            result = asyncio.run(self._trigger_async())
            if result.exception():
                raise result.exception()
        finally:
            asyncio.set_event_loop_policy(DefaultEventLoopPolicy())

        assert self._finished(), "Not all steps have completed, but the simulation ended"

    def _finished(self):
        return self.position == len(self.steps)

def scenario(fn):
    """Decorator for scenario tests"""
    def scenario_test(given, when, then, step_manager):
        fn(given, when, then)
        step_manager.run()

    return scenario_test