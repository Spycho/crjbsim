import asyncio
import heapq
import inspect
import itertools
import logging

from crjbsim import time_provider

logger = logging.getLogger(__name__)


class EventQueue:
    def __init__(self):
        self._events: list[Event] = []

    def pop_next(self):
        return heapq.heappop(self._events)

    def add(self, event):
        heapq.heappush(self._events, event)

    def only_daemons_left(self):
        return all(event.daemon for event in self._events)

    def __bool__(self):
        return bool(self._events)

    def __len__(self):
        return len(self._events)

event_id_generator = itertools.count()

class Event:
    def __init__(self, time, runnable, daemon):
        self.id = next(event_id_generator)
        self.time = time
        self.runnable = runnable
        self.daemon = daemon
        self.cancelled = False

    def __call__(self):
        if not self.cancelled:
            result = self.runnable()
            if inspect.iscoroutine(result):
                asyncio.create_task(result)

    def cancel(self):
        self.cancelled = True

    def __lt__(self, other):
        if self.time == other.time:
            return self.id < other.id
        return self.time < other.time

    def __le__(self, other):
        if self.time == other.time:
            return self.id <= other.id
        return self.time <= other.time

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __repr__(self):
        return f"Event({self.time}, {self.runnable}, daemon={self.daemon})"


class DiscreteEventScheduler:
    def __init__(self):
        self._events = EventQueue()
        self.post_event_callbacks = []

    def run_to_completion(self):
        while self._events and not self._events.only_daemons_left():
            self.run_next_event()

    def run_next_event(self):
        event = self._events.pop_next()
        assert event.time >= time_provider.get_time()
        time_provider.set_time(event.time)
        logger.debug(f"Executing event {event}")
        event()
        for callback in self.post_event_callbacks:
            callback()

    def do_at(self, time, runnable, daemon=False):
        event = Event(time, runnable, daemon)
        self._events.add(event)
        return event

    def do_in(self, time_delta, runnable, daemon=False):
        return self.do_at(time_provider.get_time() + time_delta, runnable, daemon)

    def register_post_event_callback(self, callback):
        self.post_event_callbacks.append(callback)
