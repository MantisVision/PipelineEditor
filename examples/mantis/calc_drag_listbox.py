from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path

from examples.mantis.calc_config import *
from pipelineeditor.utils import dump_exception


class QDMDragListBox(QListWidget):
    def __init__(self, list_op_nodes=[], parent=None) -> None:
        super().__init__(parent)
        self.list_op_nodes = list_op_nodes
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.addMyItems()

    def addMyItems(self):
        # current_file_path = Path(__file__).parent
        keys = list(MV_NODES.keys()) if not self.list_op_nodes else self.list_op_nodes
        keys.sort()

        for key in keys:
            node = get_class_from_op_code(key)
            self.addMyItem(node.op_title, node.icon, node.op_code)

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
