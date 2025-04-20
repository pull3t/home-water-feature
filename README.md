# Raspberry Pi Zero 2 W – Flask Automation Dashboard

This project is a web-controlled automation system built using a **Raspberry Pi Zero 2 W**, a **TSL2591 Lux Sensor**, and a **2-channel relay module**. It allows real-time monitoring of light levels and independent control of two 12V devices (e.g., a water pump and a light) via a **Flask web dashboard**, with support for automation rules based on **time schedules** or **light intensity thresholds**.

---

## ⚙️ Features

- 🌞 **Real-Time Lux Sensor Monitoring** (TSL2591)
- 💡 **Independent Control** of Light and Pump via Web Interface
- ⏱️ **Time-Based Scheduling** for Pump Activation
- 🌗 **Lux Threshold Automation** for Light Control
- 📱 **Mobile-Friendly Interface** (HTML + JavaScript)
- 🔐 Basic Security Practices (run locally over LAN)

---

## 🧰 Hardware Requirements

- Raspberry Pi Zero 2 W (or any 40-pin Pi)
- MicroSD Card with Raspberry Pi OS Lite
- TSL2591 Light Sensor (I²C)
- 2-Channel Relay Module
- 12V Water Pump and 12V Light
- Power supplies for Raspberry Pi and 12V devices
- Jumper wires

---

## 🪛 GPIO Wiring

### TSL2591 Light Sensor

| Wire Colour | GPIO Pin (Raspberry Pi) | Sensor Pin | Function     |
|-------------|--------------------------|-------------|--------------|
| Red         | Pin 1                    | VIN         | 3.3V Power   |
| Black       | Pin 9                    | GND         | Ground       |
| White       | Pin 5 (GPIO3)            | SCL         | I²C Clock    |
| Yellow      | Pin 3 (GPIO2)            | SDA         | I²C Data     |

### Relay Module

| Wire Colour | GPIO Pin (Raspberry Pi) | Relay Pin | Function       |
|-------------|--------------------------|------------|--------------|
| Red         | -                        | DC+       | DC 12V Power  |
| Black       | -                        | DC-       | DC 12V Ground |
| Green       | Pin 11 (GPIO17)          | IN1       | Pump Control  |
| Blue        | Pin 18 (GPIO24)          | IN2       | Light Control |

---

## 🖥️ Software Setup

### 1. Flash Raspberry Pi OS Lite (Headless)

Use **Raspberry Pi Imager** to flash the latest Raspberry Pi OS Lite image. Enable:
- SSH
- Wi-Fi (via Advanced Settings or `wpa_supplicant.conf`)
- Set locale and hostname if needed

### 2. Enable I2C on the Pi

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-rpi.gpio git
sudo apt-get install -y i2c-tools
sudo raspi-config
# Interface Options > I2C > Enable
sudo reboot
sudo i2cdetect -y 1


### 3. Add water feature app to start up
Change directory to the /home-water-feature
sudo chmod +x startup.sh
sudo startup.sh

### 4. Update water feature app to latest version
Change directory to the /home-water-feature
sudo chmod +x update.sh
sudo update.sh