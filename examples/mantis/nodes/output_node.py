from PyQt5.QtCore import *
from examples.mantis.calc_config import *
from examples.mantis.calc_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
from examples.mantis.nodes.colap import FrameLayout, CollapseGB
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

        val = input_node.eval()
        if val is None:
            self.gr_node.setToolTip("Not a NaN")
            self.markInvalid()
            return

        self.content.lbl.setText(str(val))

        self.markDirty(False)
        self.markInvalid(False)
        self.gr_node.setToolTip("")

        return val


@register_nodes(OP_NODE_T_MVX_FILE)
class CalcNode_T_MVX_File(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\out.png"))
    op_code = OP_NODE_T_MVX_FILE
    op_title = "MVX File"
    content_label = "MVX"
    content_label_obj_name = "mvx_target_node_bg"
    colaps_widget = None

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[1], outputs=[])
        self.createParamWidget()

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

            t = CollapseGB()
            t.setTitle("File path")
            t.setLayout(QFormLayout())
            input_path = QLineEdit("")
            input_path.setDisabled(True)
            t.layout().addRow(QLabel("File: "), input_path)
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

            t2 = CollapseGB()
            t2.setTitle("File path2")
            t2.setLayout(QFormLayout())
            input_path = QLineEdit("")
            input_path.setDisabled(True)
            t2.layout().addRow(QLabel("File: "), input_path)
            t2.setFixedHeight(t2.sizeHint().height())
            layout.addWidget(t2)

        return self.colaps_widget