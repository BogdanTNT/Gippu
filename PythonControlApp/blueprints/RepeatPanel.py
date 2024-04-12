import threading
from flask import jsonify, render_template, request
import Robot.Robot as Robot
from flask import Blueprint

repeatPanelBlueprint = Blueprint('RepeatPanelBlueprint', __name__)

@repeatPanelBlueprint.route("/")
def home():
    localIp = request.remote_addr
    
    return render_template('repeatPanel.html', Robot=Robot), 200

@repeatPanelBlueprint.route('/run_once', methods=['POST'])
def run_once():
    if not Robot.running:
        Robot.running = True
        Robot.running_thread = threading.Thread(target=Robot.RunProgramOnce)
        Robot.running_thread.start()
        print("The program started running")
    return jsonify(status='started')

@repeatPanelBlueprint.route('/run_forever', methods=['POST'])
def run_forever():
    if not Robot.running:
        Robot.running = True
        Robot.running_thread = threading.Thread(target=Robot.RunProgramForever)
        Robot.running_thread.start()
        print("The program started running")
    return jsonify(status='started')

@repeatPanelBlueprint.route('/stop_printing', methods=['POST'])
def stop_printing():
    if Robot.running:
        Robot.running = False
        Robot.running_thread.join()  # Wait for the thread to finish
        print("The program stopped running")
    return jsonify(status='stopped')