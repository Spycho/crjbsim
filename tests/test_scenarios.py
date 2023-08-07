import pytest

from crjbsim.scenario_test import scenario
from traffic_light_sim import TrafficLight


@scenario
def test_scenario(given, when, then):
    when.pedestrian.presses_button()

    then.car_light.turns(TrafficLight.RED)
    then.time_passes(4.999)
    then.pedestrian_light.turns(TrafficLight.GREEN)
    then.time_passes(29.999)
    then.pedestrian_light.turns(TrafficLight.RED)
    then.time_passes(9.999)
    then.car_light.turns(TrafficLight.GREEN)


def test_scenario_step_basic(given, when, then, step_manager):
    """You should generally use the @scenario decorator instead of calling run on the step manager. This test just exists to mirror the
    step_not_met test."""
    when.pedestrian.presses_button()

    then.car_light.turns(TrafficLight.RED)
    then.time_passes(4.999)
    then.pedestrian_light.turns(TrafficLight.GREEN)

    step_manager.run()


def test_scenario_step_not_met(given, when, then, step_manager):
    when.pedestrian.presses_button()

    then.car_light.turns(TrafficLight.RED)
    then.time_passes(5.001)
    then.pedestrian_light.turns(TrafficLight.GREEN)

    with pytest.raises(AssertionError):
        step_manager.run()
