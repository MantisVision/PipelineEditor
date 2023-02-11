from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.calc_config import *
from examples.mantis.calc_node_base import *
from examples.mantis.nodes.colap import FrameLayout, CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_O_HARVEST)
class CalcNode_Harvest(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_O_HARVEST
    op_title = "Harvest"
    content_label = "Harvest"
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
            self.colaps_widget.setMinimumWidth(250)
            self.colaps_widget.setStyleSheet("")
            self.colaps_widget.setObjectName(str(self.id))
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)
            self.colaps_widget.setLayout(layout)

            t = FrameLayout(title=self.op_title)
            frame = QFrame()
            frame.setLayout(QFormLayout())

            if not self.uuid_line_edit:
                self.uuid_line_edit = QLineEdit()
                self.uuid_line_edit.setDisabled(True)
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

            t = CollapseGB()
            t.setTitle("Harvest")
            t.setLayout(QFormLayout())
            t.layout().addRow(QLabel("UUID:"), self.uuid_line_edit)
            t.layout().addRow(QLabel("Method of Capture:"), self.method_of_capture_line)
            t.layout().addRow(QLabel("MV Session:"), self.mv_session_line)
            t.layout().addRow(QLabel("DropIR:"), self.dropir_cb)
            t.layout().addRow(QLabel("No Join:"), self.no_join_cb)
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ != "CalcNode_S_UUID":
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

    def onTextChange(self):
        self._uuid = self.uuid_line_edit.text()
        output_node = self.getOutput(0)
        if output_node:
            output_node.eval()

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self.uuid_line_edit.text()
        res['method_of_capture'] = self.method_of_capture_line.text()
        res['mv_session'] = self.mv_session_line.text()
        res['drop_ir'] = self.dropir_cb.currentIndex()
        res['no_join'] = self.no_join_cb.currentIndex()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap)
        try:
            self.uuid_line_edit.setText(data['uuid'])
            self.method_of_capture_line.setText(data['method_of_capture'])
            self.mv_session_line.setText(data['mv_session'])
            self.dropir_cb.setCurrentIndex(data['drop_ir'])
            self.no_join_cb.setCurrentIndex(data['no_join'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res


@register_nodes(OP_NODE_O_JOIN)
class CalcNode_Join(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_O_JOIN
    op_title = "JOIN"
    content_label = "JOIN"
    content_label_obj_name = "join_o_node_bg"
    colaps_widget = None
    output_path = ""
    uuid_line_edit = None
    _uuid = ""

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[2], outputs=[2])
        self.createParamWidget()

    def createParamWidget(self):
        if not self.colaps_widget:
            if not self.colaps_widget:
                self.colaps_widget = QWidget()
                self.colaps_widget.setMinimumWidth(250)
                self.colaps_widget.setStyleSheet("")
                self.colaps_widget.setObjectName(str(self.id))
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)
            self.colaps_widget.setLayout(layout)

            if not self.uuid_line_edit:
                self.uuid_line_edit = QLineEdit("")
                self.uuid_line_edit.setReadOnly(True)
                self.uuid_line_edit.textChanged.connect(self.onTextChange)

            t = CollapseGB()
            t.setTitle("File path")
            t.setLayout(QFormLayout())
            t.layout().addRow(QLabel("File: "), self.uuid_line_edit)
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return
        if input_node.__class__.__name__ not in ["CalcNode_S_UUID", "CalcNode_Harvest"]:
            self.gr_node.setToolTip("Input should be either UUID or Harvest node")
            if self.uuid_line_edit:
                self.uuid_line_edit.setText("")
            self.markInvalid()
            return

        val = input_node.eval()
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
            self.uuid_line_edit.setText(self.output_path)

        return self.output_path

    def onTextChange(self):
        self._uuid = self.uuid_line_edit.text()
        output_node = self.getOutput(0)
        if output_node:
            output_node.eval()

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self.uuid_line_edit.text()
        res['output_path'] = self.output_path
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap)
        try:
            value = data['uuid']
            self.uuid_line_edit.setText(value)
            return True & res
        except Exception as e:
            dump_exception(e)
        return res

