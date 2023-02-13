import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

EDGE_CP_ROUNDNESS = 100     #: Bezier control point distance on the line
WEIGHT_SOURCE = 0.2         #: factor for square edge to change the midpoint between start and end socket


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge

        # init flags
        self._last_selected_state = False
        self.hovered = False

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        self.initAssets()
        self.initUI()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.setAcceptHoverEvents(True)

    def initAssets(self):
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._color_hovered  = QColor("#FF37A6FF")
        self._hover_width = 5
        self._width = 3

        self._pen = QPen(self._color)
        self._pen.setWidthF(self._width)
        self._pen_dragging = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_hovered  = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(self._hover_width)
        self._pen_selected.setWidthF(self._width)
        self._pen_dragging.setWidthF(self._width)
        self._pen_dragging.setStyle(Qt.DashLine)

    def onSelected(self):
        self.edge.scene.gr_scene.itemSelected.emit()

    def doSelect(self, new_state):
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state:
            self.onSelected()

    def hoverEnterEvent(self, event) -> None:
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event) -> None:
        self.hovered = False
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        super().mouseReleaseEvent(event)
        if self._last_selected_state != self.isSelected():
            self.edge.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def setSource(self, x, y):
        self.posSource = x, y

    def boundingRect(self) -> QRectF:
        return self.shape().boundingRect()

    def shape(self) -> QPainterPath:
        return self.calcPath()

    def setDestination(self, x, y):
        self.posDestination = x, y

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None) -> None:
        self.setPath(self.calcPath())

        painter.setBrush(Qt.NoBrush)

        if self.hovered and self.edge.end_socket:
            painter.setPen(self._pen_hovered)
            painter.drawPath(self.path())

        if not self.edge.end_socket:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.drawPath(self.path())

    def calcPath(self):
        raise NotImplementedError("This method must be overriden by the child class")

    def intersects_with(self, p1, p2):
        cut_path = QPainterPath(p1)
        cut_path.lineTo(p2)
        return cut_path.intersects(self.calcPath())


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(QPointF(self.posDestination[0], self.posDestination[1]))
        return path


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def calcPath(self):
        s = self.posSource
        d = self.posDestination

        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        if self.edge.start_socket:
            ssin = self.edge.start_socket.is_input
            ssout = self.edge.start_socket.is_output

            if (s[0] > d[0] and ssout) or (s[0] < d[0] and ssin):
                cpx_s = -cpx_s
                cpx_d = -cpx_d
                cpy_d = ((s[1] - d[1]) / math.fabs((s[1] - d[1]) if s[1] - d[1] != 0 else 0.001)) * EDGE_CP_ROUNDNESS
                cpy_s = ((d[1] - s[1]) / math.fabs((d[1] - s[1]) if d[1] - s[1] != 0 else 0.001)) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(s[0], s[1]))
        path.cubicTo(
            s[0] + cpx_s,
            s[1] + cpy_s,
            d[0] + cpx_d,
            d[1] + cpy_d,
            d[0],
            d[1]
        )

        return path


class GraphicsEdgePathSquare(QDMGraphicsEdge):
    """Square line connection Graphics Edge"""
    def __init__(self, *args, handle_weight=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self.rand = None
        self.handle_weight = handle_weight

    def calcPath(self):
        """Calculate the square edge line connection

        :returns: ``QPainterPath`` of the edge square line
        :rtype: ``QPainterPath``
        """

        s = self.posSource
        d = self.posDestination

        mid_x = s[0] + ((d[0] - s[0]) * self.handle_weight)

        path = QPainterPath(QPointF(s[0], s[1]))
        path.lineTo(mid_x, s[1])
        path.lineTo(mid_x, d[1])
        path.lineTo(d[0], d[1])

        return path
