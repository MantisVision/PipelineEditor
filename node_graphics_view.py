from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER

MODE_NOOP = 1
MODE_EDGE_GRAPH = 2
EDGE_DRAG_THRESHOLD = 10


class QDMGraphicsView(QGraphicsView):
    def __init__(self, gr_scene, parent=None):
        super().__init__(parent)
        self.gr_scene = gr_scene
        self.initUI()
        self.setScene(self.gr_scene)
        self.mode = MODE_NOOP
        self.editingFlag = True
        self.zoom_in_factor = 1.25
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [5, 15]
        self.zoom_clamp = True
        self.last_mb_pos = None
        self.release_mb_pos = None

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        for item in self.gr_scene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            if hasattr(item, 'node'):
                item.node.remove()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleButtonEventPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleButtonEventRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleButtonEventPress(self, event):
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fake_event)

    def middleButtonEventRelease(self, event):
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        self.last_mb_pos = self.mapToScene(event.pos())

        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or not item:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if type(item) is QDMGraphicsSocket and self.mode == MODE_NOOP:
            self.mode = MODE_EDGE_GRAPH
            self.edgeDragStart(item)
            return

        if self.mode == MODE_EDGE_GRAPH and self.edgeDragEnd(item):
            return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)

        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or not item:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_GRAPH:
            if self.distBetweenClickRelease(event):
                pass
            else:
                if self.edgeDragEnd(item):
                    return

        super().mouseReleaseEvent(event)

    def edgeDragStart(self, item):
        print("start dragging")
        print("assign start socket")
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.gr_scene.scene, item.socket, None, EDGE_TYPE_BEZIER)

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP
        print('end dragging edge')

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket:
                print('Assign end socket')
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                if self.previousEdge:
                    self.previousEdge.remove()
                    self.previousEdge = None
                self.dragEdge._start_socket = self.last_start_socket
                self.dragEdge._end_socket = item.socket
                self.dragEdge._start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge._end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.updatePositions()
                return True

        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge:
            self.previousEdge._start_socket.edge = self.previousEdge

        return False

    def mouseMoveEvent(self, event) -> None:
        if self.mode == MODE_EDGE_GRAPH:
            pos = self.mapToScene(event.pos())
            self.dragEdge.gr_edge.setDestination(pos.x(), pos.y())
            self.dragEdge.gr_edge.update()
        super().mouseMoveEvent(event)

    def distBetweenClickRelease(self, event):
        self.release_mb_pos = self.mapToScene(event.pos())
        dist = self.release_mb_pos - self.last_mb_pos

        return (dist.x() * dist.x() + dist.y() * dist.y()) < EDGE_DRAG_THRESHOLD * EDGE_DRAG_THRESHOLD

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_out_factor = 1 / self.zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step

        clamped = False

        if self.zoom < self.zoom_range[0]:
            self.zoom = self.zoom_range[0]
            clamped = True
        if self.zoom > self.zoom_range[1]:
            self.zoom = self.zoom_range[1]
            clamped = True

        if not clamped or not self.zoom_clamp:
            self.scale(zoom_factor, zoom_factor)

    def getItemAtClick(self, event):
        return self.itemAt(event.pos())