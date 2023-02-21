from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.mv_config import *
from examples.mantis.mv_node_base import *
from examples.mantis.nodes.colap import CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_O_HARVEST)
class MVNode_Harvest(MVOperationsNode):
    icon = str(current_file_path.joinpath(r"icons\ops.png"))
    op_code = OP_NODE_O_HARVEST
    op_title = "HARVEST"
    content_label = "HARVEST"
    content_label_obj_name = "harvest_o_node_bg"
    colaps_widget = None
    output_path = ""
    _uuid = ""
    uuid_line_edit = None
    dropir_cb = None
    no_join_cb = None
    method_of_capture_line = None
    mv_session_line = None

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

            self.uuid_line_edit = QLineEdit()
            self.uuid_line_edit.setReadOnly(True)
            self.uuid_line_edit.textChanged.connect(self.onTextChange)

            self.method_of_capture_line = QLineEdit()
            self.mv_session_line = QLineEdit()
            self.dropir_cb = QComboBox()
            self.dropir_cb.setObjectName("dropir_cb")
            self.dropir_cb.setMaximumWidth(60)
            self.dropir_cb.addItems(["True", "False"])

            self.no_join_cb = QComboBox()
            self.no_join_cb.setObjectName("no_join_cb")
            self.no_join_cb.addItems(["True", "False"])
            self.no_join_cb.setMaximumWidth(60)

            UuidGB = CollapseGB()
            UuidGB.setTitle("UUID")
            UuidGB.setLayout(QGridLayout())
            UuidGB.layout().addWidget(QLabel("UUID:"), 0, 0)
            UuidGB.layout().addWidget(self.uuid_line_edit, 0, 1)
            UuidGB.setFixedHeight(UuidGB.sizeHint().height())
            layout.addWidget(UuidGB)

            paramsGB = CollapseGB()
            paramsGB.setTitle("Params")
            paramsGB.setLayout(QFormLayout())
            paramsGB.layout().addRow(QLabel("Method of Capture:"), self.method_of_capture_line)
            paramsGB.layout().addRow(QLabel("MV Session:"), self.mv_session_line)
            paramsGB.layout().addRow(QLabel("DropIR:"), self.dropir_cb)
            paramsGB.layout().addRow(QLabel("No Join:"), self.no_join_cb)
            paramsGB.setFixedHeight(paramsGB.sizeHint().height())
            layout.addWidget(paramsGB)

            outputGB = CollapseGB()
            outputGB.setTitle("Output")
            outputGB.setLayout(QFormLayout())
            outputGB.layout().addRow(QLabel("File Path:"), QLineEdit('Implement me'))
            outputGB.setFixedHeight(outputGB.sizeHint().height())
            layout.addWidget(outputGB)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ != "MVNode_S_UUID":
            self.gr_node.setToolTip("Input should be UUID node")
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

        if self.uuid_line_edit:
            self.uuid_line_edit.setText(val)

        return val

    def getVal(self):
        return self._uuid if not self.isInvalid() else None

    def onTextChange(self):
        self._uuid = self.uuid_line_edit.text()
        output_node = self.getOutput(0)
        if output_node:
            output_node.eval()

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self._uuid
        res['params'] = {}
        res['params']['method_of_capture'] = self.method_of_capture_line.text()
        res['params']['mv_session'] = self.mv_session_line.text()
        res['params']['drop_ir'] = self.dropir_cb.currentIndex()
        res['params']['no_join'] = self.no_join_cb.currentIndex()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.uuid_line_edit.setText(data['uuid'])
            self.method_of_capture_line.setText(data['params']['method_of_capture'])
            self.mv_session_line.setText(data['params']['mv_session'])
            self.dropir_cb.setCurrentIndex(data['params']['drop_ir'])
            self.no_join_cb.setCurrentIndex(data['params']['no_join'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
