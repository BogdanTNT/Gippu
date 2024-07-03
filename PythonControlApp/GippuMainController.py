from Arduino.ArduinoSerialCommunication import InitArduinoConnection
from flask import Flask, jsonify,  render_template, request, send_file, redirect, url_for
# from firebase import IsHeOnDatabase, UploadEvent, GetPersonel, GetEveryoneInLab
import os
import blueprints.RepeatPanel as RepeatPanel
import blueprints.TeachPanel as TeachPanel
import blueprints.ProgramList as ProgramList
import blueprints.MovePanel as MovePanel
import blueprints.ProgramPanel as ProgramPanel
import Robot.Robot as Robot

InitArduinoConnection()

app = Flask(__name__)
app.register_blueprint(RepeatPanel.repeatPanelBlueprint)
app.register_blueprint(TeachPanel.teachPanelBlueprint)
app.register_blueprint(MovePanel.movePanelBlueprint)
app.register_blueprint(ProgramList.programListBlueprint)
app.register_blueprint(ProgramPanel.programPanelBlueprint)

Robot.Initialise()

@app.route('/')
def home():
    return redirect('/programPanel')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port = port)

