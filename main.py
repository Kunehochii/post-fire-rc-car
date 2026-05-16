"""
Post-Fire Building Inspection RC Car
Integration of MQ-2 & DHT11 Sensors with Raspberry Pi and Blynk Interface
"""

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import board
import busio
import serial
import threading
from blynk_lib import Blynk
from Adafruit_ADS1x15 import ADS1115
from config import BLYNK_AUTH, MQ2_PIN, DHT_PIN, MOTOR_PINS, SERVO_PINS

# =====================
# Global Variables
# =====================
pwm_left = None
pwm_right = None
current_speed = 100
blynk = None
ads = None
arduino_serial = None
running = True
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor pins (L298N Motor Driver)
MOTOR_LEFT_FORWARD = MOTOR_PINS['left_forward']
MOTOR_LEFT_BACKWARD = MOTOR_PINS['left_backward']
MOTOR_RIGHT_FORWARD = MOTOR_PINS['right_forward']
MOTOR_RIGHT_BACKWARD = MOTOR_PINS['right_backward']
MOTOR_LEFT_SPEED = MOTOR_PINS['left_speed']
MOTOR_RIGHT_SPEED = MOTOR_PINS['right_speed']

# Servo pins for camera/sensor mount
SERVO_HORIZONTAL = SERVO_PINS['horizontal']
SERVO_VERTICAL = SERVO_PINS['vertical']

# Sensor pins
MQ2_ANALOG_PIN = MQ2_PIN['analog']
DHT_SENSOR_PIN = DHT_PIN['pin']
DHT_SENSOR_TYPE = DHT_PIN['type']  # 11 for DHT11

# =====================
# Setup GPIO
# =====================
def setup_gpio():
    """Initialize all GPIO pins"""
    global pwm_left, pwm_right
    
    motor_pins = [MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, 
                  MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD]
    
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)
    
    # PWM for speed control
    pwm_left = GPIO.PWM(MOTOR_LEFT_SPEED, 1000)  # 1kHz frequency
    pwm_right = GPIO.PWM(MOTOR_RIGHT_SPEED, 1000)
    pwm_left.start(0)
    pwm_right.start(0)
    
    print("GPIO setup complete")


# =====================
# Blynk & ADC Initialization
# =====================
try:
    blynk = Blynk(BLYNK_AUTH)
    print("Blynk object created")
except Exception as e:
    print(f"Warning: Blynk initialization failed: {e}")
    blynk = None

try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS1115(i2c)
    print("ADS1115 ADC initialized")
except Exception as e:
    print(f"Warning: ADS1115 ADC initialization failed: {e}")
    ads = None


# =====================
# Arduino Serial Communication
# =====================
def setup_serial():
    """Initialize serial connection to Arduino via USB"""
    global arduino_serial
    try:
        # Try common Arduino serial ports
        ports_to_try = ['/dev/ttyUSB0', '/dev/ttyACM0', '/dev/ttyUSB1', '/dev/ttyACM1']
        
        for port in ports_to_try:
            try:
                arduino_serial = serial.Serial(port, 9600, timeout=1)
                time.sleep(2)  # Wait for Arduino to initialize
                print(f"✓ Connected to Arduino on {port}")
                
                # Wait for Arduino ready signal
                for _ in range(10):
                    if arduino_serial.in_waiting:
                        msg = arduino_serial.readline().decode('utf-8', errors='ignore').strip()
                        print(f"Arduino startup: {msg}")
                        if "ARDUINO_READY" in msg:
                            break
                    time.sleep(0.2)
                
                return True
            except Exception as e:
                continue
        
        print("⚠ Warning: Could not connect to Arduino on any port")
        return False
    
    except Exception as e:
        print(f"Error setting up serial: {e}")
        return False


def read_arduino():
    """Read messages from Arduino in a separate thread"""
    global arduino_serial, running
    
    while running:
        try:
            if arduino_serial and arduino_serial.is_open and arduino_serial.in_waiting:
                message = arduino_serial.readline().decode('utf-8', errors='ignore').strip()
                
                if message:
                    print(f"[Arduino] {message}")
                    
                    # Parse and handle Arduino commands
                    if "ACTION:FWD" in message:
                        move_forward(current_speed)
                    elif "ACTION:REV" in message:
                        move_backward(current_speed)
                    elif "ACTION:LEFT" in message:
                        turn_left(current_speed)
                    elif "ACTION:RIGHT" in message:
                        turn_right(current_speed)
                    elif "ACTION:STOP" in message:
                        stop_car()
                    elif "ACTION:CENTER" in message:
                        pass  # Center steering (handled by Arduino)
                    elif "FORWARD AT VALUE:" in message or "New Reverse Ceiling:" in message:
                        # Just log calibration messages
                        pass
            
            time.sleep(0.05)
        
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            time.sleep(1)


# =====================
# Motor Control Functions
# =====================
def stop_car():
    """Stop all motors"""
    if pwm_left is None or pwm_right is None:
        return
    
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)


def move_forward(speed=100):
    """Move car forward"""
    if pwm_left is None or pwm_right is None:
        print("Motors not initialized")
        return
    
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def move_backward(speed=100):
    """Move car backward"""
    if pwm_left is None or pwm_right is None:
        print("Motors not initialized")
        return
    
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def turn_left(speed=100):
    """Turn car left"""
    if pwm_left is None or pwm_right is None:
        print("Motors not initialized")
        return
    
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def turn_right(speed=100):
    """Turn car right"""
    if pwm_left is None or pwm_right is None:
        print("Motors not initialized")
        return
    
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


