import time
import Arduino.ArduinoSerialCommunication as Arduino


class Keyframe:
    def __init__(self, positions, speed = 2.0):
        self.positions = positions
        self.speed = speed

# Create instances of the struct
keyframe = Keyframe([30, 100, 110, 50, 90, 90])

# Store the struct instances in a list
program = [keyframe]
currentPosition = 0

running = False
running_thread = None

teachMode = False

# Robot details
currentAngles = []
motorMaxAngle = [180, 270, 270, 300, 300, 300]

IKController = None

xyz = [
    {'name': 'X', 'value': 0.4},
    {'name': 'Y', 'value': 0},
    {'name': 'Z', 'value': 0.4},
]

def RunProgramOnce():
    global running
    global currentPosition
    currentPosition = 0
    while running and currentPosition < len(program):
        time.sleep(program[currentPosition].speed)  # Print every 2 seconds
        MoveToNextPosition()

def RunProgramForever():
    global running
    global currentPosition
    currentPosition = 0
    while running:
        time.sleep(program[currentPosition].speed)  # Print every 2 seconds
        MoveToNextPosition()
        if currentPosition >= len(program):
            currentPosition = 0

def AddPositionFromServoPos(index):
    global program
    # Send JSON to Arduino
    data = {"id": 1, "values": [0, 0, 0, 0, 0, 0]}
    Arduino.send_json_to_arduino(data)

    # Receive JSON from Arduino
    received_data = Arduino.receive_json_from_arduino()

    if index == -1:
        index = len(program)
    # else:
    #     index += 1
    keyframe = Keyframe(received_data['values'])
    program.insert(index, keyframe)

    return received_data['values']



def MoveToNextPosition():
    global teachMode
    teachMode = False

    global currentPosition
    if currentPosition >= len(program): return

    print(f"Moving to {program[currentPosition].positions}")

    data = {"id": 0, "values": program[currentPosition].positions}
    Arduino.send_json_to_arduino(data=data)
    currentPosition += 1

def MoveToSpecificPosition(position):
    if position > len(program):
        print(f"The program is not long enough")
        return
    
    global currentPosition
    currentPosition = position

    print(f"Moving to pos {position} at coord {program[position].positions}")

    data = {"id": 0, "values": program[position].positions}
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

def InitIK():
    import ikpy.chain

    IKController = ikpy.chain.Chain.from_urdf_file("Robot/robo.urdf",active_links_mask=[False, True, True, True, True, True, True])

    return IKController


def IK():
    import math
    target_position = [xyz[0]['value'], xyz[1]['value'], xyz[2]['value']]

    target_orientation = [-1, 0, 0]

    global IKController

    if IKController == None:
        IKController = InitIK()
    ik = IKController.inverse_kinematics(target_position)
    ik = IKController.inverse_kinematics(target_position, target_orientation, orientation_mode="Y")
    angles = list(map(lambda r: int(math.degrees(r)), ik.tolist()))[1:]
    print("The angles of each joints are : ", angles)

    computed_position = IKController.forward_kinematics(ik)
    print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
    print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])

    # # angles.pop(0)
    for i in range(6):
        # print(i)
        angles[i] = int(angles[i] / motorMaxAngle[i] * 180)

    # angles = angles[1:]
    print(angles)
    global currentAngles
    print(computed_position[:3, 3])
    for i in range(3):
        delta = computed_position[:3, 3][i] - target_position[i]
        if delta > 0.1:
            return currentAngles
    
    currentAngles = angles
    return angles

def MoveInBasePos():
    data = {"id": 0, "values": IK()}
    Arduino.send_json_to_arduino(data=data)