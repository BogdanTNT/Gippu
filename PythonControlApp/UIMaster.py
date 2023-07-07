from tkinter import *
import customtkinter
import PythonControlApp.Robot as Robot


def InitUI():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("PythonControlApp/custom_theme.json")

    global programStepsUI
    global root

    root = customtkinter.CTk()
    root.geometry("300x400")

    # Switch function to toggle between the two containers
    def toggle_switch():
        if container1.winfo_ismapped():
            container1.pack_forget()
            container2.pack()
        else:
            container2.pack_forget()
            container1.pack()

    # Use CTkButton instead of tkinter Button
    switch_button = customtkinter.CTkButton(master=root, text="Switch", command=toggle_switch)
    switch_button.pack()

    programStepsUI = customtkinter.CTkLabel(master=root, text="")
    programStepsUI.pack()

    # Create two containers to hold the two sets of UI elements
    container1 = customtkinter.CTkFrame(master=root)
    container2 = customtkinter.CTkFrame(master=root)

    def RunProgramOnce():
        Robot.currentPosition = 0
        Robot.running = True

        def RunProgram():
            if Robot.currentPosition < len(Robot.program):
                Robot.MoveToNextPosition()
                container1.after(2000, RunProgram)
            else:
                running = False

        RunProgram()

    def RunProgramEndleslly():
        Robot.currentPosition = 0
        Robot.running = True

        def RunProgram():
            if Robot.currentPosition < len(Robot.program):
                Robot.MoveToNextPosition()
                container1.after(2000, RunProgram)
            else:
                RunProgramEndleslly()
                Robot.running = False

        RunProgram()

    # Define the UI elements for the first set
    label1 = customtkinter.CTkLabel(master=container1, text="Container 1")
    repeatProgramOnceButton = customtkinter.CTkButton(master=container1, text="Repeat action once", command=RunProgramOnce)
    repeatProgramEndlesslyButton = customtkinter.CTkButton(master=container1, text="Repeat action forever", command=RunProgramEndleslly)

    # Pack the UI elements for the first set into container1
    repeatProgramOnceButton.pack()
    repeatProgramEndlesslyButton.pack()
    label1.pack()

    # Define the UI elements for the second set
    label2 = customtkinter.CTkLabel(master=container2, text="Container 2")
    button2 = customtkinter.CTkButton(master=container2, text="Add Position")

    # Pack the UI elements for the second set into container2
    button2.pack()
    label2.pack()

    # Initially, show container1 and hide container2
    container1.pack()
    container2.pack_forget()

    

    
def UpdateUI():
    def update_values():
        # Update the label with the new values
        programStepsUI.configure(text="Values: " + str(Robot.program))
        
        # Schedule the update function to run again after a certain delay
        root.after(1000, update_values)  # Update every 1 second

    # Start the initial update and subsequent updates
    update_values()


    root.mainloop()