# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
# # from custompyqt import set_appearance_mode, set_default_color_theme  # Assuming you have similar custom functions
# import PythonControlApp.Robot as Robot
# # from PythonControlApp.UI.ListBox import ListBox

# class MainUI(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # set_appearance_mode("dark")
#         # set_default_color_theme("PythonControlApp/custom_theme.json")

#         self.setGeometry(100, 100, 400, 800)
#         self.setWindowTitle("PyQt5 App")

#         self.programStepsUI = QLabel(self)
#         self.programStepsUI.setGeometry(10, 50, 380, 200)

#         self.programList = ListBox(self)

#         self.runContainer = QWidget(self)
#         self.runContainer.setGeometry(10, 300, 380, 200)

#         self.teachContainer = QWidget(self)
#         self.teachContainer.setGeometry(10, 300, 380, 200)

#         self.init_ui()

#     def init_ui(self):
#         switch_button = QPushButton("Switch", self)
#         switch_button.setGeometry(10, 10, 80, 30)
#         switch_button.clicked.connect(self.toggle_switch)

#         label1 = QLabel("Container 1", self.runContainer)
#         label1.setGeometry(10, 10, 100, 30)

#         repeatProgramOnceButton = QPushButton("Repeat action once", self.runContainer)
#         repeatProgramOnceButton.setGeometry(10, 50, 150, 30)
#         repeatProgramOnceButton.clicked.connect(self.run_program_once)

#         repeatProgramEndlesslyButton = QPushButton("Repeat action forever", self.runContainer)
#         repeatProgramEndlesslyButton.setGeometry(10, 90, 150, 30)
#         repeatProgramEndlesslyButton.clicked.connect(self.run_program_endlessly)

#         label2 = QLabel("Container 2", self.teachContainer)
#         label2.setGeometry(10, 10, 100, 30)

#         button2 = QPushButton("Add Position", self.teachContainer)
#         button2.setGeometry(10, 50, 100, 30)
#         button2.clicked.connect(self.programList.AddPosition)

#         remove_button = QPushButton("Remove", self)
#         remove_button.setGeometry(10, 550, 80, 30)
#         remove_button.clicked.connect(self.programList.remove_selected_item)

#         self.runContainer.hide()
#         self.teachContainer.hide()

#         self.update_values()

#     def toggle_switch(self):
#         if self.runContainer.isVisible():
#             self.runContainer.hide()
#             self.teachContainer.show()
#             Robot.SwitchToTeachMode()
#         else:
#             self.teachContainer.hide()
#             self.runContainer.show()

#     def run_program_once(self):
#         Robot.currentPosition = 0
#         Robot.running = True
#         self.run_program()

#     def run_program_endlessly(self):
#         Robot.currentPosition = 0
#         Robot.running = True
#         self.run_program()

#     def run_program(self):
#         if Robot.currentPosition < len(Robot.program):
#             Robot.MoveToNextPosition()
#             self.runContainer.repaint()
#             self.runContainer.repaint()
#             self.update_values()
#             self.runContainer.repaint()
#             self.runContainer.after(4000, self.run_program)
#         else:
#             Robot.running = False

#     def update_values(self):
#         program_text = "\n".join(str(value) for value in Robot.program)
#         self.programStepsUI.setText(f"Values:\n{program_text}")
#         self.repaint()
#         self.runContainer.repaint()
#         self.teachContainer.repaint()
#         self.after(1000, self.update_values)

