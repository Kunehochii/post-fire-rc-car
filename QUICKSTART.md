# Quick Start Guide - Post-Fire RC Car Project

## Step 1: Initial Setup (30 minutes)

### Hardware Assembly
1. Connect L298N motor driver to Raspberry Pi GPIO pins (see README.md wiring diagram)
2. Connect both DC motors to L298N outputs
3. Connect DHT11 sensor to GPIO4 with pull-up resistor
4. Connect ADS1115 ADC to I2C pins (GPIO2/3)
5. Connect MQ-2 sensor to ADS1115 Channel 0
6. Power Raspberry Pi and motors

### Software Installation
```bash
# Clone or navigate to project directory
cd ~/Post-Fire-RC-Car

# Install dependencies
sudo pip3 install -r requirements.txt

# Enable I2C interface
sudo raspi-config
# Navigate to: Interfacing Options > I2C > Yes > Finish > Reboot
```

---

## Step 2: Configuration (15 minutes)

### Update config.py
1. Open `config.py` in your editor
2. Add your **Blynk Auth Token**:
   ```python
   BLYNK_AUTH = "your_token_here"
   ```
3. Verify GPIO pins match your wiring
4. Save the file

### Create Blynk Account
1. Download Blynk IoT app
2. Create account at blynk.cloud
3. Create new project > Raspberry Pi
4. Copy auth token to config.py

---

## Step 3: Testing (20 minutes)

### Test Motors
```bash
python3 test_motors.py
# Watch for smooth motor operation in each direction
```

### Test Sensors
```bash
python3 test_sensors.py
# Verify DHT11 and MQ-2 readings
```

### Calibrate MQ-2
```bash
# Run in clean air - takes ~1.5 minutes
python3 calibrate_mq2.py
# Update config.py with baseline values
```

---

## Step 4: Run Main Application (5 minutes)

### Start the program
```bash
python3 main.py
```

Expected output:
```
Starting Post-Fire Building Inspection RC Car...
GPIO setup complete
Blynk connected. Ping: XX
Sensor Data - Temp: 25.3°C, Humidity: 45.2%, Gas: 150
```

### Control via Blynk App
1. Open Blynk app
2. Tap Play button (▶) to activate
3. Use joystick or buttons to control car
4. Monitor sensor readings in real-time

---

## Step 5: Deploy (Auto-start)

### Optional: Auto-start on Boot

Create systemd service:
```bash
sudo nano /etc/systemd/system/rc-car.service
```

Copy and paste:
```ini
[Unit]
Description=Post-Fire RC Car
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Post-Fire-RC-Car
ExecStart=/usr/bin/python3 main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rc-car.service
sudo systemctl start rc-car.service
sudo systemctl status rc-car.service
```

---

## File Reference

| File | Purpose |
|------|---------|
| `main.py` | Main application with motor control & Blynk integration |
| `config.py` | Configuration & settings (EDIT THIS FIRST) |
| `calibrate_mq2.py` | MQ-2 sensor calibration utility |
| `test_motors.py` | Motor testing & debugging |
| `test_sensors.py` | Sensor testing & debugging |
| `requirements.txt` | Python package dependencies |
| `README.md` | Detailed documentation |

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Motors don't move** | Check GPIO pins in config.py, verify power supply, run test_motors.py |
| **Blynk won't connect** | Verify WiFi, check auth token, ensure blynk.cloud is accessible |
| **DHT11 no reading** | Check GPIO4 connection, verify pull-up resistor, enable GPIO |
| **MQ-2 no reading** | Verify I2C with `i2cdetect -y 1`, check ADS1115 address 0x48 |
| **Permission denied** | Run with `sudo python3 main.py` or add user to gpio group |
| **Module not found** | Run `sudo pip3 install -r requirements.txt` |

---

## Blynk App Setup

### Required Virtual Pins to Create:

```
V0 - Label (Status)
V1 - Joystick (Movement)
V2 - Button Matrix (5 buttons: Stop, Fwd, Bwd, Left, Right)
V3 - Slider (Speed: 0-100%)
V4 - Label (Humidity %)
V5 - Label (Temperature °C)
V6 - Gauge (Gas Level: 0-100)
```

---

## Control Instructions

### Joystick Mode (V1)
- Move joystick forward/backward to move car
- Move left/right to turn
- Return to center to stop

### Button Mode (V2)
- Button 0: **STOP**
- Button 1: **FORWARD**
- Button 2: **BACKWARD**
- Button 3: **LEFT TURN**
- Button 4: **RIGHT TURN**

### Speed Control (V3)
- Slider from 0-100% for motor speed
- Lower speeds = more controlled movement
- Higher speeds = faster response

---

## Important Reminders

✓ Always test motors before deployment
✓ Calibrate MQ-2 in clean air
✓ Start with low speeds during testing
✓ Clear testing area of obstacles
✓ Check WiFi signal strength
✓ Monitor Raspberry Pi temperature
✓ Ensure adequate power supply (5V @ 2A minimum for Pi, 12V for motors)

---

## Next Steps

After successful testing:
1. Explore Blynk dashboard customization
2. Add camera integration (optional)
3. Implement autonomous navigation
4. Set up data logging
5. Optimize motor performance

---

## Support Resources

- Blynk Docs: https://docs.blynk.io/
- Raspberry Pi GPIO: https://pinout.xyz/
- Python Adafruit Libraries: https://github.com/adafruit/
- MQ-2 Sensor Info: https://www.sparkfun.com/products/9404
- L298N Motor Driver: https://www.mouser.com/ProductDetail/ST-Microelectronics/L298N/

---

**Good luck with your Post-Fire Building Inspection RC Car project!** 🚗🔥
