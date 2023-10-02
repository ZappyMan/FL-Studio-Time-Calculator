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
from PySide6.QtGui import QStandardItem

# Local clone of pyflp library used
import pyflp


# Custom object to hold information about parsed song
class FLP_Object():
    def __init__(self, file_path = None, relative_file_path = None):
        self.file_path = file_path
        self.relative_path = relative_file_path
        self.file_name = self.path_to_array(relative_file_path)[-1]
        self.creation_date = None           # datetime
        self.project_hours = None           # float
        # self.total_num_notes              # int
        self.tree_item = None
        self.check_state = Qt.CheckState.Checked

    # Convert filepath from string to file array
    # Ex: "folder1/folder2/file1" == ["folder1","folder2","file1"]
    def path_to_array(self, path) -> list:
        # path_array = os.path.normpath(path)   # Normalize path
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
                self.project_hours = 0

    # Create standard item for different trees
    def create_standard_item(self):
        if self.creation_date:  # If file could be parsed
            self.tree_item = QTreeWidgetItem([self.file_name,str("{:.2f}".format(self.project_hours)),str(self.creation_date.date())])
            self.tree_item.setCheckState(0,self.check_state)
        else:
            self.tree_item = QTreeWidgetItem([self.file_name,"",""])
            self.tree_item.setBackground(0,Qt.GlobalColor.red)

    # Update personal class state based on tree_items checkstate
    def update_state(self):
        if Qt.ItemFlag.ItemIsUserCheckable in self.tree_item.flags():
            self.check_state = self.tree_item.checkState(0)


