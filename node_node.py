from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget


class Node():
    def __init__(self, scene, title="New Node") -> None:
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.gr_scene.addItem(self.grNode)

        # self.grNode.title = "ASDASDAD"

        self.inputs = []
        self.outputs = []