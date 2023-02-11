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


@register_nodes(OP_NODE_T_MVX_FILE)
class CalcNode_T_MVX_File(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\out.png"))
    op_code = OP_NODE_T_MVX_FILE
    op_title = "MVX File"
    content_label = "MVX"
    content_label_obj_name = "mvx_target_node_bg"
    colaps_widget = None
    file_line_edit = ""
    output_path = ""

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
            t.setLayout(QGridLayout())

            if not self.file_line_edit:
                self.file_line_edit = QLineEdit(self.output_path)
                self.file_line_edit.textChanged.connect(self.onTextChange)

            t.layout().addWidget(QLabel("File path:"), 0, 0)
            t.layout().addWidget(self.file_line_edit, 0, 1)
            browse_btn = QPushButton("...")
            browse_btn.setMaximumWidth(24)
            browse_btn.clicked.connect(self.BrowseFile)
            t.layout().addWidget(browse_btn, 0, 2)
            t.layout().setColumnStretch(1, 5)
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        if not self.output_path:
            self.markInvalid()
            self.gr_node.setToolTip("File wasn't selected")
            return

        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.gr_node.setToolTip("")

        return self.output_path

    def BrowseFile(self):
        fname, ffilter = QFileDialog.getOpenFileName(None, "Open a MVX file")

        if not fname:
            return

        self.file_line_edit.setText(fname)

    def onTextChange(self):
        self.output_path = self.file_line_edit.text()
        if not self.getInput().eval():
            self.markInvalid()
            self.gr_node.setToolTip("Input node is not vaild")
            return
