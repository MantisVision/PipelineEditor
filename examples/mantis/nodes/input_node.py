from PyQt5.QtCore import *
from examples.mantis.calc_config import *
from examples.mantis.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
from examples.mantis.nodes.colap import FrameLayout
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
        self.content = CalcInputContent(self)
        self.gr_node = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def eval_impl(self):
        u_val = self.content.edit.text()
        s_val = int(u_val)
        self.value = s_val
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.gr_node.setToolTip("")

        self.evalChildren()

        return self.value


@register_nodes(OP_NODE_S_MVX_FILE)
class CalcNode_S_MVX_File(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\in.png"))
    op_code = OP_NODE_S_MVX_FILE
    op_title = "MVX File"
    content_label = "MVX"
    content_label_obj_name = "mvx_source_node_bg"
    colaps_widget = None

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])

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


@register_nodes(OP_NODE_S_UUID)
class CalcNode_S_MVX_File(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\in.png"))
    op_code = OP_NODE_S_UUID
    op_title = "UUID"
    content_label_obj_name = "mvx_source_node_bg"
    colaps_widget = None

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])

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