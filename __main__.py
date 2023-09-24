# ---------------------------------------------------
#   Version: 2.0.0
#   Creators: Elliott Chimienti, Zane Little
#   Support us!: https://ko-fi.com/flhourcounterguys
# ---------------------------------------------------
#   Python 3.10
#   PyFLP 2.2.1
#   PySide6

import sys, os, datetime, time
from PySide6.QtWidgets import QAbstractItemView, QTabWidget, QLabel, QSplitter ,QApplication, QMainWindow, QToolButton, QDateEdit, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QTreeWidget, QTreeWidgetItem, QGroupBox
from PySide6.QtCore import QDateTime, Qt
import pyqtgraph as pg

# Local clone of pyflp library used
import pyflp
# CHANGES MADE
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

        self.FLP_files = {
            "creation_dates": [],
            "time_spent": []
        } # List of custom dict holding every FLP file info
        self.total_time = 0  # Inital Time delta of 0
        
        # ----- Define Buttons and widgets in order of appearance ------

        self.tabs = QTabWidget()

        self.filetree = QTreeWidget()
        self.filetree.setColumnCount(3)
        self.filetree.setHeaderLabels(["Files","Hours","Creation Date"])
        self.filetree.setSortingEnabled(True)

        self.filelist = QTreeWidget()
        self.filelist.setColumnCount(3)
        self.filelist.setHeaderLabels(["Files","Hours","Creation Date"])
        self.filelist.setSortingEnabled(True)
        self.filelist.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)   # Extended Selection

        self.tabs.addTab(self.filetree, "Tree")
        self.tabs.addTab(self.filelist, "List")
        # self.tabs.currentChanged.connect(self.onTabChange) # Swap Qwidgets between layouts! (Stupid hacky solution)
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
        self.SectionDivider.setSizes([window_size.width()*.30,window_size.width()*.70]) # Set sections to 25% and 75% screen width
        self.filetree.header().resizeSection(0,int(window_size.width()*.12))
        self.filelist.header().resizeSection(0,int(window_size.width()*.12))
        self.filetree.header().setMinimumSectionSize(int(window_size.width()*.05))
        self.filelist.header().setMinimumSectionSize(int(window_size.width()*.05))
        # self.filelist.header().setSelectionBehavior()

        widget = QWidget()
        self.MasterLayout.addWidget(self.SectionDivider)
        widget.setLayout(self.MasterLayout)
        self.setCentralWidget(widget)

    # Triggered by tree item checkbox
    def tree_checked(self):
        pass
    
    # Triggered by list item checkbox
    def list_checked(self):
        pass

    # Loads file tree with paths and files
    def load_folders(self):
        path = QFileDialog().getExistingDirectory(self, 'Select a directory')
        if(path):
            FLPfiles, FLPfiles_full = self.walk(path)  # Returns FLPFile struct Object
            if len(FLPfiles) > 0:   # If project(s) found
                # Set root directory
                root_path = os.path.normpath(path)
                root = QTreeWidgetItem([root_path.split(os.sep)[-1],""])
                root.setCheckState(0,Qt.CheckState.Checked)
                self.filetree.insertTopLevelItem(0, root)
                root.setExpanded(True)
                for FLP_path, FLP_path_full in zip(FLPfiles, FLPfiles_full):
                    tree_pointer = None         # Holds last traversed TreeWudgetItem
                    text_color = Qt.GlobalColor.transparent
                    try:
                        hours, created_on = self.parse(FLP_path_full)   # Parse file
                    except:
                        text_color = Qt.GlobalColor.red
                    for file in FLP_path:   # For every index within FLP path
                        items = self.filetree.findItems(file, Qt.MatchFlag.MatchExactly|Qt.MatchFlag.MatchRecursive, column=0)
                        if len(items) > 0:              # If sub-directory already exists withinn tree
                            tree_pointer = items[0]     # Set pointer to that directory
                        else:                           # Create new tree item
                            temp = QTreeWidgetItem([file,""])
                            temp.setCheckState(0,Qt.CheckState.Checked)
                            if file.endswith(".flp"):
                                file_tree_temp = QTreeWidgetItem([file,str("{:.2f}".format(hours)),str(created_on.date())])
                                file_tree_temp.setCheckState(0,Qt.CheckState.Checked)
                                file_tree_temp.setBackground(0,text_color)
                                temp.setBackground(0,text_color)
                                self.filelist.addTopLevelItem(file_tree_temp)
                                temp.setData(1, Qt.ItemDataRole.DisplayRole, str("{:.2f}".format(hours)))
                                temp.setData(2, Qt.ItemDataRole.DisplayRole, str(created_on.date()))
                            temp.setExpanded(True)
                            tree_pointer.addChild(temp)
                            tree_pointer = temp         # Update pointer
                    QApplication.processEvents()

                range = self.scatter.getPlotItem().getViewBox().viewRange()
                self.scatter.getPlotItem().getViewBox().setLimits(xMin=range[0][0], xMax=range[0][1],   
                             yMin=range[1][0], yMax=range[1][1])
                          
    # Parse passed FLP file path
    # Parrelellize
    def parse(self, path):
        real_path = os.path.abspath(path)
        temp = pyflp.parse(real_path)
        hours = temp.time_spent/datetime.timedelta(hours=1) # Float
        self.total_time += hours
        self.FLP_files["creation_dates"].append(temp.created_on)
        self.FLP_files["time_spent"].append(hours)
        self.plotItem.plot(x=[x.timestamp() for x in self.FLP_files["creation_dates"]] , y=self.FLP_files["time_spent"], pen=None, symbol='o')
        num_files = len(self.FLP_files["creation_dates"])
        self.total_num_files.setText(str(num_files))
        self.total_time_hours.setText(str("{:.2f}".format(self.total_time)))
        self.average_time.setText(str("{:.2f}".format(self.total_time/num_files)))
        return hours, temp.created_on

    # Fast search of selected root directory and sub-directories
    def walk(self, path):
        FLPfiles = []
        FLPfiles_full = []
        root_folder_name = self.path_to_array(path)[-1]
        update_process_counter = 0
        for p, _, f in os.walk(path):
            for file in f:
                if file.endswith('.flp') and "autosave" not in file and "overwritten" not in file:
                    flp_path_string = os.path.join(p,file)
                    flp_path = os.path.relpath(flp_path_string,path)
                    flp_path = self.path_to_array(flp_path)
                    flp_path.insert(0,root_folder_name)
                    FLPfiles.append(flp_path)    # Append to filepath array
                    FLPfiles_full.append(flp_path_string)
                update_process_counter += 1
                if update_process_counter >= 1000:
                    QApplication.processEvents()
                    update_process_counter = 0
        return FLPfiles, FLPfiles_full
    
    # Convert filepath from string to file array
    # Ex: "folder1/folder2/file1" == ["folder1","folder2","file1"]
    def path_to_array(self, path):
        path_array = os.path.normpath(path)
        return path_array.split(os.sep)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()   # Main Window
    window.show()
    sys.exit(app.exec())