import RPi.GPIO as GPIO
import toml
import logging
from robocar.config_log import (
    setup_logging,
)
import time
import numpy as np

logger = logging.getLogger(__name__)

logger.info("Motor control initialized.")


class Motor:
    def __init__(
        self, name, forward_pin, backward_pin, enable_pin, threshold, is_inverted
    ):
        self.name = name
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.enable_pin = enable_pin
        self.threshold = threshold
        self.pwm = None
        self.dt = 1  # Time step for the PWM signal
        # Add an attribute to keep track of whether the orientation is inverted
        self.is_orientation_inverted = is_inverted

    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.backward_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.enable_pin, 1000)  # Set up PWM
        self.pwm.start(0)  # Start PWM with 0% duty cycle
        logger.debug(
            "Motor %sself.name started. Forward pin: %s, Backward pin: %s, Enable pin: %s",
            self.name,
            self.forward_pin,
            self.backward_pin,
            self.enable_pin,
        )

    def close(self):
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup([self.forward_pin, self.backward_pin, self.enable_pin])
        logger.debug(f"Motor {self.name} cleaned up.")

    def stop(self):
        """Stop the motor by setting its duty cycle to 0."""
        self.pwm.ChangeDutyCycle(0)
        logger.debug(f"Motor {self.name} stopped.")

    def set_orientation(self, is_inverted):
        # Set the orientation flag based on the passed parameter
        self.is_orientation_inverted = is_inverted

    def move(self, duty_cycle_ratio):
        # Adjust duty cycle based on the threshold
        effective_duty_cycle = min(
            100,
            max(
                0, (100 - self.threshold) / 100 * abs(duty_cycle_ratio) + self.threshold
            ),
        )
        # Update the PWM duty cycle to move the motor
        self.pwm.ChangeDutyCycle(effective_duty_cycle)
        # Determine the direction and adjust based on orientation
        if (duty_cycle_ratio < 0) != self.is_orientation_inverted:  # XOR operation
            GPIO.output(self.forward_pin, GPIO.HIGH)
            GPIO.output(self.backward_pin, GPIO.LOW)
        else:
            GPIO.output(self.forward_pin, GPIO.LOW)
            GPIO.output(self.backward_pin, GPIO.HIGH)

        logger.debug(
            f"motor{self.name} move on intensity {effective_duty_cycle}, original: {duty_cycle_ratio}"
        )


class MotorControl:
    def __init__(self, config_path="config.toml"):
        """
        Initialize MotorControl with motor instances, each identified by a unique name.

        :param motor_configs: A list of dictionaries, each containing the configuration
                              for a Motor instance, including the name.
        """
        self.motor_configs = self.load_motor_config(config_path)
        self.motors = {
            name: Motor(**config) for name, config in self.motor_configs.items()
        }
        logger.info("MotorControl initialized. Motors: %s", ", ".join(self.motors))

    def load_motor_config(self, config_path):
        # Load motor configurations from a TOML file
        config = toml.load(config_path)
        logger.debug("Motor configurations loaded from %s", config_path)
        return config["motors"]

    def load_chassis_config(self, config_path):
        # Load motor configurations from a TOML file
        config = toml.load(config_path)
        logger.debug("Chassis configurations loaded from %s", config_path)
        return config["chassis"]

    def start_all(self):
        """Initialize all motor instances."""
        for motor in self.motors.values():
            motor.start()
        logger.info("All motors started.")

    def close_all(self):
        """Clean up all motors."""
        for motor in self.motors.values():
            motor.close()
        logger.info("All motors cleaned up.")

    def move_motor(self, name, duty_cycle_ratio):
        """Move a specific motor by name."""
        if name in self.motors:
            self.motors[name].move(duty_cycle_ratio)
        else:
            raise ValueError(f"Motor {name} not found.")

    def stop_motor(self, name):
        """Stop a specific motor by name."""
        if name in self.motors:
            self.motors[name].stop()
        else:
            raise ValueError(f"Motor {name} not found.")

    def stop_all(self):
        """Stop all motors."""
        for motor in self.motors.values():
            motor.stop()
        logger.info("All motors stopped.")


class FourWheelMotorControl(MotorControl):
    def __init__(self, alpha: float = 0.1, config_path="config.toml"):
        super().__init__(config_path)
        self.alpha = alpha
        self.dt = 1  # Time step for the PWM signal
        self.chassis = self.load_chassis_config(config_path)
        self.max_angular_velocity = np.deg2rad(
            self.chassis["angular_velocity"]["max"]
        )  # degrees per second
        if len(self.motors) != 4:
            raise ValueError(
                "FourWheelMotorControl requires exactly four motor configurations."
            )

    def start(self):
        self.start_all()
        logger.info("FourWheelMotorControl started.")

    def move(self, w_FL, w_FR, w_BL, w_BR):
        """Move the vehicle based on the wheel speeds."""
        self.move_motor("LF", w_FL * self.alpha)
        self.move_motor("RF", w_FR * self.alpha)
        self.move_motor("LB", w_BL * self.alpha)
        self.move_motor("RB", w_BR * self.alpha)
        time.sleep(self.dt)
        logger.info(
            "Vehicle moving with angular velocity: LF %s, RF %s, LB %s, RB %s",
            w_FL,
            w_FR,
            w_BL,
            w_BR,
        )

    def move_forward(self, intensity):
        """Move the vehicle forward."""
        for name in ["LF", "LB", "RF", "RB"]:
            self.move_motor(name, intensity)
        time.sleep(self.dt)
        logger.info("Vehicle moving forward on intensity %s", intensity)

    def move_backward(self, intensity):
        """Move the vehicle backward."""
        self.move_forward(-intensity)
        logger.info("Vehicle moving backward on intensity %s", intensity)

    def stop(self):
        """Stop all four wheels."""
        self.stop_all()
        logger.info("Vehicle stopped.")
