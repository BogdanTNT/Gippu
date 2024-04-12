import threading
import time
from flask import jsonify, redirect, render_template, url_for
from Arduino.ArduinoSerialCommunication import InitArduinoConnection
import Robot.Robot as Robot
from flask import Blueprint

teachPanelBlueprint = Blueprint('TeachPanelBlueprint', __name__)


@teachPanelBlueprint.route('/teachPanel')
def teachPanel():
    InitArduinoConnection()

    # time.sleep(1000)
    Robot.SwitchToTeachMode()

    return render_template('teachPanel.html', Robot = Robot)

@teachPanelBlueprint.route('/AddPositionFromServoPos', methods=['GET', 'POST'])
def AddPositionFromServoPos():
    Robot.AddPositionFromServoPos(-1)
    redirect(url_for('/teachPanel'))

# @app.route('/remove/<item>', methods=['POST'])
# def remove_item(item):
#     Robot.program.pop(int(item) - 1)

#     # if item in Robot.program:
#     #     print("da")
#     return redirect(url_for('teachPanel'))

@teachPanelBlueprint.route('/remove/<item_index>', methods=['POST'])
def remove_item(item_index):
    index = int(item_index) - 1
    if 0 <= index < len(Robot.program):
        Robot.program.pop(index)
    return redirect(url_for('teachPanel'))

@teachPanelBlueprint.route('/reorder/<from_index>/<to_index>', methods=['POST'])
def reorder_items(from_index, to_index):
    from_index = int(from_index)
    to_index = int(to_index)
    if 0 <= from_index < len(Robot.program) and 0 <= to_index < len(Robot.program):
        element = Robot.program.pop(from_index)
        Robot.program.insert(to_index, element)
    return redirect(url_for('teachPanel'))

