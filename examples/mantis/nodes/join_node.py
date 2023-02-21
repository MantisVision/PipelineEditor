from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.mv_config import *
from examples.mantis.mv_node_base import *
from examples.mantis.nodes.colap import CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_O_JOIN)
class MVNode_Join(MVOperationsNode):
    icon = str(current_file_path.joinpath(r"icons\ops.png"))
    op_code = OP_NODE_O_JOIN
    op_title = "JOIN"
    content_label = "JOIN"
    content_label_obj_name = "join_o_node_bg"
    colaps_widget = None
    uuid_line_edit = None
    _uuid = ""
    output_path = ""
    output_path_line_edit = None

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[2], outputs=[2])
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

            self.output_path_line_edit = QLineEdit("")
            self.output_path_line_edit.setReadOnly(True)

            UuidGB = CollapseGB()
            UuidGB.setTitle("UUID")
            UuidGB.setLayout(QGridLayout())
            UuidGB.layout().addWidget(QLabel("UUID:"), 0, 0)
            UuidGB.layout().addWidget(self.uuid_line_edit, 0, 1)
            UuidGB.setFixedHeight(UuidGB.sizeHint().height())
            layout.addWidget(UuidGB)

            outputGB = CollapseGB()
            outputGB.setTitle("Output")
            outputGB.setLayout(QFormLayout())
            outputGB.layout().addRow(QLabel("File Path: "), self.output_path_line_edit)
            outputGB.setFixedHeight(outputGB.sizeHint().height())
            layout.addWidget(outputGB)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ not in ["MVNode_S_UUID", "MVNode_Harvest"]:
            self.gr_node.setToolTip("Input should be either UUID or Harvest node")
            if self.uuid_line_edit:
                self.uuid_line_edit.setText("")
            self.markInvalid()
            return

        val = input_node.getVal()

        if val is None:
            self.gr_node.setToolTip("Not a valid UUID")
            if self.uuid_line_edit:
                self.uuid_line_edit.setText("")
            self.markInvalid()
            return

        self.markDirty(False)
        self.markInvalid(False)
        self.gr_node.setToolTip("")

        self.output_path = fr"C:\HARVEST\{val}\{val}_joined.mvx"

        if self.uuid_line_edit:
            self.uuid_line_edit.setText(val)

        if self.output_path_line_edit:
            self.output_path_line_edit.setText(self.output_path)

        return self.output_path

    def onTextChange(self):
        self._uuid = self.uuid_line_edit.text()
        output_node = self.getOutput(0)
        if output_node:
            output_node.eval()

    def getVal(self):
        return self.output_path if not self.isInvalid() else None

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self._uuid
        res['params'] = {}
        res['params']['uuid'] = self._uuid
        res['params']['output_path'] = self.output_path
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.uuid_line_edit.setText(data['uuid'])
            self.output_path_line_edit.setText(data['params']['output_path'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
