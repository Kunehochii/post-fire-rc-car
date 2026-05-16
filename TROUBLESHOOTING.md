# Troubleshooting & Debugging Guide

## Quick Diagnostics

### Check Raspberry Pi System
```bash
# Check OS and Python version
uname -a
python3 --version

# Check available memory
free -h

# Check disk space
df -h

# Check temperature
vcgencmd measure_temp
```

---

## Motor Issues

### Motors Don't Move at All

**1. Check Power Supply**
```bash
# Verify 12V motor supply is connected and working
# Use multimeter to check voltage at L298N motor pins
```

**2. Verify GPIO Configuration**
```bash
# Check GPIO pins in config.py match your wiring
# Run motor test
python3 test_motors.py

# If this doesn't work, check GPIO access
gpio readall  # If available, shows GPIO status
```

**3. Test Individual Motor Pins**
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
# If motor responds, GPIO is working
```

### Motors Spin but Car Doesn't Move

**Check mechanical issues:**
- Wheels not making contact with ground
- Motor shaft not connected to wheels
- Gearbox issue
- Friction too high

**Test motor direction:**
```bash
python3 test_motors.py
# Verify motors spin in expected directions
```

### Uneven Movement (One Motor Faster)

**Motor speed balancing:**
```python
# In main.py or calibration script:
pwm_left.ChangeDutyCycle(100)
pwm_right.ChangeDutyCycle(100)
# Watch if one motor is faster

# Adjust in config.py:
# Reduce the faster motor's speed value
```

---

## Sensor Issues

### DHT11 - No Reading

**1. Check Connection**
```bash
# Verify GPIO4 is used and not occupied
# Ensure 10kΩ pull-up resistor between DATA and VCC
```

**2. Enable GPIO Interface**
```bash
sudo raspi-config
# Interface Options > GPIO > Yes > Reboot
```

**3. Test DHT11 Directly**
```bash
cd ~/Adafruit_Python_DHT/examples
python3 AdafruitDHT.py 11 4  # 11=DHT11, 4=GPIO4
```

**4. Check Sensor is Functional**
- Replace with new DHT11 sensor
- Try different GPIO pin (update config.py)

### DHT11 - Intermittent Readings

**Solutions:**
```python
# Add retry logic in main.py
for attempt in range(3):
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    if humidity is not None:
        break
    time.sleep(1)
```

---

## MQ-2 Sensor Issues

### No MQ-2 Reading

**1. Check I2C Connection**
```bash
# List I2C devices
i2cdetect -y 1

# Should show:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# 40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --  <- 0x48 is ADS1115
```

**2. Enable I2C Interface**
```bash
sudo raspi-config
# Interface Options > I2C > Yes > Reboot
```

**3. Check ADS1115 Wiring**
- VDD → 5V
- GND → GND
- SCL → GPIO3
- SDA → GPIO2

**4. Test I2C Connection**
```bash
sudo apt-get install i2c-tools
i2cdetect -y 1
# Should show device at 0x48
```

**5. Verify MQ-2 Sensor Connection**
- Signal wire → ADS1115 Channel 0 (A0)
- Ensure MQ-2 is powered (5V supply working)
- Warm up MQ-2 for 1-2 minutes

### MQ-2 - Readings Not Changing

**Solutions:**
1. Run calibration: `python3 calibrate_mq2.py`
2. Check sensor hasn't exceeded lifespan (~3-5 years)
3. Verify power supply to MQ-2
4. Test with known gas source (lighter, alcohol)

---

## Blynk Connection Issues

### Blynk Won't Connect

**1. Check WiFi**
```bash
# Verify WiFi connection
nmcli device wifi list
nmcli connection show

# Connect to WiFi if not connected
sudo nmtui
```

**2. Verify Auth Token**
```bash
# Check config.py
grep BLYNK_AUTH config.py

# Should show your 32-character token
# Not "YOUR_BLYNK_AUTH_TOKEN_HERE"
```

**3. Check Firewall**
```bash
# Verify Blynk server is accessible
ping blynk.cloud
curl -I https://blynk.cloud
```

**4. Test Blynk Connection Manually**
```python
from blynk_lib import Blynk
from config import BLYNK_AUTH

blynk = Blynk(BLYNK_AUTH)
blynk.connect()
print(blynk.is_connected())
```

### Blynk Connection Drops Frequently

**Solutions:**
1. Improve WiFi signal strength
2. Reduce interference (microwave, other devices)
3. Try 2.4GHz instead of 5GHz WiFi
4. Add automatic reconnection:
```python
while not blynk.is_connected():
    print("Reconnecting...")
    blynk.connect()
    time.sleep(5)
