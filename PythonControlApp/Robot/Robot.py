import time
import Arduino.ArduinoSerialCommunication as Arduino
import json
import os

class Keyframe:
    def __init__(self, positions, speed = 2.0, keyName = "Key Name"):
        self.positions = positions
        self.speed = speed
        self.keyName = keyName

    def to_dict(self):
        return {
            'positions': self.positions,
            'speed': self.speed,
            'keyName': self.keyName
        }
    
    @staticmethod
    def from_dict(data):
        """Creates an instance from a dictionary."""
        return Keyframe(data['positions'], data['speed'], data['keyName'])

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
    {'name': 'X', 'value': 0.7},
    {'name': 'Y', 'value': 0.3},
    {'name': 'Z', 'value': -0.2},
]

# Current program loaded on the robot
loadedProgram = "Starter Program"
# Used to remember which program the user may want to override
programToOverwrite = ""
 
#  Not used
def Initialise():
    global program
    global loadedProgram
    # program = read_json_file(loadedProgram)
    
def read_json_file(filename):
    global program
    root_dir = "Programs"  # Base directory to search

    # Walk through all directories and files in root_dir
    for dirpath, dirnames, files in os.walk(root_dir):
        if filename in files:
            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, 'r') as file:
                    data = json.load(file)
                    program = [Keyframe.from_dict(kf) for kf in data['program']]
                    print(program)
                return f"Program was found and loaded from {full_path}. :)"
            except json.JSONDecodeError:
                return "Error decoding the JSON file."

    # If the file is not found in any subdirectory, load a default Keyframe
    # program = [Keyframe([30, 100, 110, 50, 90, 90])]
    return "Program was not found. :("
    
def write_json_file(filename, override=False):
    """
    Searches for a file in the Programs folder. If found and override is False, returns a warning message.
    Otherwise, writes data to the file.
    
    Args:
    filename (str): The name of the file to write to.
    override (bool): If True, overrides the file if it exists. Default is False.
    
    Returns:
    None: Returns a message if the file already exists and override is False, otherwise writes to the file.
    """
    global program
    global programToOverwrite
    global loadedProgram
    program_dict = [kf.to_dict() for kf in program]
    data = {'program': program_dict}
    root_dir = "Programs"  # Base directory to search

    # Attempt to find the file in the directory structure
    file_path = None
    for dirpath, dirnames, files in os.walk(root_dir):
        if filename in files:
            file_path = os.path.join(dirpath, filename)
            break

    if file_path and not override:
        programToOverwrite = filename
        return "File already exists. Do you want to overwrite it?"

    # If file was not found or override is True, write to the specified path
    if not file_path:
        file_path = os.path.join("Programs/Others", filename)  # Default path if not found

    # Write data to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    loadedProgram = filename
    return f"Data written to {file_path}"

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

    target_orientation = [0, 1, 0]

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
    # print(angles)
    global currentAngles
    # print(computed_position[:3, 3])
    for i in range(3):
        delta = computed_position[:3, 3][i] - target_position[i]
        if delta > 0.1:
            return currentAngles
    
    currentAngles = angles
    return angles

def MoveInBasePos():
    data = {"id": 0, "values": IK()}
    Arduino.send_json_to_arduino(data=data)
