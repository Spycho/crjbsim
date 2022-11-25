import random

from simulation import des_aware_logging
from simulation.discrete_event_scheduler import DiscreteEventScheduler


def run_sim(initial_event, post_processing=None):
    random.seed(0)
    des_aware_logging.setup()
    scheduler = DiscreteEventScheduler()

    scheduler.do_in(0, initial_event)

    scheduler.start()

    if post_processing:
        post_processing()