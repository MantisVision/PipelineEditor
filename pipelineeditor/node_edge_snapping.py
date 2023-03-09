import sys
from PyQt5.QtCore import *
from pipelineeditor.graphics.node_graphics_socket import QDMGraphicsSocket


class EdgeSnapping():
    def __init__(self, gr_view, snapping_radius=26) -> None:

        self.gr_view = gr_view
        self.gr_scene = self.gr_view.gr_scene
        self.edge_snapping_radius = snapping_radius

    def getSnappedSocketItem(self, event):
        scenepos = self.gr_view.mapToScene(event.pos())
        gr_socket, _ = self.get_snapped_to_socket_position(scenepos)

        return gr_socket

    def get_snapped_to_socket_position(self, scenepos):
        scene_rect = QRectF(
            scenepos.x() - self.snapping_radius,
            scenepos.y() - self.snapping_radius,
            self.snapping_radius * 2,
            self.snapping_radius * 2,

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

        selected_item.is_highlight = True
        calcpos = selected_item.socket.node.getSocketScenePosition(selected_item.socket)

        return selected_item, QPointF(*calcpos)