```

### App Shows "Device Offline"

1. Check Raspberry Pi is running main.py
2. Verify Blynk service status on app
3. Try unplugging and replugging USB power
4. Check system logs: `journalctl -u rc-car.service`

---

## GPIO Permission Issues

### "RuntimeError: No access to /dev/mem"

```bash
# Run as root
sudo python3 main.py

# OR add user to GPIO group
sudo usermod -a -G gpio pi
# Log out and log back in
newgrp gpio
```

### "GPIO.setup() permission denied"

```bash
# Ensure GPIO interface is enabled
sudo raspi-config
# Interface Options > GPIO > Yes

# Reboot after enabling
sudo reboot
```

---

## I2C Issues

### I2C Bus Not Found

```bash
# Enable I2C
sudo raspi-config
# Interfacing Options > I2C > Yes > Finish > Reboot

# Verify after reboot
ls /dev/i2c*
# Should show /dev/i2c-1
```

### I2C Device Not Detected

```bash
# Check I2C bus
i2cdetect -y 1

# Troubleshoot:
# 1. Verify SDA (GPIO2) and SCL (GPIO3) connections
# 2. Add pull-up resistors (4.7kΩ) if not built-in
# 3. Check power supply voltage (should be 3.3V or 5V)
# 4. Try different I2C address if configurable
```

---

## Application Crashes

### Syntax Errors

```bash
# Check for Python syntax errors
python3 -m py_compile main.py
python3 -m py_compile config.py

# Run with verbose output
python3 -u main.py  # Unbuffered output
```

### Memory Issues

```bash
# Check available RAM
free -h

# Monitor during execution
watch -n 1 free -h

# Kill other processes if needed
ps aux | grep -i python
kill -9 <process_id>
```

### Resource Exhaustion

```bash
# Check CPU usage
top

# Check disk space
df -h
# If < 10% free, clean up old files
```

---

## Performance Issues

### Car Response Lag

**Solutions:**
1. Reduce Blynk ping interval
2. Optimize sensor read interval
3. Move closer to WiFi router
4. Reduce number of Blynk virtual pins being read

### High CPU Usage

```bash
# Check what's consuming CPU
top
ps aux --sort=-%cpu

# Profile if needed
python3 -m cProfile -s cumulative main.py
```

---

## Logging & Debugging

### Enable Debug Mode

```python
# In config.py
DEBUG = True

# In main.py, add prints:
if DEBUG:
    print(f"Motor command: {direction} @ {speed}%")
```

### View System Logs

```bash
# For systemd service
sudo journalctl -u rc-car.service -n 50  # Last 50 lines
sudo journalctl -u rc-car.service -f     # Follow logs

# Check for errors
sudo journalctl -u rc-car.service | grep -i error
```

### Create Log File

```python
# Add to main.py
import logging

logging.basicConfig(
    filename='rc_car.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Application started")
```

---

## Hardware Testing

### Test Power Supply
```bash
# Verify voltages with multimeter
# Raspberry Pi: 5V on power pins
# Motor driver: 12V supply
# Sensors: Correct voltage (3.3V or 5V)
```

### Test GPIO Pins
```python
# Test each GPIO pin
for pin in [17, 27, 22, 23, 24, 25]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)
    print(f"Tested GPIO{pin}")
```

### Test I2C Bus
```bash
# Generate I2C traffic to test connection
i2cget -y 1 0x48 0x00  # Read from ADS1115
```

---

## Contact & Support

### When Seeking Help, Provide:

1. Error message (full traceback)
2. Output of `uname -a`
3. Python version (`python3 --version`)
4. Wiring diagram/photo
5. Recent config.py changes
6. Log files

### Resources:

- **Blynk Community**: https://community.blynk.cc/
- **Raspberry Pi Forums**: https://www.raspberrypi.org/forums/
- **GPIO Reference**: https://pinout.xyz/
- **I2C Tools**: https://i2c.wiki.kernel.org/

---

## Emergency Shutdown

```bash
# If car is out of control
sudo pkill -f "python3 main.py"

# Force stop systemd service
sudo systemctl stop rc-car.service

# Cut power if necessary (last resort)
```

---

**Still having issues? Create a GitHub issue or post on Blynk community with the information from "When Seeking Help" section above.**
