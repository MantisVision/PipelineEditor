from PyQt5.QtCore import *
from examples.calculator.calc_config import *
from examples.calculator.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent


@register_nodes(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\add.png"))
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_obj_name = "calc_node_bg"


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


@register_nodes(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\in.png"))
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_obj_name = "calc_node_input"

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.gr_node = CalcGraphicsNode(self)


@register_nodes(OP_NODE_TEST)
class CalcNode_Test(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_TEST
    op_title = "TEST"
    content_label = "TEST"
    content_label_obj_name = "calc_node_bg"


@register_nodes(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\out.png"))
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_obj_name = "calc_node_output"

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.gr_node = CalcGraphicsNode(self)


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_obj_name)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dump_exception(e)
        return res


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_obj_name)