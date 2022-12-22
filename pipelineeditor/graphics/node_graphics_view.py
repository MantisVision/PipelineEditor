from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pipelineeditor.node_edge import Edge, EDGE_TYPE_BEZIER
from pipelineeditor.graphics.node_graphics_edge import QDMGraphicsEdge
from pipelineeditor.graphics.node_graphics_socket import QDMGraphicsSocket
from pipelineeditor.graphics.node_graphics_cutline import QDMGraphicsCutline

MODE_NOOP = 1
MODE_EDGE_GRAPH = 2
EDGE_DRAG_THRESHOLD = 10
MODE_EDGE_CUT = 3


class QDMGraphicsView(QGraphicsView):

    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, gr_scene, parent=None):
        super().__init__(parent)
        self.gr_scene = gr_scene
        self.initUI()
        self.setScene(self.gr_scene)
        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDragRect = False
        self.zoom_in_factor = 1.25
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [2, 15]
        self.zoom_clamp = True
        self.last_mb_pos = None
        self.release_mb_pos = None
        self.cutline = QDMGraphicsCutline()
        self.gr_scene.addItem(self.cutline)

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)

    def deleteSelected(self):
        for item in self.gr_scene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            if hasattr(item, 'node'):
                item.node.remove()
        self.gr_scene.scene.history.store_history("Delete Selected", True)

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

        # Shift clicking items
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

        # Cutline event
        if not item:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            else:
                self.rubberBandDragRect = True

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
            if self.distanceBetweenClickAndReleaseIsOff(event):
                if self.edgeDragEnd(item):
                    return

        if self.mode == MODE_EDGE_CUT:
            self.cut_intersecting_edges()
            self.cutline._line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return

        # Store selection in history_stamps
        if self.rubberBandDragRect:
            self.gr_scene.scene.history.store_history("Selection Changed")
            self.rubberBandDragRect = False

        super().mouseReleaseEvent(event)

    def edgeDragStart(self, item):
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.gr_scene.scene, item.socket, None, EDGE_TYPE_BEZIER)

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP

        self.drag_edge.remove()
        self.drag_edge = None

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.drag_start_socket:
                # if release dragging on socket (other than the first)
                if not item.socket.multi_edge:
                    item.socket.remove_all_edges()

                if not self.drag_start_socket.multi_edge:
                    self.drag_start_socket.remove_all_edges()

                Edge(self.gr_scene.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_BEZIER)
                self.gr_scene.scene.history.store_history("Created new Edge", True)
                return True

        return False

    def mouseMoveEvent(self, event) -> None:
        if self.mode == MODE_EDGE_GRAPH:
            pos = self.mapToScene(event.pos())
            self.drag_edge.gr_edge.setDestination(pos.x(), pos.y())
            self.drag_edge.gr_edge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline._line_points.append(pos)
            self.cutline.update()

        self.last_scne_mb_pos = self.mapToScene(event.pos())

        self.scenePosChanged.emit(int(self.last_scne_mb_pos.x()), int(self.last_scne_mb_pos.y()))
        super().mouseMoveEvent(event)

    def distanceBetweenClickAndReleaseIsOff(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_mb_pos
        edge_drag_threshold_sq = EDGE_DRAG_THRESHOLD * EDGE_DRAG_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq

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

    def cut_intersecting_edges(self):
        for ix in range(len(self.cutline._line_points) - 1):
            p1 = self.cutline._line_points[ix]
            p2 = self.cutline._line_points[ix + 1]

            for edge in self.gr_scene.scene.edges:
                if edge.gr_edge.intersects_with(p1, p2):
                    edge.remove()
        self.gr_scene.scene.history.store_history("Cutting Edge", True)