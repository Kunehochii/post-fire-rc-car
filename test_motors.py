"""
Motor Testing Script
Test individual motors and motor driver functionality
"""

import RPi.GPIO as GPIO
import time
from config import MOTOR_PINS

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MOTOR_LEFT_FORWARD = MOTOR_PINS['left_forward']
MOTOR_LEFT_BACKWARD = MOTOR_PINS['left_backward']
MOTOR_RIGHT_FORWARD = MOTOR_PINS['right_forward']
MOTOR_RIGHT_BACKWARD = MOTOR_PINS['right_backward']
MOTOR_LEFT_SPEED = MOTOR_PINS['left_speed']
MOTOR_RIGHT_SPEED = MOTOR_PINS['right_speed']

def setup_motors():
    """Initialize motor pins"""
    motor_pins = [MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, 
                  MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD]
    
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)
    
    # PWM setup
    global pwm_left, pwm_right
    pwm_left = GPIO.PWM(MOTOR_LEFT_SPEED, 1000)
    pwm_right = GPIO.PWM(MOTOR_RIGHT_SPEED, 1000)
    pwm_left.start(0)
    pwm_right.start(0)


def stop():
    """Stop all motors"""
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)


def test_left_motor_forward():
    """Test left motor forward"""
    print("Testing LEFT MOTOR - FORWARD (5 seconds @ 100%)")
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(100)
    time.sleep(5)
    stop()


def test_left_motor_backward():
    """Test left motor backward"""
    print("Testing LEFT MOTOR - BACKWARD (5 seconds @ 100%)")
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(100)
    time.sleep(5)
    stop()


def test_right_motor_forward():
    """Test right motor forward"""
    print("Testing RIGHT MOTOR - FORWARD (5 seconds @ 100%)")
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_right.ChangeDutyCycle(100)
    time.sleep(5)
    stop()


def test_right_motor_backward():
    """Test right motor backward"""
    print("Testing RIGHT MOTOR - BACKWARD (5 seconds @ 100%)")
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
    pwm_right.ChangeDutyCycle(100)
    time.sleep(5)
    stop()


def test_speed_control():
    """Test motor speed control"""
    print("Testing SPEED CONTROL - Both motors")
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    
    for speed in [30, 50, 70, 100]:
        print(f"  Speed: {speed}% - 2 seconds")
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(speed)
        time.sleep(2)
    
    stop()


def test_all():
    """Run all motor tests"""
    print("=" * 50)
    print("MOTOR TESTING SCRIPT")
    print("=" * 50)
    
    try:
        setup_motors()
        print("GPIO initialized successfully\n")
        
        tests = [
            test_left_motor_forward,
            test_left_motor_backward,
            test_right_motor_forward,
            test_right_motor_backward,
            test_speed_control,
        ]
        
        for test in tests:
            print(f"\n{test.__doc__}")
            test()
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        print("=" * 50)
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        stop()
        GPIO.cleanup()
        print("GPIO cleanup complete")


if __name__ == "__main__":
    try:
        test_all()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        GPIO.cleanup()
