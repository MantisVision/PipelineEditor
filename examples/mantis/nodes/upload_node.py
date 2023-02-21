from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.mv_config import *
from examples.mantis.mv_node_base import *
from examples.mantis.nodes.colap import CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_O_UPLOAD)
class MVNode_Upload(MVOperationsNode):
    icon = str(current_file_path.joinpath(r"icons\ops.png"))
    op_code = OP_NODE_O_UPLOAD
    op_title = "UPLOAD"
    content_label = "UPLOAD"
    content_label_obj_name = "upload_o_node_bg"
    colaps_widget = None
    input_path = ""
    input_path_line_edit = ""
    uuid_line_edit = None

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[2], outputs=[])
        self.createParamWidget()

    def createParamWidget(self):
        if not self.colaps_widget:
            self.colaps_widget = QWidget()
            self.colaps_widget.setMinimumWidth(270)
            self.colaps_widget.setStyleSheet("")
            self.colaps_widget.setObjectName(str(self.id))
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)
            self.colaps_widget.setLayout(layout)

            self.uuid_line_edit = QLineEdit("")
            self.uuid_line_edit.setReadOnly(True)
            self.uuid_line_edit.textChanged.connect(self.onTextChange)

            self.input_path_line_edit = QLineEdit()
            self.input_path_line_edit.setReadOnly(True)
            self.input_path_line_edit.textChanged.connect(self.onTextChange)

            UuidGB = CollapseGB()
            UuidGB.setTitle("UUID")
            UuidGB.setLayout(QGridLayout())
            UuidGB.layout().addWidget(QLabel("UUID:"), 0, 0)
            UuidGB.layout().addWidget(self.uuid_line_edit, 0, 1)
            UuidGB.setFixedHeight(UuidGB.sizeHint().height())
            layout.addWidget(UuidGB)

            inputGB = CollapseGB()
            inputGB.setTitle("Input")
            inputGB.setLayout(QFormLayout())
            inputGB.layout().addRow(QLabel("File Path:"), self.input_path_line_edit)
            inputGB.setFixedHeight(inputGB.sizeHint().height())
            layout.addWidget(inputGB)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ not in ["MVNode_S_MVX_File", "MVNode_Join"]:
            self.gr_node.setToolTip("Input should be either MVX file or Join node")
            if self.input_path_line_edit:
                self.input_path_line_edit.setText("")
            self.markInvalid()
            return

        val = input_node.getVal()
        self.uuid_line_edit.setText(input_node.getUUID())

        if val is None:
            self.gr_node.setToolTip("File path is missing")
            if self.input_path_line_edit:
                self.input_path_line_edit.setText("")
            self.markInvalid()
            return

        if self.input_path_line_edit:
            self.input_path_line_edit.setText(val)

        if not Path(self.input_path).exists():
            self.markInvalid()
            self.markDescendantsDirty()
            self.gr_node.setToolTip("File wasn't found")
            return

        self.markDirty(False)
        self.markInvalid(False)
        self.gr_node.setToolTip("")

        return self.input_path

    def onTextChange(self):
        self.input_path = self.input_path_line_edit.text()
        self.eval()

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self._uuid
        res['params'] = {}
        res['params']['file_path'] = self.input_path_line_edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.uuid_line_edit.setText(data['uuid'])
            self.input_path_line_edit.setText(data['params']['file_path'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
