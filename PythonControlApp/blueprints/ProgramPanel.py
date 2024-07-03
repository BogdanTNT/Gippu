from flask import Blueprint, render_template
import Robot.RobotController as RobotController

programPanelBlueprint = Blueprint('ProgramPanelBlueprint', __name__)

@programPanelBlueprint.route('/programPanel')
def program_panel():

    return render_template('programPanel.html', RobotController = RobotController), 200