import time
import requests
from flask import Flask, request, jsonify, render_template
from threading import Thread
import pyfirmata2
from datetime import datetime

# Flask setup
app = Flask(__name__)

# PyFirmata2 setup
board = pyfirmata2.Arduino(pyfirmata2.Arduino.AUTODETECT)
servo_pin = 9  # Pin connected to the servo signal wire
buzzer_pin = 10  # Pin connected to the buzzer

# Microservice URL
DB_SERVICE_URL = "http://db-service:5001"  # Update to the actual IP/hostname of the DB microservice

# Sweep servo function
def sweep_servo(delay_back=1.0, delay_level=1):

    sweep_angle = 30
    """
    Move the servo with a delay when sweeping back.
    :param delay_back: Time delay before the servo returns.
    """
    # Turn on the buzzer for 5 seconds
    board.digital[buzzer_pin].write(1)
    time.sleep(5)
    board.digital[buzzer_pin].write(0)

    # Sweep servo from 0° to 180°
    for angle in range(0, 60, 1):
        board.digital[servo_pin].write(angle)
        time.sleep(0.0001)

    # Delay before sweeping back
    time.sleep(delay_back)

    # Sweep servo back from 180° to 0°
    for angle in range(60, -1, -1):
        board.digital[servo_pin].write(angle)
        time.sleep(0.0001)

    # Log action to the database microservice
    delay_mapping_str = {0: 'not much', 1: 'just enough', 2: 'a lot!'}
    log_entry = {"action": delay_mapping_str[delay_level], "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    requests.post(f'{DB_SERVICE_URL}/log', json=log_entry)

@app.route('/')
def index():
    """Render the main web page."""
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control_servo():
    """
    Handle requests to control the servo.
    Receives a JSON payload with the `delayLevel` (0, 1, 2).
    """
    try:
        data = request.get_json()
        delay_level = int(data.get('delayLevel', 1))  # Default to 1 if not provided

        # Map slider levels to delay times (in seconds)
        delay_mapping = {0: .1, 1: 0.25, 2: 0.5}
        delay_time = delay_mapping.get(delay_level, 1.0)

        # Trigger the servo in a separate thread
        Thread(target=sweep_servo, args=(delay_time, delay_level)).start()
        return jsonify({"status": "success", "message": "Servo is moving"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@app.route('/logs', methods=['GET'])
def get_logs():
    # Retrieve logs from the database microservice
    response = requests.get(f'{DB_SERVICE_URL}/logs')
    return response.json()  # Forward the logs to the frontend

if __name__ == '__main__':
    # Configure the pins
    board.digital[servo_pin].mode = pyfirmata2.SERVO
    board.digital[buzzer_pin].mode = pyfirmata2.OUTPUT

    # Start Flask server
    app.run(host='0.0.0.0', port=5000)
