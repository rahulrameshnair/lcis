import tkinter as tk
from tkinter import simpledialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Use a simple dialog box to get the length of the array from the user
db_array_length = simpledialog.askinteger(title="Number of databases", prompt="Enter the no. of database dependencies:")

# Create an empty list to hold the array elements
db_names = []

# Loop through the length of the array and use a simple dialog box to get each element from the user
for i in range(db_array_length):
    element = simpledialog.askstring(title="Database name", prompt=f"Enter  {i+1} database:")
    db_names.append(element)

# Print the array to the console (for troubleshooting)
#print(db_names)
#print(db_names[1])
#print(len(db_names))