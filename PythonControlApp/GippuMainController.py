from Arduino.ArduinoSerialCommunication import InitArduinoConnection
# from PythonControlApp.UIMaster import InitUI, UpdateUI
from flask import Flask, jsonify,  render_template, request, send_file, redirect, url_for
# from firebase import IsHeOnDatabase, UploadEvent, GetPersonel, GetEveryoneInLab
import os
import Robot.Robot as Robot

# InitRobot()
InitArduinoConnection()
# InitUI()
# app = QApplication(sys.argv)
# main_ui = MainUI()
# main_ui.show()
# sys.exit(app.exec_())


# UpdateUI()

def GetTime():
    return GetDate().time()

def GetDate():
    import datetime
    current_date = datetime.datetime.now()
    return current_date


app = Flask(__name__)

@app.route("/")
def home():
    localIp = request.remote_addr
    
    return render_template('repeatPanel.html', elements = Robot.program), 200

@app.route('/element/<int:index>', methods=['GET', 'POST'])
def element_details(index):
    selected_element = Robot.program[index - 1]

    if request.method == 'POST':
        for i, value in enumerate(selected_element):
            selected_element[i] = int(request.form.get(f'value_{i+1}'))

    return render_template('element_details.html', selected_element=selected_element)


@app.route('/teachPanel')
def teachPanel():
    InitArduinoConnection()
    Robot.SwitchToTeachMode()

    return render_template('teachPanel.html', elements = Robot.program)

@app.route('/addPosition', methods=['GET', 'POST'])
def AddPosition():
    Robot.AddPosition(-1)
    redirect(url_for('teachPanel'))

# @app.route('/remove/<item>', methods=['POST'])
# def remove_item(item):
#     Robot.program.pop(int(item) - 1)

#     # if item in Robot.program:
#     #     print("da")
#     return redirect(url_for('teachPanel'))

@app.route('/remove/<item_index>', methods=['POST'])
def remove_item(item_index):
    index = int(item_index) - 1
    if 0 <= index < len(Robot.program):
        Robot.program.pop(index)
    return redirect(url_for('teachPanel'))

@app.route('/reorder/<from_index>/<to_index>', methods=['POST'])
def reorder_items(from_index, to_index):
    from_index = int(from_index)
    to_index = int(to_index)
    if 0 <= from_index < len(Robot.program) and 0 <= to_index < len(Robot.program):
        element = Robot.program.pop(from_index)
        Robot.program.insert(to_index, element)
    return redirect(url_for('teachPanel'))

# @app.route('/update_element', methods=['POST'])
# def update_element():
#     data = request.get_json()
#     index = data['index']
#     new_value = data['value']
#     Robot.program[index] = new_value
#     return jsonify(success=True)

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
     app.run(debug=True, port = port)