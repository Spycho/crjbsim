import datetime


class _TimeProvider:
    def __init__(self):
        self.time = 0  # ms


_instance = _TimeProvider()


def get_time() -> int:
    """Gets the system time in milliseconds"""
    return _instance.time


def get_time_formatted() -> str:
    return datetime.datetime.fromtimestamp(_instance.time / 1000).strftime('%H:%M:%S.%f')[:-3]


def set_time(time: int):
    """Sets the system time in milliseconds. Should only be called from the discrete event scheduler"""
    _instance.time = time
