import xml.etree.ElementTree as ET
import pandas as pd
# make sure to have easygui installed using pip install easygui
import easygui
from easygui import *

documentation = '''
Logic behind this script

[under construction]

Requirements: pandas, easygui and etree
'''

display_message = ccbox(documentation, 'Documentation')

if not display_message:
    exit() # exits the program if the user has clicked cancel button

# select the xml file and folder path for storing the result
folder_path_result = easygui.diropenbox(msg='Please select the folder to store the result excel file', title='Folder location for the result')
excel_file_name = enterbox('enter the name for your resulting excel file')
excel_sheet_name = enterbox('enter name for the result excel sheet')
filename = easygui.fileopenbox('Please select your desired cpacs .xml file from which data must be extracted')
excel_result_location = folder_path_result + '\\' + excel_file_name +'.xlsx'

# Parse the XML file imported from above
tree = ET.parse(filename)
# gets to the root of the selected xml file
#root = tree.getroot()

tree=ET.parse(filename)
#print (tree)
#print(tree.getroot())

mass_element_names = tree.findall(".//mEM//massDescription")
mass_elements = tree.findall(".//mEM//massDescription/mass")

component_masses={"names":[], "masses":[]}
for men in mass_element_names:
    #print(m.get("uID"), m.text)
    temp=men.get("uID")
    component_masses["names"].append(temp)
for me in mass_elements:
    component_masses["masses"].append(me.text)
print (len(component_masses["names"]), len(component_masses["masses"]))
    
data_file = pd.DataFrame.from_dict(component_masses, orient='columns')
data_file.to_excel(excel_result_location, index=True, sheet_name=excel_sheet_name)
