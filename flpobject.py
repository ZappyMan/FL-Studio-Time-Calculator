# ---------------------------------------------------
#   Version: 2.0.0
#   Creators: Elliott Chimienti, Zane Little
#   Support us!: https://ko-fi.com/flhourcounterguys
# ---------------------------------------------------
#   Python 3.10
#   PyFLP 2.2.1
#   PySide6

import datetime, os
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt

# Local clone of pyflp library used
import pyflp
# CHANGES MADE TO LIBRARY
#   __init__.py 
#       - Line 131 divided file_size by 2
#    channel.py 
#       - Line 279 Commented out


# Custom object to hold information about parsed song
class FLP_Object():
    def __init__(self, file_path = None, relative_file_path = None):
        self.file_path = file_path
        self.relative_path = relative_file_path
        self.file_name = self.path_to_array(relative_file_path)[-1]
        self.creation_date = None           # datetime
        self.project_hours = None           # float
        # self.total_num_notes              # int
        self.tree_object = None
        self.list_object = None

    # Convert filepath from string to file array
    # Ex: "folder1/folder2/file1" == ["folder1","folder2","file1"]
    def path_to_array(self, path) -> list:
        # path_array = os.path.normpath(path)
        return path.split(os.sep)
        
    # Parse song
    def parse(self):
        if self.file_path:  # If file path exists
            try:    # attempt to parse file
                temp = pyflp.parse(self.file_path)
                self.project_hours = temp.time_spent/datetime.timedelta(hours=1) # Float
                self.creation_date = temp.created_on
                # total notes
                # other metrics                
            except:
                print("Error: Could not parse file ", self.file_name)
            self.create_tree_object()
            self.create_list_object()

    # Create TreeWidget instance for file tree
    def create_tree_object(self):
        self.tree_object = QTreeWidgetItem([self.file_name,str("{:.2f}".format(self.project_hours)),str(self.creation_date.date())])
        if self.project_hours:  # If file could be parsed
            self.tree_object.setCheckState(0,Qt.CheckState.Checked)
        else:
            self.tree_object.setBackground(0,Qt.GlobalColor.red)

    # Create TreeWidget instance for file list
    def create_list_object(self):
        self.list_object = QTreeWidgetItem([self.file_name,str("{:.2f}".format(self.project_hours)),str(self.creation_date.date())])
        if self.project_hours:  # If file could be parsed
            self.list_object.setCheckState(0,Qt.CheckState.Checked)
        else:
            self.list_object.setBackground(0,Qt.GlobalColor.red)