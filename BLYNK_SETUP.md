# Blynk App Setup Guide

## Create Blynk Account

1. Download **Blynk IoT** app from:
   - iOS: App Store
   - Android: Google Play

2. Create new account:
   - Email: Your email address
   - Password: Strong password
   - Confirm password

3. Go to: https://blynk.cloud (via browser)
   - Sign in with same credentials

---

## Create New Project

### In Blynk.cloud (Web):

1. Click **"New Project"** button
2. Project name: `Post-Fire RC Car`
3. Select device type: **Raspberry Pi**
4. Select connection type: **WiFi**
5. Click **"Create"**

### Copy Auth Token:
- Find your auth token (email or project dashboard)
- Copy this token to `config.py`:
  ```python
  BLYNK_AUTH = "paste_token_here"
  ```

---

## Setup Virtual Pins in Blynk App

### Open Your Project in App

Click Play button (▶) → Edit mode (pencil icon)

### Output Widgets Only (No Controls)

Add these three widgets to show sensor readings only:

### Add Widget: V4 - Humidity Label (DHT22)

1. Tap **"+"** → Add widget
2. Select **"Label"**
3. Settings:
   - **Virtual Pin**: V4
   - **Name**: Humidity
   - **Display**: "--" (optional default)
4. Click Save

### Add Widget: V5 - Temperature Label (DHT22)

1. Tap **"+"** → Add widget
2. Select **"Label"**
3. Settings:
   - **Virtual Pin**: V5
   - **Name**: Temperature
   - **Display**: "--" (optional default)
4. Click Save

### Add Widget: V6 - Gas Level Gauge

1. Tap **"+"** → Add widget
2. Select **"Gauge"**
3. Settings:
   - **Virtual Pin**: V6
   - **Name**: Gas Level
   - **Min**: 0
   - **Max**: 100
   - **Color**: Select red for high values
4. Click Save

---

## Optional: Advanced Dashboard Setup

### Add Display Names
Each label can show custom format:
- Temperature: `{V5} °C`
- Humidity: `{V4} %`
- Gas Level: `{V6} PPM`

### Color Coding (V6 - Gas Level)

Configure alerts based on value:
- **0-30**: Green (Safe)
- **30-60**: Yellow (Caution)
- **60+**: Red (Danger)

The app will automatically update colors.

---

## Blynk Virtual Pins Reference

| Virtual Pin | Widget | Purpose | Range |
|------------|--------|---------|-------|
| V4 | Label | DHT22 Humidity Reading | 0-100% |
| V5 | Label | DHT22 Temperature Reading | -40 to 80°C |
| V6 | Gauge | Gas/Smoke Level | 0-100 |

---

## Testing Blynk Connection

### Verify WiFi Connected
```bash
# On Raspberry Pi
ifconfig
# Look for inet address on wlan0
```

### Check Blynk Connection
1. Run main.py
2. Look for message: `Blynk object created`
3. Check Blynk app - humidity, temperature, and gas level should update

### Troubleshooting

**App shows "Device Offline":**
- Verify WiFi is connected on Raspberry Pi
- Check auth token matches in config.py
- Restart main.py script
- Check firewall isn't blocking port 80/443

**No sensor readings in app:**
- Ensure sensors are properly calibrated
- Check sensor connections
- Run `test_sensors.py` on Raspberry Pi
- Verify virtual pins V4, V5, V6 exist

---

## Dashboard Layout Tips

### Suggested Layout:
```
┌─────────────────────┐
│ SENSOR READINGS     │
│ Temp: {V5}  Hum: {V4} │
│ Gas Level: {V6}     │
└─────────────────────┘
```

---

## Security Notes

⚠️ **Important:**
- Keep your auth token **PRIVATE**
- Don't share config.py with auth token visible
- Use HTTPS when accessing blynk.cloud
- Consider IP whitelisting if available
- Regularly change password

---

## Blynk Pricing

- **Free Plan**: 1 device, limited voids, ads
- **Plus Plan**: Multiple devices, more data
- **Business Plan**: API access, priority support

For hobby use, free plan is sufficient.

---

## Additional Resources

- **Blynk Documentation**: https://docs.blynk.io/
- **API Reference**: https://docs.blynk.io/en/blynk-cloud/api
- **Widget Tutorials**: https://docs.blynk.io/en/getting-started/what-do-i-need-to-know-about-virtual-pins
- **Community Forum**: https://community.blynk.cc/

---

## FAQ

**Q: Can I use the app without internet?**
A: No, Blynk requires WiFi connection for cloud communication.

**Q: How many devices can I control?**
A: Free plan: 1 device. Paid plans: Multiple devices.

**Q: Can I access from anywhere?**
A: Yes, as long as your Raspberry Pi has internet and Blynk account is accessible.

**Q: What happens if connection drops?**
A: App will show "Device Offline". Reconnects automatically when WiFi returns.

---

**Next: Run `python3 main.py` and open Blynk app to monitor your RC car sensors.** 🚗📱
