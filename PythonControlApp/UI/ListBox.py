from tkinter import *
import customtkinter
from CTkListbox import *
import PythonControlApp.Robot.Robot as Robot

class ListBox(CTkListbox):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        for item in Robot.program:
            self.insert(customtkinter.END, item)

    def remove_selected_item(self):
        selected_index = self.index_of_current_selection()
        if selected_index:
            self.delete(selected_index)

    def AddPosition(self):
        whereToInsert = self.index_of_current_selection()
        newPos = Robot.AddPosition(index=whereToInsert)
        # print(whereToInsert)
        self.insert(whereToInsert + 1, newPos)

    def index_of_current_selection(self):
        value_to_find = self.get()

        try:
            index = Robot.program.index(value_to_find)
            return index
        except ValueError:
            return -1  # Value not found in the list
