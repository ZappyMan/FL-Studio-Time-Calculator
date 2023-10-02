# ---------------------------------------------------
#   Version: 2.0.0
#   Creators: Elliott Chimienti, Zane Little
#   Support us!: https://ko-fi.com/flhourcounterguys
# ---------------------------------------------------
#   Python 3.10
#   PyFLP 2.2.1
#   PySide6

from typing import Union
from PySide6.QtWidgets import QGraphicsTextItem, QTreeView, QAbstractItemView, QHeaderView, QSplitter ,QApplication, QMainWindow, QToolButton, QDateEdit, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QTreeWidget, QTreeWidgetItem, QGroupBox
from PySide6.QtCore import Qt, QAbstractItemModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from flpobject import FLP_Object
import os
        
# Holds QTreeWidget file tree and appropriate customization functions
class CustomTree():
    def __init__(self, tree_bool):
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Files","Hours","Creation Date"])
        # self.tree.header().setSizeAdjustPolicy(QAbstractItemView.SizeAdjustPolicy.AdjustIgnored)
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.tree.header().setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        self.tree.header().setStretchLastSection(False)
        self.tree.header().resizeSection(1,15)
        self.tree.header().resizeSection(2,90)
        self.tree.setSortingEnabled(False)   # By default, disable when bulk updating
        self.tree.setAutoScroll(False)
        # configure sorting characteristics
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)   # Extended Selection
        self.tree_bool = tree_bool    # True == Tree, False == List

    # Add item to widget
    def add_item(self, flp_object: FLP_Object):
        if self.tree_bool:     # If this object is a tree
            self.insert_into_tree(flp_object)
        else:
            self.tree.insertTopLevelItem(0,flp_object.tree_item)

    # Inserts object into file tree
    def insert_into_tree(self, flp_object: FLP_Object):
        tree_pointer = None
        for directory in flp_object.path_to_array(flp_object.relative_path):
            # check for root directory
            if self.tree.topLevelItemCount() == 0:
                root = QTreeWidgetItem([directory,"",""])
                root.setCheckState(0,Qt.CheckState.Checked)
                self.tree.insertTopLevelItem(0,root)
                tree_pointer = root
            else:
                matches = self.tree.findItems(directory, Qt.MatchFlag.MatchExactly|Qt.MatchFlag.MatchRecursive, column=0)
                if len(matches) > 0:
                    tree_pointer = matches[0]
                else:
                    if directory.endswith(".flp"):  # Add file
                        tree_pointer.addChild(flp_object.tree_item)
                        tree_pointer.setExpanded(True)
                    else:
                        dir = QTreeWidgetItem([directory,"",""])
                        dir.setCheckState(0,Qt.CheckState.Checked)
                        tree_pointer.addChild(dir)
                        tree_pointer.setExpanded(True)
                        tree_pointer = dir

    # Compress filespaths for long paths with single children
    def compress_filepaths(self):
        # Check through toplevel items and their children
        for index in range(self.tree.topLevelItemCount()):
            top_level_item = self.tree.topLevelItem(index)
            for child_index in range(top_level_item.childCount()):
                self.recursive_depth_search(top_level_item.child(child_index))

        # .takechildren()

    # Recursivly search through children and find instances of paths that need to be compressed
    def recursive_depth_search(self, item: QTreeWidgetItem):
        count = item.childCount()
        if count == 0:  # Contains no children
            return
        elif count == 1:
            # if item has children, take them and merge strings
            if item.child(0).text(0).endswith(".flp"):
                return
            else:
                new_children = item.child(0).takeChildren()  # get childs child
                item.setText(0,os.path.join(item.text(0),item.child(0).text(0)))    # Update current items text
                item.removeChild(item.child(0))
                item.addChildren(new_children)
                self.recursive_depth_search(item)   # continue recursion
        else:   # Contains more than one child
            for child_index in range(item.childCount()):
                self.recursive_depth_search(item.child(child_index))
