# ---------------------------------------------------
#   Version: 2.0.0
#   Creators: Elliott Chimienti, Zane Little
#   Support us!: https://ko-fi.com/flhourcounterguys
# ---------------------------------------------------
#   Python 3.10
#   PyFLP 2.2.1
#   PySide6

import sys, os, datetime
from PySide6.QtWidgets import QAbstractItemView, QTabWidget, QLabel, QSplitter ,QApplication, QMainWindow, QToolButton, QDateEdit, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QTreeWidget, QTreeWidgetItem, QGroupBox
from PySide6.QtCore import QDateTime, Qt
import pyqtgraph as pg
from filetree import CustomTree
from flpobject import FLP_Object

# Local clone of pyflp library used
import pyflp
# CHANGES MADE TO LIBRARY
#   __init__.py 
#       - Line 131 divided file_size by 2
#    channel.py 
#       - Line 279 Commented out

# --------------
#   Main Window
# --------------
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("FL Studio Time Calculator")
        window_size = QApplication.primaryScreen().availableSize()
        self.resize(window_size)    # Set app to size of screen
        self.resize(window_size.width()*0.85,window_size.height()*0.85)    # Set app to size of screen

        self.flp_objects = []   # Empty list to fold FLP_Object()'s
        self.load_state = False
        
        # ----- Define Buttons and widgets in order of appearance ------

        self.tabs = QTabWidget()

        self.filetree = CustomTree(True)
        self.filelist = CustomTree(False)

        #self.filetree.tree.itemChanged.connect(self.tree_checked)
        self.filetree.tree.model().dataChanged.connect(self.tree_checked)
        self.filelist.tree.model().dataChanged.connect(self.list_checked)

        self.tabs.addTab(self.filelist.tree, "List")
        self.tabs.addTab(self.filetree.tree, "Tree")

        self.tabs.setTabEnabled(1, True)
        self.tabs.setTabEnabled(2, True)

        self.end = QDateEdit(calendarPopup=True)
        self.end.setDateTime(QDateTime.currentDateTime())

        self.start = QDateEdit(calendarPopup=True)
        self.start.setDateTime(QDateTime(1997, 12, 18, 1, 0, 0)) # December, 18 1997; 1:00 am

        self.browse = QToolButton(self)
        self.browse.setText('Import')
        self.browse.clicked.connect(self.load_folders)

        self.MasterLayout = QHBoxLayout()                         # Verticle Box layout
        self.SectionDivider = QSplitter(Qt.Orientation.Horizontal)
        self.SectionDivider.setStyleSheet("QSplitter::handle{background: gray;}")
        self.Lwidget = QWidget()
        self.Rwidget = QWidget()

        # Left side ---------
        self.Sublayout1 = QVBoxLayout()    
        self.buttonLayout = QHBoxLayout()
        self.Filetreelayout = QHBoxLayout()

        self.buttonLayout.addWidget(self.browse)
        self.Filetreelayout.addWidget(self.tabs)

        self.Sublayout1.addLayout(self.buttonLayout)
        self.Sublayout1.addLayout(self.Filetreelayout)
        self.Lwidget.setLayout(self.Sublayout1)
        
        # Right side ---------
        self.Sublayout2 = QVBoxLayout()    
        self.InfoLayout = QHBoxLayout()            

        # QLabels to hold total project data
        self.total_num_files = QLabel("--")
        self.total_time_days = QLabel("--")
        self.total_time_hours = QLabel("--")
        self.average_time = QLabel("--")
        self.average_break_time = QLabel("--")

        self.GB1 = QGroupBox("Total Files")
        temp_layout1 = QVBoxLayout()
        temp_layout1.addWidget(self.total_num_files)
        self.GB1.setLayout(temp_layout1)

        self.GB2 = QGroupBox("Total Time in Days")
        temp_layout2 = QVBoxLayout()
        temp_layout2.addWidget(self.total_time_days)
        self.GB2.setLayout(temp_layout2)

        self.GB3 = QGroupBox("Total Time in Hours")
        temp_layout3 = QVBoxLayout()
        temp_layout3.addWidget(self.total_time_hours)
        self.GB3.setLayout(temp_layout3)

        self.GB4 = QGroupBox("Avg. Project Time")
        temp_layout4 = QVBoxLayout()
        temp_layout4.addWidget(self.average_time)
        self.GB4.setLayout(temp_layout4)

        self.GB5 = QGroupBox("Avg. Time Between Projects")
        temp_layout5 = QVBoxLayout()
        temp_layout5.addWidget(self.average_break_time)
        self.GB5.setLayout(temp_layout5)

        # Top Level Project Info
        self.InfoLayout.addWidget(self.GB1)
        self.InfoLayout.addWidget(self.GB2)
        self.InfoLayout.addWidget(self.GB3)
        self.InfoLayout.addWidget(self.GB4)
        self.InfoLayout.addWidget(self.GB5)

        # Scatter Plot
        axisX = pg.DateAxisItem(orientation='bottom')
        axisY = pg.AxisItem(orientation='left',text="Project Hours")
        self.plotItem = pg.PlotItem(title="Project Hours vs. Creation Date",axisItems={'bottom': axisX, 'left':axisY})
        self.plotItem.getAxis('bottom').setLabel("Creation Dates")
        self.plotItem.getAxis('left').setLabel("Time Spent (Hours)")
        self.scatter = pg.PlotWidget(plotItem=self.plotItem)

        self.Sublayout2.addLayout(self.InfoLayout)
        self.Sublayout2.addWidget(self.scatter)
        self.Rwidget.setLayout(self.Sublayout2)

        # Set Main Layout
        self.SectionDivider.addWidget(self.Lwidget)
        self.SectionDivider.addWidget(self.Rwidget)
        self.SectionDivider.setSizes([self.width()*.30,self.width()*.70]) # Set sections to 25% and 75% screen width
        self.filetree.tree.header().resizeSection(0,int(self.width()*.12))
        self.filelist.tree.header().resizeSection(0,int(self.width()*.12))
        self.filetree.tree.header().setMinimumSectionSize(int(self.width()*.05))
        self.filelist.tree.header().setMinimumSectionSize(int(self.width()*.05))
        # self.filelist.header().setSelectionBehavior()

        widget = QWidget()
        self.MasterLayout.addWidget(self.SectionDivider)
        widget.setLayout(self.MasterLayout)
        self.setCentralWidget(widget)

    # Triggered by tree item checkbox
    def tree_checked(self, signal):
        # grab all selected items
        if not self.load_state:
            selected_items = self.filetree.tree.selectedItems()             # Get list of user selected items
            triggered_treeitem = self.filetree.tree.itemFromIndex(signal)   # Get tree widget item
            triggered_state = triggered_treeitem.checkState(0)
            self.filetree.tree.model().blockSignals(True)
            if triggered_treeitem in selected_items:
                for item in selected_items: # Update all selected items
                    if item.background(0).color() != Qt.GlobalColor.red: # Check if item has children
                        item.setCheckState(0,triggered_state)
                        self.change_checkstate_of_all_children(item, triggered_state)
            self.change_checkstate_of_all_children(triggered_treeitem, triggered_treeitem.checkState(0))
            self.update_list_after_tree(selected_items)
            self.update_list_after_tree([triggered_treeitem])
            self.filetree.tree.model().blockSignals(False)  # re-Enable triggers when editing trees
            self.plot_data()
            self.filetree.tree.viewport().update()

    # Update filelist after filetree is updated
    def update_list_after_tree(self, changed_items: list[QTreeWidgetItem]):
        for item in changed_items:
            for object in self.flp_objects:
                if item == object.tree_object:
                    object.list_object.setCheckState(0,item.checkState(0))

    # Triggered by list item checkbox
    def list_checked(self, signal):
        if not self.load_state:
            triggered_treeitem = self.filelist.tree.itemFromIndex(signal)   # Get tree widget item
            triggered_state = triggered_treeitem.checkState(0)
            selected_items = self.filelist.tree.selectedItems()
            self.filelist.tree.model().blockSignals(True)
            if triggered_treeitem in selected_items:
                for item in selected_items:
                    if item.background(0).color() != Qt.GlobalColor.red:
                        item.setCheckState(0,triggered_state)
            # LEFT OFF HERE
            # ADD TREE/LIST UPDATE FUNCTIONS TO INSSIDE FOR LOOP,
            # SHOULDNT NEED TO ITERATE TWICE AND CHECK FOR RED TREEWIDGETITEM TWICE
            self.filetree.tree.model().blockSignals(True)
            self.update_tree_after_list(selected_items)
            self.update_tree_after_list([triggered_treeitem])
            self.filetree.tree.model().blockSignals(False)
            self.filelist.tree.model().blockSignals(False)  # re-Enable triggers when editing trees
            self.plot_data()
            self.filelist.tree.viewport().update()

    # Update filetree after filelist is updated
    def update_tree_after_list(self, changed_items: list[QTreeWidgetItem]):
        for item in changed_items:
            for object in self.flp_objects:
                if item == object.list_object:
                    object.tree_object.setCheckState(0,item.checkState(0))

    # Recursivly change checkstate of all children from starting item
    def change_checkstate_of_all_children(self, item: QTreeWidgetItem, checkState):
        for child_index in range(item.childCount()):
            if item.child(child_index).background(0).color() != Qt.GlobalColor.red:
                self.change_checkstate_of_all_children(item.child(child_index), checkState)
                item.child(child_index).setCheckState(0,checkState)

    # Parses FL Projects, loads into file list/tree, and plots data
    def load_folders(self):
        path = QFileDialog().getExistingDirectory(self, 'Select a directory')
        if(path):
            filepaths_full, filepaths_relative_dir = self.walk(path)  # Returns FLPFile struct Object
            if len(filepaths_full) > 0:   # If project(s) found
                self.load_state = True
                for full_path, relative_path in zip(filepaths_full, filepaths_relative_dir):
                    project = FLP_Object(full_path, relative_path)
                    project.parse() # parse project
                    self.filetree.add_item(project) # Add FLP to tree
                    self.filelist.add_item(project) # Add FLP to list
                    self.flp_objects.append(project)
                    self.plot_data()
                    QApplication.processEvents()
                self.filetree.compress_filepaths()
                self.load_state = False
    
    # Update graph and header information with FLP data
    def plot_data(self):
        self.plotItem.clear()
        x_data = []
        y_data = []
        for object in self.flp_objects:
            if object.list_object.checkState(0) == Qt.CheckState.Checked:
                x_data.append(object.creation_date.timestamp())
                y_data.append(object.project_hours)
        self.plotItem.plot(x=x_data,y=y_data,pen=None,symbol='o')
        viewBox = self.plotItem.getViewBox()
        viewBox.enableAutoRange()
        viewBox.setLimits(yMin=0)
        self.total_num_files.setText(str(len(self.flp_objects)))
        self.total_time_hours.setText(str("{:.2f}".format(sum(project.project_hours for project in self.flp_objects))))
        self.total_time_days.setText("{:.2f}".format(float(self.total_time_hours.text())/24))
        # Update information header

    # Fast search of selected root directory and sub-directories
    # Output nexted array in compress filepath form 
    def walk(self, path: str):
        filepath_full = []          # FULL path directory for importing
        filepath_relative_dir = []  # Relative directory for file tree
        root_folder_name = path.split(os.sep)[-1]
        update_process_counter = 0
        for p, _, f in os.walk(path):
            for file in f:
                if file.endswith('.flp') and "autosave" not in file and "overwritten" not in file:
                    full_path = os.path.join(p,file)
                    flp_path_string = os.path.relpath(full_path,path)
                    flp_path_string = os.path.join(root_folder_name,flp_path_string)
                    filepath_relative_dir.append(flp_path_string)
                    filepath_full.append(full_path)
                update_process_counter += 1
                if update_process_counter >= 1000:  # Must update process when searching through deep heiarchy
                    QApplication.processEvents()    # Update in future to custom loading screen
                    update_process_counter = 0

        return filepath_full, filepath_relative_dir  # Return list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()   # Main Window
    window.show()
    sys.exit(app.exec())