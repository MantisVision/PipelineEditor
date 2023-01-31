from examples.calculator.calc_config import *
from examples.calculator.calc_node_base import *
from pathlib import Path

current_file_path = Path(__file__).parent


@register_nodes(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\add.png"))
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"


@register_nodes(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\sub.png"))
    op_code = OP_NODE_SUB
    op_title = "Subtract"
    content_label = "-"


@register_nodes(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\mul.png"))
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"


@register_nodes(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\divide.png"))
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"


@register_nodes(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\in.png"))
    op_code = OP_NODE_INPUT
    op_title = "Input"

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])


@register_nodes(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\out.png"))
    op_code = OP_NODE_OUTPUT
    op_title = "Output"

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[1], outputs=[])


@register_nodes(OP_NODE_TEST)
class CalcNode_Test(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_TEST
    op_title = "TEST"
    content_label = "TEST"