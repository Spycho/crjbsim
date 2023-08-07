import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class TrafficLight(Enum):
    RED = 1
    GREEN = 2


class TrafficLightSim:
    def __init__(self):
        self.lights = {
            "car_light": TrafficLight.GREEN,
            "pedestrian_light": TrafficLight.RED,
        }

    async def press_button(self):
        self.lights["car_light"] = TrafficLight.RED
        logger.debug("Car light turned red")

        await asyncio.sleep(5)
        self.lights["pedestrian_light"] = TrafficLight.GREEN
        logger.debug("Pedestrian light turned green")

        await asyncio.sleep(30)
        self.lights["pedestrian_light"] = TrafficLight.RED
        logger.debug("Pedestrian light turned red")

        await asyncio.sleep(10)
        self.lights["car_light"] = TrafficLight.GREEN
        logger.debug("Car light turned green")

    def get_light_state(self, light_id):
        return self.lights[light_id]