@register_nodes(OP_NODE_O_UPLOAD)
class CalcNode_Upload(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_O_UPLOAD
    op_title = "UPLOAD"
    content_label = "UPLOAD"
    content_label_obj_name = "upload_o_node_bg"
    colaps_widget = None
    input_path = ""
    input_path_line_edit = ""

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

            if not self.input_path_line_edit:
                self.input_path_line_edit = QLineEdit()
                self.input_path_line_edit.setReadOnly(True)
                self.input_path_line_edit.textChanged.connect(self.onTextChange)

            t = CollapseGB()
            t.setTitle("File path")
            t.setLayout(QFormLayout())
            t.layout().addRow(QLabel("File Path:"), self.input_path_line_edit)
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)
        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ not in ["CalcNode_S_MVX_File", "CalcNode_Join"]:
            self.gr_node.setToolTip("Input should be either MVX file or Join node")
            if self.input_path_line_edit:
                self.input_path_line_edit.setText("")
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

        return self.input_path

    def onTextChange(self):
        self.input_path = self.input_path_line_edit.text()
        self.eval()


@register_nodes(OP_NODE_O_TSDF)
class CalcNode_TSDF(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
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

            dropir_cb = QComboBox()
            dropir_cb.setObjectName("dropir_cb")
            dropir_cb.setMaximumWidth(60)
            dropir_cb.addItems(["True", "False"])
            no_join_cb = QComboBox()
            no_join_cb.setObjectName("no_join_cb")
            no_join_cb.addItems(["True", "False"])
            no_join_cb.setMaximumWidth(60)
            scale = QLineEdit()
            scale.setMaximumWidth(60)
            fps_cb = QComboBox()
            fps_cb.setObjectName("no_join_cb")
            fps_cb.addItems(["5", "10", "15", "20", "25"])
            fps_cb.setCurrentText("25")
            fps_cb.setMaximumWidth(40)
            t = CollapseGB()
            t.setTitle("Harvest")
            t.setLayout(QFormLayout())
            t.layout().addRow(QLabel("File Path:"), self.input_path_line_edit)
            t.layout().addRow(QLabel("Client:"), QLineEdit())
            t.layout().addRow(QLabel("Build:"), QLineEdit())
            t.layout().addRow(QLabel("Scale:"), scale)
            t.layout().addRow(QLabel("Atlas Size:"), QLineEdit())
            t.layout().addRow(QLabel("FPS:"), fps_cb)
            t.layout().addRow(QLabel("Additional Params:"), QLineEdit())
            t.layout().addRow(QCheckBox("Segmented"))
            t.layout().addRow(QCheckBox("Local"))
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

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


@register_nodes(OP_NODE_O_AUDIO)
class CalcNode_T_MVX_File(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\out.png"))
    op_code = OP_NODE_O_AUDIO
    op_title = "Audio"
    content_label = "AUDIO"
    content_label_obj_name = "wav_o_audio_node_bg"
    colaps_widget = None
    file_line_edit = ""
    input_path = ""
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
            t.setLayout(QFormLayout())

            if not self.file_line_edit:
                self.file_line_edit = QLineEdit(self.input_path)
                self.file_line_edit.setReadOnly(True)
                self.file_line_edit.textChanged.connect(self.onTextChange)

            t.layout().addRow(QLabel("File path:"), self.file_line_edit)
            t.setFixedHeight(t.sizeHint().height())
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        input_node = self.getInput(0)

        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ != "CalcNode_S_UUID":
            self.gr_node.setToolTip("Input should be UUID node")
            if self.file_line_edit:
                self.file_line_edit.setText("")
            self.markInvalid()
            return

        # val = input_node.eval()
        val = input_node.getVal()

        if val is None:
            self.gr_node.setToolTip("Not a valid UUID")
            if self.file_line_edit:
                self.file_line_edit.setText("")
            self.markInvalid()
            return

        self.markDirty(False)
        self.markInvalid(False)
        self.gr_node.setToolTip("")

        self.output_path = fr"C:\HARVEST\{val}\{val}.wav"

        if self.file_line_edit:
            self.file_line_edit.setText(self.output_path)

        return self.output_path

    def onTextChange(self):
        self.input_path = self.file_line_edit.text()
        self.eval()
