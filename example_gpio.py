import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define motor control and enable pins for L298N-A
IN1_A = 17
IN2_A = 27  # Right Motor
ENA_A = 18  # PWM for L298N-A Motor A
IN3_A = 22
IN4_A = 23  # Left Motor
ENB_A = 19  # PWM for L298N-A Motor B

# Define motor control and enable pins for L298N-B
IN1_B = 24
IN2_B = 25  # Left Motor
ENA_B = 12  # PWM for L298N-B Motor A
IN3_B = 5
IN4_B = 6  # Right Motor
ENB_B = 13  # PWM for L298N-B Motor B. Reverse orientation

# Setup GPIO
all_pins = [
    IN1_A,
    IN2_A,
    ENA_A,
    IN3_A,
    IN4_A,
    ENB_A,
    IN1_B,
    IN2_B,
    ENA_B,
    IN3_B,
    IN4_B,
    ENB_B,
]
GPIO.setup(all_pins, GPIO.OUT)

# Initialize PWM for each enable pin
pwm_ENA_A = GPIO.PWM(ENA_A, 1000)
pwm_ENB_A = GPIO.PWM(ENB_A, 1000)
pwm_ENA_B = GPIO.PWM(ENA_B, 1000)
pwm_ENB_B = GPIO.PWM(ENB_B, 1000)

pwm_ENA_A.start(0)
pwm_ENB_A.start(0)
pwm_ENA_B.start(0)
pwm_ENB_B.start(0)

# Example: Set each motor to run at different speeds
pwm_ENA_A.ChangeDutyCycle(75)  # Motor A on L298N-A at 25%
pwm_ENB_A.ChangeDutyCycle(75)  # Motor B on L298N-A at 50%
pwm_ENA_B.ChangeDutyCycle(75)  # Motor A on L298N-B at 75%
pwm_ENB_B.ChangeDutyCycle(75)  # Motor B on L298N-B at 100%

# Set directions (example)
GPIO.output([IN1_A, IN3_A, IN1_B, IN3_B], GPIO.HIGH)
GPIO.output([IN2_A, IN4_A, IN2_B, IN4_B], GPIO.LOW)

time.sleep(1)  # Motors run for 2 seconds

# Cleanup
pwm_ENA_A.stop()
pwm_ENB_A.stop()
pwm_ENA_B.stop()
pwm_ENB_B.stop()
GPIO.cleanup()
