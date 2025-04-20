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
    "mode": "time",  # or "light"

    "time": {
        "on": "08:00",
        "off": "08:30",
        "pump": False,
        "light": False
    },

    "light": {
        "threshold": 50.0,
        "pump": False,
        "light": False
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
            rounded_lux = int(round(avg_lux))


device_states = {
    "pump": False,
    "light": False
}

def toggle_device(device, state):
    pin = PUMP_PIN if device == "pump" else LIGHT_PIN
    GPIO.output(pin, GPIO.LOW if state else GPIO.HIGH)
    device_states[device] = state

def automation_job():
    mode = automation_rules["mode"]
    now = datetime.now().strftime("%H:%M")

    if mode == "time":
        time_rules = automation_rules["time"]
        if now == time_rules["on"]:
            if time_rules["pump"]:
                toggle_device("pump", True)
            if time_rules["light"]:
                toggle_device("light", True)
        elif now == time_rules["off"]:
            if time_rules["pump"]:
                toggle_device("pump", False)
            if time_rules["light"]:
                toggle_device("light", False)

    elif mode == "light":
        lux = sensor.lux or 0
        light_rules = automation_rules["light"]
        if lux < light_rules["threshold"]:
            if light_rules["pump"]:
                toggle_device("pump", True)
            if light_rules["light"]:
                toggle_device("light", True)
        else:
            if light_rules["pump"]:
                toggle_device("pump", False)
            if light_rules["light"]:
                toggle_device("light", False)


# Scheduler setup
schedule.every(1).minutes.do(automation_job)

threading.Thread(target=lux_sampling_thread, daemon=True).start()
@app.route('/')
def index():
    return render_template('index.html',
                           lux=rounded_lux,
                           current_time=datetime.now().strftime("%H:%M, %d-%m-%Y"),
                           device_states=device_states,
                           automation_rules=automation_rules),

@app.route('/api/toggle_device', methods=['POST'])
def toggle_device_api():
    data = request.json
    device = data['device']
    device_states[device] = not device_states[device]
    toggle_device(device, device_states[device])
    return jsonify(status='success', state=device_states[device])

@app.route('/api/update_automation', methods=['POST'])
def update_automation():
    data = request.json
    automation_rules["mode"] = data["mode"]
    
    automation_rules["time"]["on"] = data["time_on"]
    automation_rules["time"]["off"] = data["time_off"]
    automation_rules["time"]["pump"] = data["time_pump"]
    automation_rules["time"]["light"] = data["time_light"]
    
    automation_rules["light"]["threshold"] = float(data["lux_threshold"])
    automation_rules["light"]["pump"] = data["lux_pump"]
    automation_rules["light"]["light"] = data["lux_light"]
    
    return jsonify(status='success')

@app.route('/api/get_status', methods=['GET'])
def get_status():
    return jsonify({
        'lux': rounded_lux,
        'datetime': datetime.now().strftime("%H:%M, %d-%m-%Y"),
        'device_states': device_states
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
