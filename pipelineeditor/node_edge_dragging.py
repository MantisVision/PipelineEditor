from pipelineeditor.graphics.node_graphics_socket import QDMGraphicsSocket
from pipelineeditor.utils import dump_exception
from pipelineeditor.node_edge import Edge, EDGE_TYPE_DEFAULT


class EdgeDragging:
    def __init__(self, gr_view) -> None:
        self.gr_view = gr_view

    def getEdgeClass(self):
        return self.gr_view.gr_scene.scene.getEdgeClass()

    def edgeDragStart(self, item):
        try:
            self.drag_start_socket = item.socket
            self.drag_edge = self.getEdgeClass()(item.socket.node.scene, item.socket, None, EDGE_TYPE_DEFAULT)
        except Exception as e:
            dump_exception(e)

    def edgeDragEnd(self, item):
        self.gr_view.reset_mode()

        self.drag_edge.remove(silent=True)
        self.drag_edge = None

        try:
            if isinstance(item, QDMGraphicsSocket):
                if item.socket != self.drag_start_socket:

                    # if release dragging on socket (other than the first)
                    if not item.socket.multi_edge:
                        item.socket.remove_all_edges()

                    # First remove old edges / send notifications
                    for socket in (item.socket, self.drag_start_socket):
                        if not socket.multi_edge:
                            if socket.is_input:
                                # print("removing SILENTLY edges from input socket (is_input and !is_multi_edges) [DragStart]:", item.socket.edges)
                                socket.remove_all_edges(silent=True)
                            else:
                                socket.remove_all_edges(silent=False)

                    new_edge = self.getEdgeClass()(item.socket.node.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_DEFAULT)

                    for socket in [self.drag_start_socket, item.socket]:
                        socket.node.onEdgeConnectionChanged(new_edge)
                        # TODO: check this uncomment this line
                        # if socket.is_input:
                        socket.node.onInputChanged(socket)

                    self.gr_view.gr_scene.scene.history.store_history("Created new Edge", True)
                    return True
        except Exception as e:
            dump_exception(e)

        return False

    def update_destination(self, x, y):
        # according to sentry: 'NoneType' object has no attribute 'gr_edge'
        if self.drag_edge is not None and self.drag_edge.gr_edge:
            self.drag_edge.gr_edge.setDestination(x, y)
            self.drag_edge.gr_edge.update()
        else:
            print(">>> Want to update self.drag_edge gr_edge, but it's None!!!")