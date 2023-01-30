from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path

from examples.calculator.calc_config import *
from pipelineeditor.utils import dump_exception


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

        self.addMyItem(name="Input",     icon=str(current_file_path.joinpath(r"icons\in.png")),     op_code=OP_NODE_INPUT)
        self.addMyItem(name="Output",    icon=str(current_file_path.joinpath(r"icons\out.png")),    op_code=OP_NODE_OUTPUT)
        self.addMyItem(name="Add",       icon=str(current_file_path.joinpath(r"icons\add.png")),    op_code=OP_NODE_ADD)
        self.addMyItem(name="Substract", icon=str(current_file_path.joinpath(r"icons\sub.png")),    op_code=OP_NODE_SUB)
        self.addMyItem(name="Multiply",  icon=str(current_file_path.joinpath(r"icons\mul.png")),    op_code=OP_NODE_MUL)
        self.addMyItem(name="Divide",    icon=str(current_file_path.joinpath(r"icons\divide.png")), op_code=OP_NODE_DIV)

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data inside item object
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            pixmap = QPixmap(item.data(Qt.UserRole))
            op_code = item.data(Qt.UserRole + 1)

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))

            drag.exec_(Qt.MoveAction)
        except Exception as e:
            dump_exception(e)