# =====================
# Sensor Reading Functions
# =====================
def read_mq2_sensor():
    """
    Read MQ-2 sensor (Gas/Smoke sensor)
    Returns analog value (0-4095 for 12-bit ADC)
    Note: Requires ADS1115 ADC converter connected via I2C
    """
    global ads
    try:
        if ads is None:
            return None
        
        # Channel 0 for MQ-2 (0-3 for ADS1115)
        value = ads.read_adc(MQ2_PIN['analog'], gain=1)
        return value
    except Exception as e:
        print(f"Error reading MQ-2: {e}")
        return None


def read_dht11_sensor():
    """
    Read DHT11 sensor
    Returns tuple of (humidity, temperature)
    """
    try:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR_TYPE, DHT_SENSOR_PIN)
        
        if humidity is not None and temperature is not None:
            return humidity, temperature
        else:
            print("Failed to read DHT11 sensor")
            return None, None
    except Exception as e:
        print(f"Error reading DHT11: {e}")
        return None, None


# =====================
# Blynk Virtual Pin Handlers
# =====================
@blynk.on("connected")
def blynk_connected(ping):
    """Called when Blynk connects"""
    print(f"Blynk connected. Ping: {ping}")
    blynk.virtual_write(0, "Blynk Connected")


@blynk.on("V1")
def on_joystick(value):
    """
    Virtual Pin V1 - Joystick Control
    Value format: "x:y" where x,y are -1 to 1
    """
    try:
        x, y = map(float, value.split(':'))
        
        # Determine movement based on joystick position
        if y > 0.3:  # Forward
            move_forward(int(y * 100))
        elif y < -0.3:  # Backward
            move_backward(int(abs(y) * 100))
        elif x > 0.3:  # Right
            turn_right(int(x * 100))
        elif x < -0.3:  # Left
            turn_left(int(abs(x) * 100))
        else:
            stop_car()
    except Exception as e:
        print(f"Error in joystick handler: {e}")


@blynk.on("V2")
def on_car_control(value):
    """
    Virtual Pin V2 - Button Control
    0=Stop, 1=Forward, 2=Backward, 3=Left, 4=Right
    """
    try:
        command = int(value[0])
        
        if command == 0:
            stop_car()
        elif command == 1:
            move_forward()
        elif command == 2:
            move_backward()
        elif command == 3:
            turn_left()
        elif command == 4:
            turn_right()
    except Exception as e:
        print(f"Error in car control handler: {e}")


@blynk.on("V3")
def on_speed_slider(value):
    """Virtual Pin V3 - Speed Control (0-100)"""
    global current_speed
    try:
        current_speed = int(value[0])
    except Exception as e:
        print(f"Error in speed control: {e}")


# =====================
# Data Publishing to Blynk
# =====================
def publish_sensor_data():
    """Publish sensor data to Blynk virtual pins"""
    try:
        # Read sensors
        humidity, temperature = read_dht11_sensor()
        mq2_value = read_mq2_sensor()
        
        # Publish to Blynk
        if humidity is not None:
            blynk.virtual_write(4, f"{humidity:.1f}%")  # V4 - Humidity
        
        if temperature is not None:
            blynk.virtual_write(5, f"{temperature:.1f}°C")  # V5 - Temperature
        
        if mq2_value is not None:
            # Normalize MQ-2 reading (assuming 12-bit ADC: 0-4095)
            mq2_ppm = (mq2_value / 4095.0) * 100  # Scale to 0-100
            blynk.virtual_write(6, f"{mq2_ppm:.1f}")  # V6 - Gas Level
            
            # Alert if gas detected (threshold can be adjusted)
            if mq2_ppm > 30:
                blynk.set_property(6, "color", "#FF0000")  # Red alert
            else:
                blynk.set_property(6, "color", "#00FF00")  # Green safe
        
        print(f"Sensor Data - Temp: {temperature}°C, Humidity: {humidity}%, Gas: {mq2_value}")
        
    except Exception as e:
        print(f"Error publishing sensor data: {e}")


# =====================
# Main Loop
# =====================
def main():
    """Main program loop"""
    global running, arduino_serial
    
    try:
        print("Starting Post-Fire Building Inspection RC Car...")
        
        # Initialize GPIO
        setup_gpio()
        
        # Setup serial connection to Arduino
        setup_serial()
        
        # Start Arduino reader thread
        if arduino_serial is not None:
            arduino_thread = threading.Thread(target=read_arduino, daemon=True)
            arduino_thread.start()
            print("Arduino reader thread started")
        
        # Connect to Blynk if available
        if blynk is not None:
            blynk.connect()
        else:
            print("Warning: Blynk not available, running in local mode only")
        
        # Main loop
        sensor_read_interval = 2  # Read sensors every 2 seconds
        last_sensor_read = time.time()
        
        while True:
            # Handle Blynk connection
            if blynk is not None and blynk.is_connected():
                blynk.run()
                
                # Publish sensor data at interval
                current_time = time.time()
                if current_time - last_sensor_read >= sensor_read_interval:
                    publish_sensor_data()
                    last_sensor_read = current_time
            else:
                if blynk is not None:
                    print("Attempting to reconnect to Blynk...")
                    blynk.connect()
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    except Exception as e:
        print(f"Error in main loop: {e}")
    
    finally:
        running = False
        stop_car()
        
        # Close serial connection
        if arduino_serial is not None:
            try:
                arduino_serial.close()
                print("Serial connection closed")
            except:
                pass
        
        GPIO.cleanup()
        if blynk is not None and blynk.is_connected():
            blynk.disconnect()
        print("Cleanup complete")


# =====================
# Entry Point
# =====================
if __name__ == "__main__":
    main()
