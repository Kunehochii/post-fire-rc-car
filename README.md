# Post-Fire Building Inspection RC Car
## Integration of MQ-2 & DHT11 Sensors with Raspberry Pi and Blynk Interface

---

## Project Overview

This project integrates a Raspberry Pi with an existing RC car to create an autonomous inspection robot capable of:
- **Remote Control**: Via Blynk app over WiFi
- **Environmental Monitoring**: Temperature and humidity using DHT11
- **Hazard Detection**: Smoke and gas detection using MQ-2 sensor
- **Real-time Data Visualization**: Live sensor readings on Blynk dashboard

---

## Hardware Requirements

### Main Components
- **Raspberry Pi 4 Model B** (4GB RAM recommended)
- **RC Car** (2WD or 4WD with separate left/right motor control)
- **L298N Motor Driver Module** (for controlling DC motors)
- **ADS1115** ADC Converter (for reading MQ-2 analog values)
- **DHT11 Sensor** (Temperature & Humidity)
- **MQ-2 Gas/Smoke Sensor**
- **5V Power Supply** (for Raspberry Pi)
- **12V Power Supply** (for motors)
- **WiFi connectivity** (built-in or USB adapter)

### Optional Components
- **Servo Motors** (for camera pan/tilt mount)
- **USB Camera** (for live video streaming)
- **Jumper Wires** (M-M and M-F)
- **Breadboard** (for connections)

---

## Wiring Diagram

### Motor Driver (L298N) to Raspberry Pi
```
L298N Pin          Raspberry Pi GPIO
IN1 (Left Fwd)   → GPIO17
IN2 (Left Bwd)   → GPIO27
IN3 (Right Fwd)  → GPIO23
IN4 (Right Bwd)  → GPIO24
ENA (Left Speed) → GPIO22 (PWM)
ENB (Right Speed)→ GPIO25 (PWM)
GND              → GND
+5V              → 5V
```

### Motor Connections
```
L298N Output → RC Car Motors
OUT1, OUT2   → Left Motor
OUT3, OUT4   → Right Motor
```

### DHT11 to Raspberry Pi
```
DHT11 Pin    Raspberry Pi GPIO
VCC          → 3.3V or 5V
GND          → GND
DATA         → GPIO4
```
*Add 10kΩ pull-up resistor between DATA and VCC*

### ADS1115 (I2C) to Raspberry Pi
```
ADS1115 Pin  Raspberry Pi GPIO
VDD          → 5V
GND          → GND
SCL          → GPIO3 (I2C SCL)
SDA          → GPIO2 (I2C SDA)
A0           → MQ-2 Signal
```

### MQ-2 Sensor to ADS1115
```
MQ-2 Pin        ADS1115 Connection
VCC             → VDD (5V)
GND             → GND
AO (Analog Out) → A0
DO (Digital Out)→ Optional: GPIO6
```

---

## Installation & Setup

### 1. Enable Raspberry Pi Interfaces

```bash
sudo raspi-config
# Enable: I2C, SPI, GPIO (if needed)
# Restart after enabling
```

### 2. Install Python Dependencies

```bash
cd ~/Post-Fire-RC-Car
sudo pip3 install -r requirements.txt
```

### 3. Configure Blynk

