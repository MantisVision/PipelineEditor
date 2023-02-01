from PyQt5.QtWidgets import *

from pipelineeditor.node_node import Node
from pipelineeditor.node_content_widget import QDMNodeContentWidget
from pipelineeditor.graphics.node_graphics_node import QDMGraphicsNode
from pipelineeditor.node_socket import *


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 8
        self.edge_padding = 0
        self._title_horizontal_padding = 8
        self._title_vertical_padding = 10


class CalcContentWidget(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_obj_name)


class CalcNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_obj_name = "calc_node_bg"

    def __init__(self, scene, inputs=[2, 2], outputs=[1]) -> None:
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = CalcContentWidget(self)
        self.gr_node = CalcGraphicsNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print(f"Deserialize CalcNode {self.__class__.__name__} res: {res}")
        return res
