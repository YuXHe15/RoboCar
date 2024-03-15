from abc import ABC, abstractmethod
import numpy as np
from robocar import motor_control as mc
from pathlib import Path
import logging

file_path = Path(__file__).parent.parent.parent / "config.toml"
from robocar.config_log import (
    setup_logging,
)

logger = logging.getLogger(__name__)

logger.info("Motor control initialized.")


class KineticSystem(ABC):
    def __init__(
        self,
    ) -> None:
        self.accelerate = 0.0
        self.steer = 0.0

    @abstractmethod
    def drive(self, accelerate: float, steer: float) -> None:
        pass

    @abstractmethod
    def get_state(self) -> dict:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class SSMRKineticSystem(KineticSystem):
    def __init__(
        self,
        wheelbase: float,
        track_bottom_to_COM: float,
        track_front_to_COM: float,
        radius_wheel: float,
        chassis: mc.MotorControl = mc.FourWheelMotorControl,
        alpha: float = 1,
    ) -> None:
        self.chassis = chassis(alpha=alpha, config_path=file_path)
        self.chassis.start()
        self.wheelbase = wheelbase
        self.track_bottom_to_COM = track_bottom_to_COM
        self.track_front_to_COM = track_front_to_COM
        self.radius_wheel = radius_wheel
        self.vx = 0.0
        self.vy = 0.0
        self.theta = 0.0
        self.vX = 0.0
        self.vY = 0.0
        self.v1x = 0.0
        self.v1y = 0.0
        self.v2x = 0.0
        self.v2y = 0.0
        self.v3x = 0.0
        self.v3y = 0.0
        self.v4x = 0.0
        self.v4y = 0.0
        self.w1 = 0.0
        self.w2 = 0.0
        self.w3 = 0.0
        self.w4 = 0.0
        self.w = 0.0
        self.d1 = 0.0
        self.d2 = 0.0
        self.d3 = 0.0
        self.d4 = 0.0
        self.dc = 0.0
        self.xICR = 0.5 * self.track_front_to_COM - self.track_bottom_to_COM
        self.yICR = 0.0
        super().__init__()

    def update(self, vx, w) -> None:
        self.yICR = vx / w if w != 0 else 0
        coefficient_matrix = np.array(
            [
                [1, -0.5 * self.wheelbase],
                [1, 0.5 * self.wheelbase],
                [0, -self.xICR + self.track_front_to_COM],
                [0, -self.xICR - self.track_bottom_to_COM],
            ]
        )
        V = coefficient_matrix @ np.array([vx, w])
        self.v1x = self.v2x = V[0]
        self.v3x = self.v4x = V[1]
        self.v2y = self.v3y = V[2]
        self.v1y = self.v4y = V[3]
        self.w1 = self.v1x / self.radius_wheel
        self.w2 = self.v2x / self.radius_wheel
        self.w3 = self.v3x / self.radius_wheel
        self.w4 = self.v4x / self.radius_wheel
        self.chassis.move(self.w2, self.w3, self.w1, self.w4)

    def drive(self, accelerate: float, steer: float) -> None:
        self.accelerate = accelerate
        self.steer = steer
        
        self.update(self.accelerate, self.steer)

    def get_state(self) -> dict:
        return {"accelerate": self.accelerate, "steer": self.steer}
