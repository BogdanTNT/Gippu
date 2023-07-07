from PythonControlApp.ArduinoSerialCommunication import connect_to_arduino
from PythonControlApp.UIMaster import InitUI, UpdateUI
# from PythonControlApp.Robot import InitRobot


# InitRobot()
connect_to_arduino()
InitUI()

UpdateUI()
