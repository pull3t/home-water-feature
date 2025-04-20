from flask import Flask, render_template, request, jsonify
import threading
import time
import board
import busio
import adafruit_tsl2591
import RPi.GPIO as GPIO
import schedule
from datetime import datetime
import subprocess
import sys
from statistics import mean

app = Flask(__name__)

# Lux readings
lux_readings = []
rounded_lux = 0

# GPIO setup
PUMP_PIN = 17   # BCM GPIO17 (pin 11)
LIGHT_PIN = 24  # BCM GPIO24 (pin 18)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.HIGH)

def check_i2c_sensor():
    try:
        output = subprocess.check_output(['i2cdetect', '-y', '1'], text=True)
        if "29" not in output:
            print("Lux light sensor not found. Please connect the sensor and restart the application.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("Failed to run i2cdetect. Ensure I2C is enabled and the i2c-tools package is installed.")
        sys.exit(1)

check_i2c_sensor()

# Sensor setup
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)

# Automation Rules (initial defaults)
automation_rules = {
    "pump": {
        "enabled": False,
        "on_time": "08:00",
        "off_time": "08:30"
    },
    "light": {
        "enabled": False,
        "lux_threshold": 50.0
    }
}

def lux_sampling_thread():
    global lux_readings, rounded_lux

    while True:
        try:
            reading = sensor.lux or 0
            lux_readings.append(reading)
            # Keep only the last 5 seconds (assumes 1 sample per second)
            if len(lux_readings) > 5:
                lux_readings.pop(0)
        except Exception as e:
            print(f"Lux read error: {e}")
            lux_readings.append(0)

        # Every 5 seconds, calculate average and round
        if len(lux_readings) == 5:
            avg_lux = mean(lux_readings)
            rounded_lux = round(avg_lux)
        time.sleep(1)  # Adjust to sample frequency (e.g., every 1s)


device_states = {
    "pump": False,
    "light": False
}

def toggle_device(device, state):
    pin = PUMP_PIN if device == "pump" else LIGHT_PIN
    GPIO.output(pin, GPIO.LOW if state else GPIO.HIGH)
    device_states[device] = state

def automation_job():
    # Time-based control for pump
    now = datetime.now().strftime("%H:%M")
    pump_rules = automation_rules["pump"]
    if pump_rules["enabled"]:
        if now == pump_rules["on_time"]:
            toggle_device("pump", True)
        elif now == pump_rules["off_time"]:
            toggle_device("pump", False)

    # Lux-based control for light
    light_rules = automation_rules["light"]
    current_lux = sensor.lux or 0
    if light_rules["enabled"]:
        if current_lux < light_rules["lux_threshold"]:
            toggle_device("light", True)
        else:
            toggle_device("light", False)

# Scheduler setup
schedule.every(1).minutes.do(automation_job)

# def scheduler_thread():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# threading.Thread(target=scheduler_thread, daemon=True).start()
threading.Thread(target=lux_sampling_thread, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', lux=rounded_lux, device_states=device_states, rules=automation_rules)

# @app.route('/')
# def index():
#     current_lux = sensor.lux or 0
#     return render_template('index.html', lux=current_lux, device_states=device_states, rules=automation_rules)

@app.route('/toggle/<device>', methods=['POST'])
def toggle(device):
    state = not device_states[device]
    toggle_device(device, state)
    return jsonify({"status": "success", "state": state})

@app.route('/update_rules', methods=['POST'])
def update_rules():
    data = request.json
    automation_rules["pump"]["enabled"] = data["pump_enabled"]
    automation_rules["pump"]["on_time"] = data["pump_on_time"]
    automation_rules["pump"]["off_time"] = data["pump_off_time"]
    automation_rules["light"]["enabled"] = data["light_enabled"]
    automation_rules["light"]["lux_threshold"] = float(data["lux_threshold"])
    return jsonify({"status": "success", "rules": automation_rules})

# @app.route('/lux', methods=['GET'])
# def get_lux():
#     lux = sensor.lux or 0
#     return jsonify({"lux": lux})

@app.route('/lux', methods=['GET'])
def get_lux():
    return jsonify({"lux": rounded_lux})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
