from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.calc_config import *
from examples.mantis.calc_node_base import *
from examples.mantis.nodes.colap import FrameLayout
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\add.png"))
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_obj_name = "calc_node_bg"

    def eval_operation(self, input1, input2):
        return input1 + input2


@register_nodes(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\sub.png"))
    op_code = OP_NODE_SUB
    op_title = "Subtract"
    content_label = "-"
    content_label_obj_name = "calc_node_bg"

    def eval_operation(self, input1, input2):
        return input1 - input2


@register_nodes(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\mul.png"))
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_obj_name = "calc_node_mul"

    def eval_operation(self, input1, input2):
        return input1 * input2


@register_nodes(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\divide.png"))
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_obj_name = "calc_node_div"

    def eval_operation(self, input1, input2):
        return input1 / input2

    def createParamWidget(self):

        if not self.colaps_widget:
            self.colaps_widget = QWidget()
            self.colaps_widget.setMinimumWidth(250)
            self.colaps_widget.setStyleSheet("")
            self.colaps_widget.setObjectName(str(self.id))
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)
            self.colaps_widget.setLayout(layout)

            t = FrameLayout(title=self.__class__.__name__)
            t.addWidget(QPushButton('test'))
            t.addWidget(QLineEdit())
            layout.addWidget(t)

        return self.colaps_widget


@register_nodes(OP_NODE_TEST)
class CalcNode_Test(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_TEST
    op_title = "TEST"
    content_label = "TEST"
    content_label_obj_name = "calc_node_bg"
    colaps_widget = None

    def createParamWidget(self):
        if not self.colaps_widget:
            self.colaps_widget = QWidget()
            self.colaps_widget.setMinimumWidth(250)
            self.colaps_widget.setStyleSheet("")
            self.colaps_widget.setObjectName(str(self.id))
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)
            self.colaps_widget.setLayout(layout)

            t = FrameLayout(title=self.__class__.__name__)
            t.addWidget(QPushButton('test'))
            t.addWidget(QLineEdit())
            layout.addWidget(t)

        return self.colaps_widget
