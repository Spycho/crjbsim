from functools import partial

from crjbsim.scenario_test import ChangesToStep, ExecuteStep, ThenSteps


class GivenSteps:
    pass


class PedestrianSteps:
    def __init__(self, step_manager, traffic_light_sim):
        self.step_manager = step_manager
        self.traffic_light_sim = traffic_light_sim

    def presses_button(self):
        self.step_manager.add_step(ExecuteStep(self.traffic_light_sim.press_button))


class WhenSteps:
    def __init__(self, step_manager, traffic_light_sim):
        self.step_manager = step_manager
        self.pedestrian = PedestrianSteps(step_manager, traffic_light_sim)


class TrafficLightSteps:
    def __init__(self, step_manager, traffic_light_sim, traffic_light_id):
        self.step_manager = step_manager
        self.traffic_light_sim = traffic_light_sim
        self.traffic_light_id = traffic_light_id

    def turns(self, color):
        self.step_manager.add_step(ChangesToStep(partial(self.traffic_light_sim.get_light_state, self.traffic_light_id), color))


class TrafficThenSteps(ThenSteps):
    def __init__(self, step_manager, traffic_light_sim):
        super().__init__(step_manager)
        self.traffic_light_sim = traffic_light_sim
        self.car_light = TrafficLightSteps(step_manager, traffic_light_sim, "car_light")
        self.pedestrian_light = TrafficLightSteps(step_manager, traffic_light_sim, "pedestrian_light")
