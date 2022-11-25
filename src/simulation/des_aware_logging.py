import logging
from logging import StreamHandler

from src.simulation import time_provider


class Handler(StreamHandler):
    def format(self, record):
        return f"{time_provider.get_time_formatted()} {super().format(record)}"


def setup():
    root_logger = logging.getLogger()
    handler = Handler()
    handler.formatter = logging.Formatter('%(levelname)-8s: %(message)s (%(name)s)')
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.DEBUG)
