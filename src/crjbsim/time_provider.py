import datetime


class _TimeProvider:
    def __init__(self):
        self.time = 0  # seconds


_instance = _TimeProvider()


def get_time() -> int:
    """Gets the system time in seconds"""
    return _instance.time


def get_time_formatted() -> str:
    return datetime.datetime.fromtimestamp(_instance.time).strftime('%H:%M:%S.%f')[:-3]


def set_time(time: int):
    """Sets the system time in seconds. Should only be called from the discrete event scheduler"""
    _instance.time = time
