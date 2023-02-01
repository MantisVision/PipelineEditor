from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None) -> None:
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        # init flags
        self._was_moved = False
        self._last_selected_state = False

        self.initSizes()
        self.initAssets()

        self.initUI()

    def initUI(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        self.initTitle()
        self.title = self.node.title
        self.initContent()

    def initSizes(self):
        self.width = 180
        self.height = 240
        self.edge_roundness = 10
        self.edge_padding = 10
        self.title_height = 24
        self._title_horizontal_padding = 4
        self._title_vertical_padding = 4

    def initAssets(self):
        self._title_color = Qt.white
        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def onSelected(self):
        self.node.scene.gr_scene.itemSelected.emit()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)

        # optmize this, just update selected nodes
        for node in self.scene().scene.nodes:
            if self.node.gr_node.isSelected():
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseReleaseEvent(event)
        # handle when gr_node was moved
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.store_history("Node Moved", True)

            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = True
            # we need to store the last selected state, because moving is also means selecting the object
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # we want to skip storing selection in history
            return

        # handle when gr_node was clicked on
        if self._last_selected_state != self.isSelected() or self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def mouseDoubleClickEvent(self, event):
        """Overriden event for doubleclick. Resend to `Node::onDoubleClicked`"""
        self.node.onDoubleClicked(event)

    def boundingRect(self) -> QRectF:
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        # self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._title_horizontal_padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self._title_horizontal_padding)

    def initContent(self):
        self.gr_content = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding, self.width - 2 * self.edge_padding, self.height - 2 * self.edge_padding - self.title_height)
        self.gr_content.setWidget(self.content)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # contnet
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())