from PythonControlApp.ArduinoSerialCommunication import *

program = [[0, 130, 110, 180, 90, 90]]
currentPosition = 0
running = False

# def InitRobot():
#     global program
#     global currentPosition
#     program = [[0, 130, 110, 180, 90, 90]]
#     currentPosition = 0

def AddPosition():
    # Send JSON to Arduino
    data = {"id": 1, "values": [10, 20, 30, 40, 50, 60]}
    send_json_to_arduino(data)

    # Receive JSON from Arduino
    received_data = receive_json_from_arduino(arduino)
    program.append(received_data['values'])

def MoveToNextPosition():
    global currentPosition
    if currentPosition >= len(program): return

    data = {"id": 0, "values": program[currentPosition]}
    send_json_to_arduino(data=data)
    currentPosition += 1
