import RPi.GPIO as GPIO

class DriveTrain:
    def __init__(self, wheelbase: float, track: float, wheels_orientation: list = [True, True, True, True], threshold = [0, 0, 0, 0]):
        self.wheelbase = wheelbase
        self.track = track
        self.IN1_FRONT = 17
        self.IN2_FRONT = 27
        self.IN3_FRONT = 22
        self.IN4_FRONT = 23
        self.IN1_BACK = 24
        self.IN2_BACK = 25
        self.IN3_BACK = 5
        self.IN4_BACK = 6
        self.EN_R_FRONT = 18
        self.EN_L_FRONT = 19
        self.EN_L_BACK = 12
        self.EN_R_BACK = 13
        self.wheels_orientation = wheels_orientation
        self.threshold = threshold
        self.wheel_config = {}
        self.wheel_state = {""}
        self.config_pins()
        self.config_wheels()
    
    def config_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.IN1_FRONT, self.IN2_FRONT, self.IN3_FRONT, self.IN4_FRONT, self.IN1_BACK, self.IN2_BACK, self.IN3_BACK, self.IN4_BACK], GPIO.OUT)
        GPIO.setup([self.EN_R_FRONT, self.EN_L_FRONT, self.EN_L_BACK, self.EN_R_BACK], GPIO.OUT)
        self.pwm_EN_R_FRONT = GPIO.PWM(self.EN_R_FRONT, 1000)
        self.pwm_EN_L_FRONT = GPIO.PWM(self.EN_L_FRONT, 1000)
        self.pwm_EN_L_BACK = GPIO.PWM(self.EN_L_BACK, 1000)
        self.pwm_EN_R_BACK = GPIO.PWM(self.EN_R_BACK, 1000)
        self.pwm_EN_R_FRONT.start(0)
        self.pwm_EN_L_FRONT.start(0)
        self.pwm_EN_L_BACK.start(0)
        self.pwm_EN_R_BACK.start(0)
    
    def config_wheels(self):
        """Configures the wheels orientation. The wheels_orientation list should be in the following order: [LF, RF, LB, RB]. True means forward, False means backward.
        
        The threshold list is used to adjust the PWM signal. For example, if threshold LF set to 30, the linear coorelation will be reevaluated based on the interception of 30.
        :param threshold: Adjust the scale of the PWM signal, defaults to [0, 0, 0, 0]. The values should be between 0 and 100.
        :type threshold: list, optional
        """
        if any([i < 0 or i > 100 for i in self.threshold]):
            raise ValueError("Threshold values should be between 0 and 100")
        self.wheel_config = {
            self.IN1_FRONT: GPIO.HIGH if self.wheels_orientation[0] else GPIO.LOW,
            self.IN2_FRONT: GPIO.LOW if self.wheels_orientation[0] else GPIO.HIGH,
            self.IN3_FRONT: GPIO.HIGH if self.wheels_orientation[1] else GPIO.LOW,
            self.IN4_FRONT: GPIO.LOW if self.wheels_orientation[1] else GPIO.HIGH,
            self.IN1_BACK: GPIO.HIGH if self.wheels_orientation[2] else GPIO.LOW,
            self.IN2_BACK: GPIO.LOW if self.wheels_orientation[2] else GPIO.HIGH,
            self.IN3_BACK: GPIO.HIGH if self.wheels_orientation[3] else GPIO.LOW,
            self.IN4_BACK: GPIO.LOW if self.wheels_orientation[3] else GPIO.HIGH
        }
    
    def move(self, LF: float, RF: float, LB: float, RB: float):
        """Moves the robot according to the given speeds for each wheel. If a negative value is given, the wheel will move in reverse. 
        :param LF: Speed for the left front wheel (0-100)
        :type LF: float
        :param RF: Speed for the right front wheel(0-100)
        :type RF: float
        :param LB: Speed for the left back wheel(0-100)
        :type LB: float
        :param RB: Speed for the right back wheel(0-100)
        :type RB: float
        """
        all_speeds = [LF, RF, LB, RB]
        if 
        
        
        
        
        
    
    