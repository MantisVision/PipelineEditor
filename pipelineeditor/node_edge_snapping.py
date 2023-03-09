import sys
from PyQt5.QtCore import *
from pipelineeditor.graphics.node_graphics_socket import QDMGraphicsSocket


class EdgeSnapping():
    def __init__(self, gr_view, snapping_radius=24) -> None:
        self.gr_view = gr_view
        self.gr_scene = gr_view.gr_scene
        self.snapping_radius = snapping_radius

    def get_snapped_socket_item(self, event):
        scenepos = self.gr_view.mapToScene(event.pos())
        gr_socket, _ = self.get_snapped_to_socket_positio(scenepos)

        return gr_socket

    def get_snapped_to_socket_positio(self, scenepos):
        scene_rect = QRectF(
            scenepos.x() - self.snapping_radius,
            scenepos.y() - self.snapping_radius,
            self.snapping_radius * 2,
            self.snapping_radius * 2,
        )

        items = self.gr_scene.items(scene_rect)
        items = list(filter(lambda x: isinstance(x, QDMGraphicsSocket), items))

        if len(items) == 0:
            return None, scenepos

        selected_item = items[0]
        if len(items) > 1:
            nearest = sys.maxsize
            for gr_socket in items:
                gr_socket_scene_pos = gr_socket.socket.node.getSocketScenePosition(gr_socket)
                qpoint_distance = QPointF(*gr_socket_scene_pos) - scenepos
                distance = qpoint_distance.x() * qpoint_distance.x() + qpoint_distance.y() * qpoint_distance.y()
                if distance < nearest:
                    nearest = distance
                    selected_item = gr_socket

        selected_item.is_highlight = True
        calcpos = selected_item.socket.node.getSocketScenePosition(selected_item.socket)

        return selected_item, QPointF(*calcpos)