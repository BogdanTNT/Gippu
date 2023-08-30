import Arduino.ArduinoSerialCommunication as Arduino

program = [[90, 100, 110, 150, 90, 90]]
currentPosition = 0
running = False
teachMode = False

def AddPosition(index):
    global program
    # Send JSON to Arduino
    data = {"id": 1, "values": [0, 0, 0, 0, 0, 0]}
    Arduino.send_json_to_arduino(data)

    # Receive JSON from Arduino
    received_data = Arduino.receive_json_from_arduino()

    if index == -1:
        index = len(program)
    else:
        index += 1
    program.insert(index, received_data['values'])

    return received_data['values']

def MoveToNextPosition():
    global teachMode
    teachMode = False

    global currentPosition
    if currentPosition >= len(program): return

    print(f"Moving to {program[currentPosition]}")

    data = {"id": 0, "values": program[currentPosition]}
    Arduino.send_json_to_arduino(data=data)
    currentPosition += 1

def MoveToFirstPosition():
    print(f"Moving to {program[0]}")

    data = {"id": 0, "values": program[0]}
    Arduino.send_json_to_arduino(data=data)

def SwitchToTeachMode():
    data = {"id": 1, "values": [0, 0, 0, 0, 0, 0]}
    Arduino.send_json_to_arduino(data)
    Arduino.receive_json_from_arduino()
    global teachMode

    if teachMode == True:
        return True

    teachMode = True
    return False