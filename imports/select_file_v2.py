import easygui
import os
def file_selection():
    file_path = easygui.fileopenbox()
    file_dir, file_name = os.path.split(file_path)
    #print (file_path)
    #print (file_name)
    return file_path, file_name