1. Download **Blynk IoT** app from App Store or Google Play
2. Create a new account at [blynk.cloud](https://blynk.cloud)
3. Create a new project with device type "Raspberry Pi"
4. Copy your **Auth Token**
5. Update `config.py` with your token:
   ```python
   BLYNK_AUTH = "your_auth_token_here"
   ```

### 4. Setup Blynk Dashboard

Create the following virtual pins in the Blynk app:

| Virtual Pin | Widget Type | Name | Range |
|------------|-------------|------|-------|
| V0 | Label | Status | - |
| V1 | Joystick | Movement Control | ±1 |
| V2 | Button Matrix | Car Controls | 0-4 |
| V3 | Slider | Speed Control | 0-100 |
| V4 | Label | Humidity | % |
| V5 | Label | Temperature | °C |
| V6 | Gauge | Gas Level | 0-100 |

### 5. Calibrate MQ-2 Sensor

Run calibration in clean air:
```bash
python3 calibrate_mq2.py
```

Update the baseline values in `config.py` based on calibration output.

---

## Configuration

Edit `config.py` to match your hardware setup:

### GPIO Pins
Adjust pin numbers based on your wiring:
```python
MOTOR_PINS = {
    'left_forward': 17,
    'left_backward': 27,
    'left_speed': 22,
    'right_forward': 23,
    'right_backward': 24,
    'right_speed': 25,
}
```

### Sensor Calibration
Update after running `calibrate_mq2.py`:
```python
MQ2_THRESHOLDS = {
    'clean_air': 150,      # Update with calibration value
    'warning': 200,
    'danger': 300,
}
```

### Motor Speeds
```python
MAX_MOTOR_SPEED = 100      # Maximum PWM (0-100)
MIN_MOTOR_SPEED = 30       # Minimum to move
TURN_SPEED = 70            # Turning speed
```

---

## Running the Project

### Manual Start
```bash
python3 main.py
```

### Auto-start on Boot (Optional)

Create systemd service:
```bash
sudo nano /etc/systemd/system/rc-car.service
```

Add:
```ini
[Unit]
Description=Post-Fire RC Car Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Post-Fire-RC-Car
ExecStart=/usr/bin/python3 main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable rc-car.service
sudo systemctl start rc-car.service
```

Check status:
```bash
sudo systemctl status rc-car.service
```

---

## Blynk App Controls

### Joystick (V1)
- Move joystick to control car direction
- Speed varies with joystick position

### Button Matrix (V2)
- Button 0: Stop
- Button 1: Move Forward
- Button 2: Move Backward
- Button 3: Turn Left
- Button 4: Turn Right

### Speed Slider (V3)
- Adjust motor speed (0-100%)

### Sensor Readings
- **V4**: Real-time Humidity (%)
- **V5**: Real-time Temperature (°C)
- **V6**: Gas/Smoke Level (0-100, Red alert if > 30)

---

## Troubleshooting

### "ModuleNotFoundError" Errors
```bash
# Reinstall dependencies
sudo pip3 install --upgrade -r requirements.txt
```

### Blynk Connection Issues
- Check WiFi connection: `ifconfig`
- Verify auth token in `config.py`
- Test connection: `ping blynk.cloud`

### Motors Not Moving
1. Check power supply connections
2. Verify GPIO pins in `config.py`
3. Test with: `python3 test_motors.py`

### Sensor Reading Issues
- **DHT11**: Enable GPIO access, check pull-up resistor
- **MQ-2**: Verify I2C connection (`i2cdetect -y 1`)
- Run calibration script

### Check I2C Connection
```bash
sudo i2cdetect -y 1
# Should show ADS1115 at address 0x48
```

### GPIO Permission Denied
```bash
sudo usermod -a -G gpio pi
# Log out and log back in
```

---

## File Structure

```
Post-Fire-RC-Car/
├── main.py                 # Main application
├── config.py              # Configuration file
├── calibrate_mq2.py       # MQ-2 calibration script
├── requirements.txt       # Python dependencies
├── test_motors.py         # Motor testing script
├── test_sensors.py        # Sensor testing script
└── README.md              # This file
```

---

## Testing Scripts

### Test Motors Only
```bash
python3 test_motors.py
```

### Test Sensors Only
```bash
python3 test_sensors.py
```

---

## Safety Considerations

1. **Power Supply**: Ensure adequate power for motors and Pi
2. **Motor Speed**: Start with lower speeds during testing
3. **Obstacles**: Clear the testing area of obstacles
4. **Thermal Limits**: Monitor MQ-2 sensor temperature
5. **WiFi Range**: Test Blynk connection range before deployment

---

## Performance Tuning

### Optimize Motor Response
```python
# Reduce update interval in main.py
MOTOR_UPDATE_INTERVAL = 0.05  # From 0.1
```

### Increase Sensor Accuracy
```python
# Average multiple readings
SENSOR_SAMPLE_COUNT = 5  # From 3
```

### WiFi Stability
- Place Raspberry Pi close to WiFi router
- Reduce interference (2.4GHz band crowded)
- Consider 5GHz WiFi if available

---

## Advanced Features (Coming Soon)

- [ ] Live camera streaming to Blynk
- [ ] GPS/GNSS integration for mapping
- [ ] Machine Learning for autonomous navigation
- [ ] Multi-robot coordination
- [ ] Data logging to cloud storage
- [ ] Custom alerts based on sensor thresholds

---

## Project Log

- **v1.0**: Initial release with motor control, DHT11, MQ-2, and Blynk integration
- **v1.1**: Added motor calibration and PWM speed control
- **v1.2**: Enhanced sensor filtering and error handling

---

## Support & Documentation

- **Blynk Documentation**: https://docs.blynk.io/
- **Raspberry Pi GPIO**: https://www.raspberrypi.com/documentation/
- **DHT11 Datasheet**: https://www.adafruit.com/product/386
- **MQ-2 Datasheet**: https://www.sparkfun.com/datasheets/Sensors/Biometric/MQ-2.pdf
- **L298N Guide**: https://www.electronicwings.com/raspberry-pi/l298n-motor-driver-module

---

## License

Open source - feel free to modify and distribute for your needs.

---

## Author Notes

This project was designed for post-fire building inspection. The MQ-2 sensor helps detect hazardous gases, while the temperature and humidity readings provide environmental context. Always prioritize safety and conduct thorough testing before deployment.
