from PyQt5.QtCore import *
from examples.calculator.calc_config import *
from examples.calculator.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


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


@register_nodes(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\in.png"))
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_obj_name = "calc_node_input"

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.gr_node = CalcGraphicsNode(self)
        self.content = CalcInputContent(self)
        self.content.edit.textChanged.connect(self.onInputChanged)
