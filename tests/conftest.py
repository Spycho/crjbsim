from _pytest.fixtures import fixture

from crjbsim.scenario_test import StepManager
from traffic_light_scenario_steps import GivenSteps, TrafficThenSteps, WhenSteps
from traffic_light_sim import TrafficLightSim


@fixture
def traffic_light_sim():
    return TrafficLightSim()


@fixture
def given():
    return GivenSteps()


@fixture
def when(step_manager, traffic_light_sim):
    return WhenSteps(step_manager, traffic_light_sim)


@fixture
def then(step_manager, traffic_light_sim):
    return TrafficThenSteps(step_manager, traffic_light_sim)


@fixture
def step_manager():
    return StepManager()