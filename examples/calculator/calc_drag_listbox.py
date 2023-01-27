from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path


class QDMDragListBox(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.addMyItems()

    def addMyItems(self):
        current_file_path = Path(__file__).parent

        self.addMyItem(name="input",     icon=str(current_file_path.joinpath(r"icons\in.png")))
        self.addMyItem(name="output",    icon=str(current_file_path.joinpath(r"icons\out.png")))
        self.addMyItem(name="Add",       icon=str(current_file_path.joinpath(r"icons\add.png")))
        self.addMyItem(name="Substract", icon=str(current_file_path.joinpath(r"icons\sub.png")))
        self.addMyItem(name="Multiply",  icon=str(current_file_path.joinpath(r"icons\mul.png")))
        self.addMyItem(name="Divide",    icon=str(current_file_path.joinpath(r"icons\divide.png")))

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon else ".")
        print(icon)
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)