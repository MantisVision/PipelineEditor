from PyQt5.QtCore import *
from examples.calculator.calc_config import *
from examples.calculator.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_obj_name)


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

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        val = input_node.getVal()
        if val is None:
            self.gr_node.setToolTip("Not a NaN")
            self.markInvalid()
            return

        self.content.lbl.setText(str(val))

        self.markDirty(False)
        self.markInvalid(False)
        self.gr_node.setToolTip("")

        return val