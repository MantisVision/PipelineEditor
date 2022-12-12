from collections import OrderedDict
from graphics.node_graphics_edge import QDMGraphicsEdge
from node_node import Node
from node_edge import Edge


class SceneClipbaord():
    def __init__(self, scene) -> None:
        self.scene = scene

    def serializedSelected(self, delete=False):

        sel_nodes, sel_edges, sel_sockets = [], [], {}

        # Sort lists
        for item in self.scene.gr_scene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in item.node.inputs + item.node.outputs:
                    sel_sockets[socket.id] = socket
            elif isinstance(item, QDMGraphicsEdge):
                sel_edges.append(item.edge)

        # Remove edges that are not connected
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                pass
            else:
                edges_to_remove.append(edge)

        for edge in edges_to_remove:
            sel_edges.remove(edge)

        edges_final = []
        for edge in sel_edges:
            edges_final.append(edge.serialize())

        data = OrderedDict([
            ('nodes', sel_nodes),
            ('edges', edges_final)
        ])

        # delete in cut mode:
        if delete:
            self.scene.gr_scene.views()[0].deleteSelected()
            self.scene.history.store_history("Cut", True)

        return data

    def deserializeFromClipboard(self, data):
        hashmap = {}

        # Calculate mouse pos
        view = self.scene.gr_scene.views()[0]
        mouse_pos = view.last_mb_pos

        minx, maxx, miny, maxy = 0, 0, 0, 0

        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)

        # Calculate selected object bbox and center
        bbox_center_x = (minx + maxx) / 2
        bbox_center_y = (miny + maxy) / 2

        # Calculate offset of selected objects
        offsetx = mouse_pos.x() - bbox_center_x
        offsety = mouse_pos.y() - bbox_center_y

        # Create each node
        for node_data in data['nodes']:
            new_node = Node(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)

            # readjust new_node position
            pos = new_node.pos
            new_node.setPos(pos.x() + offsetx, pos.y() + offsety)

        # Create each edge
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        # Store history
        self.scene.history.store_history('Paste', True)
