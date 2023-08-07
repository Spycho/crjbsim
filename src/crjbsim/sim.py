import random

from crjbsim import des_aware_logging, time_provider
from crjbsim.discrete_event_scheduler import DiscreteEventScheduler

scheduler = None


def run_sim(initial_event, post_processing=None):
    set_up()

    global scheduler
    scheduler = DiscreteEventScheduler()

    scheduler.do_in(0, initial_event)

    scheduler.run_to_completion()

    if post_processing:
        post_processing()


def set_up():
    random.seed(0)
    des_aware_logging.setup()
    time_provider.set_time(0)
