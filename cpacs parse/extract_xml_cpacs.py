"""Note: this script has been depreciated and replaced with "extract_xml_cpacs_xpath"
The reason is that this script uses the uID to parse the cpacs data which is not robust compared to
the method of xpath.

"""
import xml.etree.ElementTree as ET
import pandas as pd
# make sure to have easygui installed using pip install easygui
import easygui
from easygui import *

documentation = '''
Logic behind this script

Note: Please make sure that the variable 'id_filename' stores the path of the uids excel file (uids.xlsx).
This uids excel file contains all the unique ids whose masses must be extracted from the cpacs file
Please do not change the format of this file. If this variable is not set, please click the cancel button.

1. At the appropriate prompts enter the desired folderlocation,  file and sheet names for the excel file that 
this program will output to. 
2. At the prompt select the input cpacs ".xml" file that must pe parsed
3. Go to the folder location that you previously selected to find the resulting excel file

At present this program will only extract tags with 'massdescription' and an unique ID.

Requirements: pandas, easygui and 
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
root = tree.getroot()

# Find each component by its unique ID and extract its mass value
components = {}  # dictionary for storing the extracted components as pairs of uID and its mass

# search ids store the ids that we need to search for in the whole xml file
id_filename = 'D:/Alicia/Work/first brightway database/cpacs_data_extraction/uids.xlsx'
required_ids = pd.read_excel(id_filename)
search_for_ids = required_ids['uids'].astype(str).values.tolist()


# search for these ids as uIDs in the xml file
for component in root.findall('.//massDescription'):
    uid = component.get('uID')
    if uid in search_for_ids:
        mass = component.find('mass').text
        components[uid] = mass

# search for ids as tags in the xml file (under construction, if required)

# storing the dictionary as an Excel file
# data_file = pd.DataFrame(data=components, index=[1]) to store the index values in row format. This results in
# an excel sheet where the unique ids are in the row format. This can result in a very low excel sheet if there are
# large number of unique ids

data_file = pd.DataFrame.from_dict(components, orient='index')
data_file.to_excel(excel_result_location, index=True, sheet_name=excel_sheet_name)


