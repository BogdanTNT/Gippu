import time
import serial
import json
import serial.tools.list_ports

arduino = None

def InitArduinoConnection():
    global arduino
    if arduino == None:
        arduino = connect_to_arduino()

def connect_to_arduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description or 'USB Serial' in p.description  # Modify this condition if needed
    ]
    # for p in serial.tools.list_ports.comports():
    #     print(p.description)

    if len(arduino_ports) == 0:
        print("Arduino not found.")
        return None

    arduino_port = arduino_ports[0]  # Use the first found Arduino port
    baud_rate = 9600

    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on port: {arduino_port}")
        print(arduino)
        return arduino
    except serial.SerialException as e:
        print(f"Serial connection error: {str(e)}")
        return None



def send_json_to_arduino(data):
    global arduino
    json_data = json.dumps(data)
    if arduino is not None:
        arduino.write(json_data.encode())
        print(f"Sent JSON data: {json_data}")


def receive_json_from_arduino():
    global arduino
    response = ""
    print(response)
    while len(response) < 2:
        response = arduino.readline().decode().rstrip()
        time.sleep(0.1)
    print(f"Received JSON data: {response}")
    return json.loads(response)
