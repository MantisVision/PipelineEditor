from PyQt5.QtWidgets import *

from pipelineeditor.node_node import Node
from pipelineeditor.node_content_widget import QDMNodeContentWidget
from pipelineeditor.graphics.node_graphics_node import QDMGraphicsNode


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_size = 5
        self._padding = 8


class CalcContentWidget(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_obj_name)


class CalcNode(Node):
    def __init__(self, scene, op_code, op_title, content_label="", content_label_obj_name="calc_node_bg", inputs=[2, 2], outputs=[1]) -> None:
        self.op_code = op_code
        self.op_title = op_title
        self.content_label = content_label
        self.content_label_obj_name = content_label_obj_name

        super().__init__(scene, self.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = CalcContentWidget(self)
        self.gr_node = CalcGraphicsNode(self)