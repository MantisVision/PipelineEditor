from PyQt5.QtCore import *
from examples.calculator.calc_config import *
from examples.calculator.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\add.png"))
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_obj_name = "calc_node_bg"

    def eval_impl(self):
        self.markDirty(False)
        self.markInvalid(False)
        return 123


@register_nodes(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\sub.png"))
    op_code = OP_NODE_SUB
    op_title = "Subtract"
    content_label = "-"
    content_label_obj_name = "calc_node_bg"


@register_nodes(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\mul.png"))
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_obj_name = "calc_node_mul"


@register_nodes(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\divide.png"))
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_obj_name = "calc_node_div"


@register_nodes(OP_NODE_TEST)
class CalcNode_Test(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_TEST
    op_title = "TEST"
    content_label = "TEST"
    content_label_obj_name = "calc_node_bg"
