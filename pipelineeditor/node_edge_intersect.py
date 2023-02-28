# -*- coding: utf-8 -*-
"""
A module containing the intersecting nodes functionality. If a node gets dragged and dropped on an existing edge
it will intersect that edge.
"""
from PyQt5.QtCore import *
from pipelineeditor.node_edge import Edge


class EdgeIntersect:

    def __init__(self, gr_view):
        self.gr_scene = gr_view.gr_scene
        self.gr_view = gr_view

    def dropNode(self, node):
        """
        Code handling the dropping of a node on an existing edge.
        """

        node_box = self.hotZone(node)
        edges = self.gr_scene.scene.edges

        # check if the node is dropped on an existing edge
        edge = self.intersect(node_box, edges)
        if not edge:
            return

        if self.isConnected(node):
            return

        # determine the order of start and end
        if edge.start_socket.is_output:
            socket_start = edge.start_socket
            socket_end = edge.end_socket
        else:
            socket_start = edge.end_socket
            socket_end = edge.start_socket

        # The new edges will have the same edge_type as the intersected edge
        edge_type = edge.edge_type
        edge.remove()
        self.gr_view.gr_scene.scene.history.store_history('Delete existing edge', set_modified=True)

        new_node_socket_in = node.inputs[0]
        Edge(self.gr_scene.scene, socket_start, new_node_socket_in, edge_type=edge_type)
        new_node_socket_out = node.outputs[0]
        Edge(self.gr_scene.scene, new_node_socket_out, socket_end, edge_type=edge_type)

        self.gr_view.gr_scene.scene.history.store_history('Created new edges by dropping node', set_modified=True)

    def hotZone(self, node):
        """A list of points creating a box around a node"""
        points = []
        node_pos = node.gr_node.scenePos()
        x = node_pos.x()
        y = node_pos.y()
        w = node.gr_node.width
        h = node.gr_node.height

        # Collision box points
        points.append(QPointF(x, y))
        points.append(QPointF(x + w, y))
        points.append(QPointF(x + w, y + h))
        points.append(QPointF(x, y + h))
        points.append(QPointF(x, y))

        return points

    def intersect(self, node_box, edges):
        """
        Code checking for intersection of a series of line points with all edges in the scene
        return the intersecting edge or None
        """
        # returns the first edge that intersects with the dropped node, ignores the rest
        for point in range(len(node_box) - 1):
            p1 = node_box[point]
            p2 = node_box[point + 1]

            for edge in edges:
                if edge.gr_edge.intersects_with(p1, p2):
                    return edge
        return None

    def isConnected(self, node):
        # Nodes with only inputs or outputs are excluded
        if node.inputs == [] or node.outputs == []:
            return True

        # Check if the node has edges connected
        return node.getInput() or node.getOutputs()
