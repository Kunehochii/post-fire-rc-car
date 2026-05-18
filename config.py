"""
Configuration file for Post-Fire Building Inspection RC Car
Update these settings based on your hardware setup
"""

# =====================
# Blynk Configuration
# =====================
# Get your auth token from the Blynk app (more.blynk.cloud)
BLYNK_AUTH = "Yci2voznzgg1oYSjZOrV0hwvMYBoSk0p"
BLYNK_SERVER = "blynk.cloud"
BLYNK_PORT = 443

# =====================
# GPIO Pin Configuration (BCM numbering)
# =====================
# Motor Control Pins (L298N Motor Driver)
MOTOR_PINS = {
    'left_forward': 17,      # GPIO17
    'left_backward': 27,     # GPIO27
    'left_speed': 22,        # GPIO22 (PWM for speed control)
    'right_forward': 23,     # GPIO23
    'right_backward': 24,    # GPIO24
    'right_speed': 25,       # GPIO25 (PWM for speed control)
}

# MQ-2 Sensor Configuration
# Note: MQ-2 is an analog sensor - requires ADC converter (ADS1115 or MCP3008)
MQ2_PIN = {
    'analog': 0,             # ADC Channel 0 (for ADS1115 via I2C)
    'do_pin': 6,             # GPIO6 - Digital output (optional, for threshold detection)
}

# DHT22 Sensor Configuration
DHT_PIN = {
    'pin': 4,                # GPIO4 (single wire)
    'type': 22,              # 11 for DHT11, 22 for DHT22
}

# Servo Pins (for camera/sensor mount - optional)
SERVO_PINS = {
    'horizontal': 13,        # GPIO13 (PWM)
    'vertical': 26,          # GPIO26 (PWM)
}

# =====================
# Blynk Virtual Pin Mapping
# =====================
BLYNK_VIRTUAL_PINS = {
    'status': 0,             # V0 - Status messages
    'joystick': 1,           # V1 - Joystick control
    'buttons': 2,            # V2 - Button controls
    'speed': 3,              # V3 - Speed slider
    'humidity': 4,           # V4 - DHT22 Humidity
    'temperature': 5,        # V5 - DHT22 Temperature
    'gas_level': 6,          # V6 - MQ-2 Gas/Smoke level
}

# =====================
# Sensor Calibration & Thresholds
# =====================
# MQ-2 Sensor Thresholds (adjust based on calibration)
MQ2_THRESHOLDS = {
    'clean_air': 50,         # ADC value for clean air (baseline)
    'warning': 100,          # Alert threshold
    'danger': 200,           # Danger threshold
}

# DHT22 Temperature Thresholds
TEMPERATURE_THRESHOLDS = {
    'min_safe': 0,           # Minimum safe temperature
    'max_safe': 60,          # Maximum safe temperature (°C)
}

# =====================
# Motor Speed Configuration
# =====================
MAX_MOTOR_SPEED = 100       # 0-100 percentage
MIN_MOTOR_SPEED = 30        # Minimum speed to move
TURN_SPEED = 70             # Speed for turning

# =====================
# Sampling Configuration
# =====================
SENSOR_SAMPLE_INTERVAL = 2  # Read sensors every N seconds
SENSOR_SAMPLE_COUNT = 3     # Number of samples for averaging
MOTOR_UPDATE_INTERVAL = 0.1 # Motor control update interval (seconds)

# =====================
# I2C Configuration (for ADS1115 ADC)
# =====================
ADS1115_ADDRESS = 0x48      # Default I2C address for ADS1115
I2C_BUS = 1                 # Raspberry Pi I2C bus (usually 1)

# =====================
# Debug Mode
# =====================
DEBUG = True                # Enable debug prints
