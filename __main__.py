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

        self.filetree.tree.itemSelectionChanged.connect(self.file_selection_signal)
        self.filelist.tree.itemSelectionChanged.connect(self.file_selection_signal)
        self.filetree.tree.model().dataChanged.connect(self.file_view_signal)
        self.filelist.tree.model().dataChanged.connect(self.file_view_signal)

        self.tabs.addTab(self.filelist.tree, "List")
        self.tabs.addTab(self.filetree.tree, "Tree")

        self.tabs.setTabEnabled(1, True)
        self.tabs.setTabEnabled(2, True)
        self.tabs.currentChanged.connect(self.update_file_selection_tab)

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

        pixel_size = int(window_size.height()/70)

        self.GB1 = QGroupBox("Total Files",)
        self.GB1.setStyleSheet("font: bold {:d}px".format(pixel_size))
        temp_layout1 = QVBoxLayout()
        temp_layout1.addWidget(self.total_num_files)
        self.GB1.setLayout(temp_layout1)

        self.GB2 = QGroupBox("Total Time in Days")
        self.GB2.setStyleSheet("font: bold {:d}px".format(pixel_size))
        temp_layout2 = QVBoxLayout()
        temp_layout2.addWidget(self.total_time_days)
        self.GB2.setLayout(temp_layout2)

        self.GB3 = QGroupBox("Total Time in Hours")
        self.GB3.setStyleSheet("font: bold {:d}px".format(pixel_size))
        temp_layout3 = QVBoxLayout()
        temp_layout3.addWidget(self.total_time_hours)
        self.GB3.setLayout(temp_layout3)

        self.GB4 = QGroupBox("Avg. Project Time")
        self.GB4.setStyleSheet("font: bold {:d}px".format(pixel_size))
        temp_layout4 = QVBoxLayout()
        temp_layout4.addWidget(self.average_time)
        self.GB4.setLayout(temp_layout4)

        self.GB5 = QGroupBox("Avg. Time Between Projects")
        self.GB5.setStyleSheet("font: bold {:d}px".format(pixel_size))
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

        widget = QWidget()
        self.MasterLayout.addWidget(self.SectionDivider)
        widget.setLayout(self.MasterLayout)
        self.setCentralWidget(widget)

    # Activated when user changes tabs
    # Index of current tab passed when signaled
    def update_file_selection_tab(self):
        self.filetree.tree.clear()
        self.filelist.tree.clear()
        if self.tabs.currentIndex() == 0:
            for _object in self.flp_objects:
                _object.create_standard_item()
                self.filelist.add_item(_object)
        else:
            for _object in self.flp_objects:
                _object.create_standard_item()
                self.filetree.add_item(_object)

    # Function activated by selection changed singal in either list or tree
    def file_selection_signal(self):
        self.update_visuals()

    # Function activated by data changed singal in either list or tree
    def file_view_signal(self, signal):
        if not self.load_state:
            if self.tabs.currentIndex() == 0:   # List
                selected_items = self.filelist.tree.selectedItems()             # Get list of user selected items
                triggered_item = self.filelist.tree.itemFromIndex(signal)   # Get tree widget item
                file_system = self.filelist.tree
            else:                               # Tree 
                selected_items = self.filetree.tree.selectedItems()
                triggered_item = self.filetree.tree.itemFromIndex(signal)   # Get tree widget item
                file_system = self.filetree.tree

            triggered_state = triggered_item.checkState(0)
            file_system.model().blockSignals(True)
            if triggered_item not in selected_items:
                selected_items.append(triggered_item)
            for item in selected_items: # Update all selected items
                if Qt.ItemFlag.ItemIsUserCheckable in item.flags(): # Check if item has children
                    item.setCheckState(0,triggered_state)
                    self.change_checkstate_of_children(item, triggered_state)
            file_system.model().blockSignals(False)
            file_system.viewport().update()
            self.update_object_states()
            self.update_visuals()

    # Recursivly change checkstate of all children from starting item
    def change_checkstate_of_children(self, item: QTreeWidgetItem, state: Qt.CheckState):
        for child_index in range(item.childCount()):
            if Qt.ItemFlag.ItemIsUserCheckable in item.flags():
                self.change_checkstate_of_children(item.child(child_index), state)
                item.child(child_index).setCheckState(0,state)

    # After file view has data changed, update personal class states 
    def update_object_states(self):
        for item in self.flp_objects:
            item.update_state()

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
                    self.flp_objects.append(project)
                    self.update_file_selection_tab()
                    self.update_visuals()
                    QApplication.processEvents()
                self.filetree.compress_filepaths()
                self.load_state = False
    
    # Update graph and header information with FLP data
    def update_visuals(self):
        # -- Collect data from project states
        x_data = []
        y_data = []    
        x_selected = []
        y_selected = []
        x_nselected = []
        y_nselected = []
        for project in self.flp_objects:
            if project.check_state == Qt.CheckState.Checked:
                if project.tree_item.isSelected():
                    x_selected.append(project.creation_date)
                    y_selected.append(project.project_hours)
                else:
                    x_nselected.append(project.creation_date)
                    y_nselected.append(project.project_hours)
                x_data.append(project.creation_date)
                y_data.append(project.project_hours)
        # -- Update Information Header
        y_length = len(y_data)
        if y_length > 0:
            total_hours = sum(y_data)
            self.total_num_files.setText(str(y_length))
            self.total_time_hours.setText(str("{:.2f}".format(total_hours)))
            self.total_time_days.setText("{:.2f}".format(float(self.total_time_hours.text())/24))
            self.average_time.setText(str("{:.2f}".format(total_hours/y_length)))
            if y_length > 1:
                timedetla = ((max(x_data)-min(x_data)).total_seconds()/86400)/(y_length-1)
            else:
                timedetla = 0
            self.average_break_time.setText("{:.2f} Days".format(timedetla))
        else:
            self.total_num_files.setText("--")
            self.total_time_hours.setText("--")
            self.total_time_days.setText("--")
            self.average_time.setText("--")
            self.average_break_time.setText("--")

        # -- Update Visual plot
        self.plotItem.clear()
        viewBox = self.plotItem.getViewBox()
        viewBox.setLimits(xMin=-62135596800.0, xMax=253370764800.0,yMin=-1e+307,yMax=1e+307)    # Library defaults
        self.plotItem.plot(x=[x.timestamp() for x in x_nselected],y=y_nselected,pen=None,symbol='o')
        self.plotItem.plot(x=[x.timestamp() for x in x_selected],y=y_selected,pen=None,symbolBrush=pg.mkColor('r'),symbol='o')  # Draw selected second for overlay effect
        viewBox.updateViewRange()
        _range = viewBox.viewRange()
        viewBox.setLimits(xMin=_range[0][0], xMax=_range[0][1],yMin=_range[1][0],yMax=_range[1][1])

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