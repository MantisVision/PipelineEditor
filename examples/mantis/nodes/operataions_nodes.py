from PyQt5.QtCore import *
from pathlib import Path
from examples.mantis.calc_config import *
from examples.mantis.calc_node_base import *
from examples.mantis.nodes.colap import FrameLayout, CollapseGB
from pipelineeditor.utils import dump_exception
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\add.png"))
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_obj_name = "calc_node_bg"

    def eval_operation(self, input1, input2):
        return input1 + input2


@register_nodes(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\sub.png"))
    op_code = OP_NODE_SUB
    op_title = "Subtract"
    content_label = "-"
    content_label_obj_name = "calc_node_bg"

    def eval_operation(self, input1, input2):
        return input1 - input2


@register_nodes(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\mul.png"))
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_obj_name = "calc_node_mul"

    def eval_operation(self, input1, input2):
        return input1 * input2


@register_nodes(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\divide.png"))
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_obj_name = "calc_node_div"
    colaps_widget = None

    def eval_operation(self, input1, input2):
        return input1 / input2

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


@register_nodes(OP_NODE_TEST)
class CalcNode_Test(CalcNode):
    icon = str(current_file_path.joinpath(r"icons\test.png"))
    op_code = OP_NODE_TEST
    op_title = "TEST"
    content_label = "TEST"
    content_label_obj_name = "calc_node_bg"
    colaps_widget = None

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

            dropir_cb = QComboBox()
            dropir_cb.setObjectName("dropir_cb")
            dropir_cb.setMaximumWidth(60)
            dropir_cb.addItems(["True", "False"])
            no_join_cb = QComboBox()
            no_join_cb.setObjectName("no_join_cb")
            no_join_cb.addItems(["True", "False"])
            no_join_cb.setMaximumWidth(60)
            t = CollapseGB()
            t.setTitle("Harvest")
            t.setLayout(QFormLayout())
            t.layout().addRow(QLabel("UUID:"), self.uuid_line_edit)
            t.layout().addRow(QLabel("Method of Capture:"), QLineEdit())
            t.layout().addRow(QLabel("MV Session:"), QLineEdit())
            t.layout().addRow(QLabel("DropIR:"), dropir_cb)
            t.layout().addRow(QLabel("No Join:"), no_join_cb)
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

        if self.uuid_line_edit:
            self.uuid_line_edit.setText(val)

        return val

    def onTextChange(self):
        self._uuid = self.uuid_line_edit.text()
        output_node = self.getOutput(0)
        if output_node:
            output_node.eval()


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

            t = FrameLayout(title=self.op_title)
            frame = QFrame()
            frame.setLayout(QFormLayout())

            if not self.input_path_line_edit:
                self.input_path_line_edit = QLineEdit()
                self.input_path_line_edit.setReadOnly(True)
                self.input_path_line_edit.textChanged.connect(self.onTextChange)

            frame.layout().addRow(QLabel("File Path:"), self.input_path_line_edit)
            t.addWidget(frame)
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

        val = input_node.eval()

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