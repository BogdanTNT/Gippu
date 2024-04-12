import threading
import time
from flask import jsonify, redirect, render_template, request, url_for
from Arduino.ArduinoSerialCommunication import InitArduinoConnection
import Robot.Robot as Robot
from flask import Blueprint

movePanelBlueprint = Blueprint('MovePanelBlueprint', __name__)


@movePanelBlueprint.route('/movePanel')
def movePanel():
    InitArduinoConnection()

    Robot.MoveInBasePos()

    return render_template('movePanel.html', Robot = Robot)

@movePanelBlueprint.route('/increment/<int:index>', methods=['POST'])
def increment(index):
    increment_values = [1, 0.5, 0.1, 0.05]
    increment_value = increment_values[int(request.form['increment_type'])]
    Robot.xyz[index]['value'] += increment_value
    Robot.MoveInBasePos()

    return render_template('movePanel.html', Robot = Robot)

@movePanelBlueprint.route('/decrement/<int:index>', methods=['POST'])
def decrement(index):
    increment_values = [1, 0.5, 0.1, 0.05]
    increment_value = increment_values[int(request.form['increment_type'])]
    Robot.xyz[index]['value'] -= increment_value
    Robot.MoveInBasePos()

    return render_template('movePanel.html', Robot = Robot)
