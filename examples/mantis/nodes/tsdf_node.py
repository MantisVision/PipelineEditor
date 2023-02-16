from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.calc_config import *
from examples.mantis.calc_node_base import *
from examples.mantis.nodes.colap import CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_O_TSDF)
class CalcNode_TSDF(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\ops.png"))
    op_code = OP_NODE_O_TSDF
    op_title = "TSDF"
    content_label = "TSDF"
    content_label_obj_name = "tsdf_o_node_bg"
    colaps_widget = None
    input_path_line_edit = None
    input_path = ""
    output_path = ""

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[2], outputs=[2])
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

            if not self.input_path_line_edit:
                self.input_path_line_edit = QLineEdit()
                self.input_path_line_edit.setDisabled(True)
                self.input_path_line_edit.textChanged.connect(self.onTextChange)

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

        if input_node.__class__.__name__ not in ["CalcNode_S_MVX_File", "CalcNode_Join"]:
            self.gr_node.setToolTip("Input should be either MVX file or Join node")
            if self.input_path_line_edit:
                self.input_path_line_edit.setText("")
            self.markInvalid()
            return

        if not output_node:
            self.gr_node.setToolTip("Output node not connected")
            self.markInvalid()
            return

        if output_node.__class__.__name__ not in ["CalcNode_T_MVX_File"]:
            self.gr_node.setToolTip("Output should be MVX file")
            self.markInvalid()
            return

        val = input_node.getVal()

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
        res['uuid'] = ""
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
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap)
        try:
            self.input_path_line_edit.setText(data['file_path'])
            self.client.setText(data['client'])
            self.build.setText(data['build'])
            self.scale.setText(data['scale'])
            self.atlas_size.setText(data['atlas_size'])
            self.fps_cb.setCurrentText(data['fps'])
            self.add_params.setText(data['add_params'])
            self.local_cb.setChecked(data['local'])
            self.segmented_cb.setChecked(data['segmented'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
