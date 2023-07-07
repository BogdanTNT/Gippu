import serial
import json
import serial.tools.list_ports

arduino = None

def InitArduinoConnection():
    global arduino
    arduino = connect_to_arduino()

    # if arduino is None:
    #     sys.exit()

def connect_to_arduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description  # Modify this condition if needed
    ]

    if len(arduino_ports) == 0:
        print("Arduino not found.")
        return None

    arduino_port = arduino_ports[0]  # Use the first found Arduino port
    baud_rate = 9600

    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on port: {arduino_port}")
        return arduino
    except serial.SerialException as e:
        print(f"Serial connection error: {str(e)}")
        return None



def send_json_to_arduino(data):
    json_data = json.dumps(data)
    if arduino != None:
        arduino.write(json_data.encode())
    print(f"Sent JSON data: {json_data}")


def receive_json_from_arduino():
    if arduino != None:
        response = arduino.readline().decode().rstrip()
    print(f"Received JSON data: {response}")
    return json.loads(response)
