from tkinter import *
import customtkinter
import PythonControlApp.Robot.Robot as Robot
from PythonControlApp.UI.ListBox import *

def InitUI():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("PythonControlApp/custom_theme.json")

    global programStepsUI
    global root

    root = customtkinter.CTk()
    root.geometry("400x800")

    # Switch function to toggle between the two containers
    def toggle_switch():
        if runContainer.winfo_ismapped():
            runContainer.pack_forget()
            teachContainer.pack()
            Robot.SwitchToTeachMode()
        else:
            teachContainer.pack_forget()
            runContainer.pack()

    # Use CTkButton instead of tkinter Button
    switch_button = customtkinter.CTkButton(master=root, text="Switch", command=toggle_switch)
    switch_button.pack()

    programStepsUI = customtkinter.CTkLabel(master=root, text="")
    programStepsUI.pack()

    programList = ListBox(root)

    # Create two containers to hold the two sets of UI elements
    runContainer = customtkinter.CTkFrame(master=root)
    teachContainer = customtkinter.CTkFrame(master=root)

    def RunProgramOnce():
        Robot.currentPosition = 0
        Robot.running = True

        def RunProgram():
            if Robot.currentPosition < len(Robot.program):
                Robot.MoveToNextPosition()
                runContainer.after(4000, RunProgram)
            else:
                running = False

        RunProgram()

    def RunProgramEndleslly():
        Robot.currentPosition = 0
        Robot.running = True

        def RunProgram():
            if Robot.currentPosition < len(Robot.program):
                Robot.MoveToNextPosition()
                runContainer.after(4000, RunProgram)
            else:
                RunProgramEndleslly()
                Robot.running = False

        RunProgram()

    # Define the UI elements for the first set
    label1 = customtkinter.CTkLabel(master=runContainer, text="Container 1")
    repeatProgramOnceButton = customtkinter.CTkButton(master=runContainer, text="Repeat action once", command=RunProgramOnce)
    repeatProgramEndlesslyButton = customtkinter.CTkButton(master=runContainer, text="Repeat action forever", command=RunProgramEndleslly)

    # Pack the UI elements for the first set into runContainer
    label1.pack()
    repeatProgramOnceButton.pack()
    repeatProgramEndlesslyButton.pack()

    # Define the UI elements for the second set
    label2 = customtkinter.CTkLabel(master=teachContainer, text="Container 2")
    button2 = customtkinter.CTkButton(master=teachContainer, text="Add Position", command=programList.AddPositionFromServoPos)

    # Create a button to remove the selected item
    remove_button = customtkinter.CTkButton(root, text="Remove", command=programList.remove_selected_item)
    remove_button.pack()

    # Pack the UI elements for the second set into teachContainer
    label2.pack()
    button2.pack()

    for child in root.winfo_children():
        child.pack(padx=10, pady=10)

    # Initially, show runContainer and hide teachContainer
    runContainer.pack()
    teachContainer.pack_forget()


def UpdateUI():
    def update_values():
        # Update the label with the new values
        program_text = "\n".join(str(value) for value in Robot.program)
        programStepsUI.configure(text=f"Values:\n{program_text}")
        
        # Schedule the update function to run again after a certain delay
        root.after(1000, update_values)  # Update every 1 second

    # Start the initial update and subsequent updates
    update_values()

    root.mainloop()
