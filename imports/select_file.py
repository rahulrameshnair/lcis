import tkinter as tk
from tkinter import filedialog as fdialog
def select_file():
# Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()
# Use the file dialog box to select a file
    file_path = fdialog.askopenfilename()
# Extract the path and name of the selected file
    path = "/".join(file_path.split("/")[:-1])
    name = file_path.split("/")[-1]
    full_path = path + "/" + name
    return full_path
# Return the path and name of the selected file
#return full_path