"""
Sensor Testing Script
Test DHT11 and MQ-2 sensor functionality
"""

import time
import adafruit_dht
import board
import busio
from config import DHT_PIN, MQ2_PIN

DHT_SENSOR_PIN = DHT_PIN['pin']
DHT_SENSOR_TYPE = DHT_PIN['type']
MQ2_CHANNEL = MQ2_PIN['analog']


def test_dht11():
    """Test DHT11 sensor"""
    print("Testing DHT11 Sensor...")
    print("-" * 50)
    
    try:
        print("Reading DHT11 (this may take a few seconds)...")
        dht_pin = _get_board_pin(DHT_SENSOR_PIN)
        if DHT_SENSOR_TYPE == 11:
            dht_device = adafruit_dht.DHT11(dht_pin, use_pulseio=False)
        elif DHT_SENSOR_TYPE == 22:
            dht_device = adafruit_dht.DHT22(dht_pin, use_pulseio=False)
        else:
            raise ValueError(f"Unsupported DHT sensor type: {DHT_SENSOR_TYPE}")

        try:
            for attempt in range(5):
                try:
                    temperature = dht_device.temperature
                    humidity = dht_device.humidity
                except RuntimeError:
                    temperature = None
                    humidity = None

                if humidity is not None and temperature is not None:
                    print(f"\nAttempt {attempt + 1}:")
                    print(f"  Temperature: {temperature:.1f}°C")
                    print(f"  Humidity: {humidity:.1f}%")
                else:
                    print(f"\nAttempt {attempt + 1}: Failed to read sensor")

                if attempt < 4:
                    time.sleep(2)
        finally:
            dht_device.exit()

        print("\n✓ DHT11 test completed")
        return True
    
    except Exception as e:
        print(f"\n✗ DHT11 Error: {e}")
        return False


def _get_board_pin(bcm_pin):
    try:
        return getattr(board, f"D{bcm_pin}")
    except AttributeError as e:
        raise ValueError(f"Unsupported BCM pin for Blinka: {bcm_pin}") from e


def test_mq2():
    """Test MQ-2 sensor via ADS1115"""
    print("\n\nTesting MQ-2 Sensor (via ADS1115 ADC)...")
    print("-" * 50)
    
    try:
        print("Initializing I2C and ADS1115...")
        i2c = busio.I2C(board.SCL, board.SDA)
        
        from Adafruit_ADS1x15 import ADS1115
        ads = ADS1115(i2c)
        
        print("Reading MQ-2 values (10 readings)...\n")
        
        readings = []
        for i in range(10):
            value = ads.read_adc(MQ2_CHANNEL, gain=1)
            readings.append(value)
            print(f"  Reading {i+1:2d}: ADC = {value:4d}")
            time.sleep(0.5)
        
        avg_value = sum(readings) // len(readings)
        min_value = min(readings)
        max_value = max(readings)
        
        print(f"\nStatistics:")
        print(f"  Average: {avg_value}")
        print(f"  Minimum: {min_value}")
        print(f"  Maximum: {max_value}")
        print(f"  Variance: {max_value - min_value}")
        
        print("\n✓ MQ-2 test completed")
        return True
    
    except Exception as e:
        print(f"\n✗ MQ-2 Error: {e}")
        print("\nTroubleshooting:")
        print("  - Ensure I2C is enabled: raspi-config")
        print("  - Verify ADS1115 is connected to I2C pins (GPIO2/GPIO3)")
        print("  - Check I2C address: i2cdetect -y 1")
        print("  - Verify MQ-2 is connected to ADS1115 Channel 0")
        return False


def test_i2c_devices():
    """Check I2C devices on the bus"""
    print("\n\nScanning I2C Devices...")
    print("-" * 50)
    
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        print("I2C bus initialized successfully")
        
        # Try to find devices
        print("\nSearching for I2C devices...")
        try:
            # Try to read from common I2C addresses
            for addr in [0x48, 0x49, 0x4A, 0x4B]:  # ADS1115 addresses
                try:
                    result = i2c.readfrom(addr, 1)
                    print(f"  Found device at address 0x{addr:02X}")
                except:
                    pass
        except:
            print("  Note: Basic device scanning may be limited")
        
        i2c.deinit()
        return True
    
    except Exception as e:
        print(f"Error initializing I2C: {e}")
        return False


def main():
    """Run all sensor tests"""
    print("=" * 50)
    print("SENSOR TESTING SCRIPT")
    print("=" * 50)
    
    results = {}
    
    # Test I2C first
    results['I2C'] = test_i2c_devices()
    
    # Test DHT11
    results['DHT11'] = test_dht11()
    
    # Test MQ-2
    results['MQ2'] = test_mq2()
    
    # Summary
    print("\n\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    for sensor, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{sensor:15} {status}")
    
    all_passed = all(results.values())
    print("\n" + ("All tests passed! ✓" if all_passed else "Some tests failed. See above for details."))
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
