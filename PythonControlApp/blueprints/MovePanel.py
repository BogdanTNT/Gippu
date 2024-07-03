import threading
import time
from flask import jsonify, redirect, render_template, request, url_for
from Arduino.ArduinoSerialCommunication import InitArduinoConnection
import Robot.Robot as Robot
from flask import Blueprint

movePanelBlueprint = Blueprint('MovePanelBlueprint', __name__)

increment_values = [1, 0.5, 0.1, 0.05]

@movePanelBlueprint.route('/movePanel')
def movePanel():
    InitArduinoConnection()

    Robot.MoveInBasePos()

    return render_template('movePanel.html', Robot = Robot, increment_values = increment_values)

@movePanelBlueprint.route('/increment/<int:index>', methods=['POST'])
def increment(index):
    increment_value = increment_values[int(request.form['increment_type'])]
    Robot.xyz[index]['value'] += increment_value
    Robot.MoveInBasePos()

    return render_template('movePanel.html', Robot = Robot, increment_values = increment_values)

@movePanelBlueprint.route('/decrement/<int:index>', methods=['POST'])
def decrement(index):
    increment_value = increment_values[int(request.form['increment_type'])]
    Robot.xyz[index]['value'] -= increment_value
    Robot.MoveInBasePos()

    return render_template('movePanel.html', Robot = Robot, increment_values = increment_values)
