import sys
from PyQt5.QtCore import *
from pipelineeditor.graphics.node_graphics_socket import QDMGraphicsSocket


class EdgeSnapping():
    def __init__(self, gr_view, snapping_radius):
        self.gr_view = gr_view
        self.gr_scene = self.gr_view.gr_scene
        self.edge_snapping_radius = snapping_radius

    def getSnappedSocketItem(self, event):
        scenepos = self.gr_view.mapToScene(event.pos())
        grSocket, pos = self.getSnappedToSocketPosition(scenepos)
        return grSocket

    def getSnappedToSocketPosition(self, scenepos):
        scan_rect = QRectF(
            scenepos.x() - self.edge_snapping_radius,
            scenepos.y() - self.edge_snapping_radius,
            self.edge_snapping_radius * 2,
            self.edge_snapping_radius * 2
        )
        items = self.gr_scene.items(scan_rect)
        items = list(filter(lambda x: isinstance(x, QDMGraphicsSocket), items))

        if len(items) == 0:
            return None, scenepos

        selected_item = items[0]
        if len(items) > 1:
            # calculate the nearest socket
            nearest = sys.maxsize
            for grsock in items:
                grsock_scenepos = grsock.socket.node.getSocketScenePosition(grsock.socket)
                qpdist = QPointF(*grsock_scenepos) - scenepos
                dist = qpdist.x() * qpdist.x() + qpdist.y() * qpdist.y()
                if dist < nearest:
                    nearest, selected_item = dist, grsock

        selected_item.is_highlight = True

        calcpos = selected_item.socket.node.getSocketScenePosition(selected_item.socket)

        return selected_item, QPointF(*calcpos)