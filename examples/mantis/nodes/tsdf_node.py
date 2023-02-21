from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.mv_config import *
from examples.mantis.mv_node_base import *
from examples.mantis.nodes.colap import CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_O_TSDF)
class MVNode_TSDF(MVOperationsNode):
    icon = str(current_file_path.joinpath(r"icons\ops.png"))
    op_code = OP_NODE_O_TSDF
    op_title = "TSDF"
    content_label = "TSDF"
    content_label_obj_name = "tsdf_o_node_bg"
    colaps_widget = None
    input_path_line_edit = None
    uuid_line_edit = None
    ow_uuid_line_edit = None
    input_path = ""
    output_path = ""

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[2], outputs=[2])
        self.createParamWidget()

    def createParamWidget(self):
        if not self.colaps_widget:
            self.colaps_widget = self.createCollapsWidget()
            layout = self.colaps_widget.layout()

            UuidGB = self.createUUIDCollapsGB(self.onTextChange)
            layout.addWidget(UuidGB)

            self.input_path_line_edit = QLineEdit()
            self.input_path_line_edit.setReadOnly(True)
            self.input_path_line_edit.textChanged.connect(self.onTextChange)

            self.ow_uuid_line_edit = QLineEdit()
            self.client = QLineEdit()
            self.build = QLineEdit()
            self.atlas_size = QLineEdit()
            self.add_params = QLineEdit()
            self.local_cb = QCheckBox("Local")
            self.local_cb.setObjectName("local_cb")
            self.segmented_cb = QCheckBox("Segmented")
            self.segmented_cb.setObjectName("segmented_cb")

            self.dropir_cb = QComboBox()
            self.dropir_cb.setObjectName("dropir_cb")
            self.dropir_cb.setMaximumWidth(60)
            self.dropir_cb.addItems(["True", "False"])

            self.no_join_cb = QComboBox()
            self.no_join_cb.setObjectName("no_join_cb")
            self.no_join_cb.addItems(["True", "False"])
            self.no_join_cb.setMaximumWidth(60)
            self.scale = QLineEdit()
            self.scale.setMaximumWidth(60)
            self.fps_cb = QComboBox()
            self.fps_cb.setObjectName("fps_cb")
            self.fps_cb.addItems(["5", "10", "15", "20", "25"])
            self.fps_cb.setCurrentText("25")
            self.fps_cb.setMaximumWidth(40)

            inputGB = CollapseGB()
            inputGB.setTitle("Input")
            inputGB.setLayout(QFormLayout())
            inputGB.layout().addRow(QLabel("File Path:"), self.input_path_line_edit)
            inputGB.setFixedHeight(inputGB.sizeHint().height())
            layout.addWidget(inputGB)

            paramsGB = CollapseGB()
            paramsGB.setTitle("Params")
            paramsGB.setLayout(QFormLayout())
            paramsGB.layout().addRow(QLabel("Client:"), self.client)
            paramsGB.layout().addRow(QLabel("Build:"), self.build)
            paramsGB.layout().addRow(QLabel("Scale:"), self.scale)
            paramsGB.layout().addRow(QLabel("Atlas Size:"), self.atlas_size)
            paramsGB.layout().addRow(QLabel("FPS:"), self.fps_cb)
            paramsGB.layout().addRow(QLabel("Overwrite UUID:"), self.ow_uuid_line_edit)
            paramsGB.layout().addRow(QLabel("Additional Params:"), self.add_params)
            paramsGB.layout().addRow(self.segmented_cb)
            paramsGB.layout().addRow(self.local_cb)
            paramsGB.setFixedHeight(paramsGB.sizeHint().height())
            layout.addWidget(paramsGB)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        output_node = self.getOutput(0)

        if not input_node:
            self.gr_node.setToolTip("Input node not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ not in ["MVNode_S_MVX_File", "MVNode_Join"]:
            self.gr_node.setToolTip("Input should be either MVX file or Join node")
            if self.input_path_line_edit:
                self.input_path_line_edit.setText("")
            self.markInvalid()
            return

        if not output_node:
            self.gr_node.setToolTip("Output node not connected")
            self.markInvalid()
            return

        if output_node.__class__.__name__ not in ["MVNode_T_MVX_File"]:
            self.gr_node.setToolTip("Output should be MVX file")
            self.markInvalid()
            return

        val = input_node.getVal()
        self._uuid = input_node.getUUID()
        self.uuid_line_edit.setText(self._uuid)

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
            self.gr_node.setToolTip("Input file wasn't found")
            return

        self.markDirty(False)
        self.markInvalid(False)
        self.gr_node.setToolTip("")

        if self.input_path_line_edit:
            self.input_path_line_edit.setText(val)

        val = output_node.eval()

        if val is None:
            self.gr_node.setToolTip("File output path is missing")
            if self.input_path_line_edit:
                self.input_path_line_edit.setText("")
            self.markInvalid()
            return

        self.output_path = val

        return self.output_path

    def onTextChange(self):
        self.input_path = self.input_path_line_edit.text()
        output_node = self.getOutput(0)
        if output_node:
            output_node.eval()

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self._uuid
        res['params'] = {}
        res['params']['file_path'] = self.input_path_line_edit.text()
        res['params']['client'] = self.client.text()
        res['params']['build'] = self.build.text()
        res['params']['scale'] = self.scale.text()
        res['params']['atlas_size'] = self.atlas_size.text()
        res['params']['fps'] = self.fps_cb.currentText()
        res['params']['add_params'] = self.add_params.text()
        res['params']['local'] = self.local_cb.isChecked()
        res['params']['segmented'] = self.segmented_cb.isChecked()
        res['params']['uuid'] = self.ow_uuid_line_edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.uuid_line_edit.setText(data['uuid'])
            self.input_path_line_edit.setText(data['params']['file_path'])
            self.client.setText(data['params']['client'])
            self.build.setText(data['params']['build'])
            self.scale.setText(data['params']['scale'])
            self.atlas_size.setText(data['params']['atlas_size'])
            self.fps_cb.setCurrentText(data['params']['fps'])
            self.add_params.setText(data['params']['add_params'])
            self.local_cb.setChecked(data['params']['local'])
            self.segmented_cb.setChecked(data['params']['segmented'])
            self.ow_uuid_line_edit.setText(data['params']['uuid'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
