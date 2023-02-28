class EdgeRerouting:
    def __init__(self, gr_view) -> None:
        self.gr_view = gr_view
        self.start_socket = None
        self.is_rerouting = False
        self.rerouting_edges = []

    def getEdgeClass(self):
        return self.gr_view.gr_scene.scene.getEdgeClass()

    def updateScenePosition(self, x, y):
        if self.is_rerouting:
            for edge in self.rerouting_edges:
                if edge and edge.gr_edge:
                    edge.gr_edge.setDestination(x, y)
                    edge.gr_edge.update()

    def clearReroutingEdges(self):
        while self.rerouting_edges:
            edge = self.rerouting_edges.pop()
            edge.remove()

    def resetRerouting(self):
        self.is_rerouting = False
        self.start_socket = None
        # self.rerouting_edges = []

    def startRerouting(self, socket):
        self.start_socket = socket
        self.is_rerouting = True
        print("start rerouting from: ", socket)
        print("num edges: ", self.getAffectedEdges())
        self.setAffectedEdges(visibility=False)

        start_position = self.start_socket.node.getSocketScenePosition(self.start_socket)

        for edge in self.getAffectedEdges():
            other_socket = edge.getOtherSocket(self.start_socket)
            new_edge = self.getEdgeClass()(self.start_socket.node.scene, edge_type=edge.edge_type)
            new_edge.start_socket = other_socket
            new_edge.gr_edge.setSource(*other_socket.node.getSocketScenePosition(other_socket))
            new_edge.gr_edge.setDestination(*start_position)
            new_edge.gr_edge.update()
            self.rerouting_edges.append(new_edge)

    def getAffectedEdges(self):
        if not self.start_socket:
            return []

        return self.start_socket.edges.copy()

    def setAffectedEdges(self, visibility=True):
        for edge in self.getAffectedEdges():
            if visibility:
                edge.gr_edge.show()
            else:
                edge.gr_edge.hide()

    def stopRerouting(self, target=None):
        print("stop rerouting on: ", target)

        if self.start_socket:
            self.start_socket.gr_socket.is_highlighted = False

        affected_nodes = []

        if not target or target == self.start_socket:
            self.setAffectedEdges(visibility=True)
        else:
            print("Reconnected to new socket: ", target)
            self.setAffectedEdges(visibility=True)
            for edge in self.getAffectedEdges():
                for node in [edge.start_socket.node, edge.end_socket.node]:
                    if node not in affected_nodes:
                        affected_nodes.append((node, edge))

                if target.is_input:
                    target.remove_all_edges(silent=True)

                if edge.end_socket == self.start_socket:
                    edge.end_socket = target
                else:
                    edge.start_socket = target

                edge.updatePositions()

        self.clearReroutingEdges()

        for node, edge in affected_nodes:
            node.onEdgeConnectionChanged(edge)
            if edge.start_socket in node.inputs:
                node.onInputChanged(edge.start_socket)
            if edge.end_socket in node.inputs:
                node.onInputChanged(edge.end_socket)

        self.start_socket.node.scene.history.store_history("Rerout edges", set_modified=True)
        self.resetRerouting()
