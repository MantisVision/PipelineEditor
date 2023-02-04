from PyQt5.QtCore import *
from examples.calculator.calc_config import *
from examples.calculator.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
from examples.calculator.nodes.colap import FrameLayout # noqa
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

        colaps_widget = QWidget()
        colaps_widget.setMinimumWidth(250)
        colaps_widget.setStyleSheet("")
        colaps_widget.setObjectName(str(self.id))
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        colaps_widget.setLayout(layout)

        t = FrameLayout(title="CalcNode_Div")
        t.addWidget(QPushButton('div'))
        t.addWidget(QLineEdit())
        layout.addWidget(t)

        return colaps_widget


@register_nodes(OP_NODE_TEST)
class CalcNode_Test(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_TEST
    op_title = "TEST"
    content_label = "TEST"
    content_label_obj_name = "calc_node_bg"

    def createParamWidget(self):

        colaps_widget = QWidget()
        colaps_widget.setMinimumWidth(250)
        colaps_widget.setStyleSheet("")
        colaps_widget.setObjectName(str(self.id))
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        colaps_widget.setLayout(layout)

        t = FrameLayout(title="CalcNode_Test")
        t.addWidget(QPushButton('test'))
        t.addWidget(QLineEdit())
        layout.addWidget(t)

        return colaps_widget
