import logging

from crjbsim import time_provider

logger = logging.getLogger(__name__)


class EventQueue:
    def __init__(self):
        self._events: set[Event] = set()

    def pop_next(self):
        # TODO: change to store sorted
        next_event = min(self._events, key=lambda event: event.time)
        self._events.remove(next_event)
        return next_event

    def add(self, event):
        self._events.add(event)

    def __bool__(self):
        return bool(self._events)

    def __len__(self):
        return len(self._events)


class Event:
    def __init__(self, time, runnable):
        self.time = time
        self.runnable = runnable

    def execute(self):
        self.runnable()

    def __repr__(self):
        return f"Event({self.time}, {self.runnable})"


class DiscreteEventScheduler:
    def __init__(self):
        self._events = EventQueue()

    def start(self):
        while self._events:
            event = self._events.pop_next()
            assert event.time >= time_provider.get_time()
            time_provider.set_time(event.time)
            logger.debug(f"Executing event {event}")
            event.execute()

    def do_at(self, time, runnable):
        self._events.add(Event(time, runnable))

    def do_in(self, time_delta, runnable):
        self._events.add(Event(time_provider.get_time() + time_delta, runnable))
