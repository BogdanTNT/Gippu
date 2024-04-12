from flask import jsonify, redirect, render_template, request, url_for
import Robot.Robot as Robot
from flask import Blueprint

programListBlueprint = Blueprint('ProgramListBlueprint', __name__)


@programListBlueprint.route('/element/<int:index>', methods=['GET', 'POST'])
def element_details(index):
    selected_element = Robot.program[index - 1].positions
    print(selected_element)
    if request.method == 'POST':
        for i, value in enumerate(selected_element):
            selected_element[i] = int(request.form.get(f'value_{i+1}'))

    return render_template('element_details.html', selected_element=selected_element)

@programListBlueprint.route('/get_current_number')
def get_current_number():
    return jsonify(number=Robot.currentPosition)