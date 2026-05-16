"""
MQ-2 Sensor Calibration Script
Run this to calibrate your MQ-2 sensor and determine baseline values
"""

import time
import board
import busio
from Adafruit_ADS1x15 import ADS1115

def calibrate_mq2():
    """
    Calibrate MQ-2 sensor
    Place sensor in clean air for 60 seconds before running this script
    """
    print("=" * 50)
    print("MQ-2 Sensor Calibration")
    print("=" * 50)
    print("\nPlace the MQ-2 sensor in CLEAN AIR")
    print("Waiting 30 seconds for sensor to stabilize...\n")
    
    # Initialize I2C and ADC
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS1115(i2c)
        
        # Warm up period
        for i in range(30, 0, -1):
            value = ads.read_adc(0, gain=1)
            print(f"[{i:2d}s] Raw ADC Value: {value:4d}", end='\r')
            time.sleep(1)
        
        print("\n\nCalibration phase - Reading clean air baseline...")
        print("-" * 50)
        
        # Calibration readings
        readings = []
        for i in range(60):
            value = ads.read_adc(0, gain=1)
            readings.append(value)
            print(f"Reading {i+1:2d}/60 - ADC: {value:4d}", end='\r')
            time.sleep(0.5)
        
        # Calculate statistics
        clean_air_baseline = sum(readings) // len(readings)
        min_val = min(readings)
        max_val = max(readings)
        variance = max(readings) - min(readings)
        
        print("\n\n" + "=" * 50)
        print("CALIBRATION RESULTS (Clean Air)")
        print("=" * 50)
        print(f"Baseline Value (Average): {clean_air_baseline}")
        print(f"Minimum Reading: {min_val}")
        print(f"Maximum Reading: {max_val}")
        print(f"Variance: {variance}")
        print("\nRecommended threshold values:")
        print(f"  Clean Air Baseline: {clean_air_baseline}")
        print(f"  Warning Threshold: {clean_air_baseline + 50}")
        print(f"  Danger Threshold: {clean_air_baseline + 150}")
        print("=" * 50)
        
        print("\nUpdate config.py with these values:")
        print(f"""
MQ2_THRESHOLDS = {{
    'clean_air': {clean_air_baseline},
    'warning': {clean_air_baseline + 50},
    'danger': {clean_air_baseline + 150},
}}
        """)
        
    except Exception as e:
        print(f"\nError during calibration: {e}")
        print("Make sure:")
        print("  - I2C is enabled on Raspberry Pi")
        print("  - ADS1115 is connected via I2C")
        print("  - MQ-2 is connected to Channel 0 of ADS1115")


if __name__ == "__main__":
    try:
        calibrate_mq2()
    except KeyboardInterrupt:
        print("\n\nCalibration cancelled by user")
