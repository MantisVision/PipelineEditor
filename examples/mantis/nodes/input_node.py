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
        res = super().deserialize(data, hashmap, restore_id)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dump_exception(e)
        return res


@register_nodes(OP_NODE_S_MVX_FILE)
class MVNode_S_MVX_File(MVInputNode):
    icon = str(current_file_path.joinpath(r"icons\mvx.png"))
    op_code = OP_NODE_S_MVX_FILE
    op_title = "MVX Source File"
    content_label = "MVX"
    content_label_obj_name = "mvx_source_node_bg"
    colaps_widget = None
    input_path = ""

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])
        self.file_line_edit = None
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
            frame.setLayout(QGridLayout())

            if not self.file_line_edit:
                self.file_line_edit = QLineEdit(self.input_path)
                self.file_line_edit.textChanged.connect(self.onTextChange)

            frame.layout().addWidget(QLabel("File path:"), 0, 0)
            frame.layout().addWidget(self.file_line_edit, 0, 1)
            browse_btn = QPushButton("...")
            browse_btn.setMaximumWidth(24)
            browse_btn.clicked.connect(self.BrowseFile)
            frame.layout().addWidget(browse_btn, 0, 2)
            frame.layout().setColumnStretch(1, 5)
            t.addWidget(frame)
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        if not self.input_path:
            self.markInvalid()
            self.markDescendantsDirty()
            self.gr_node.setToolTip("File wasn't selected")
            return

        if not Path(self.input_path).exists():
            self.markInvalid()
            self.markDescendantsDirty()
            self.gr_node.setToolTip("File wasn't found")
            return

        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.evalChildren()
        self.gr_node.setToolTip("")

        return self.input_path

    def BrowseFile(self):
        fname, ffilter = QFileDialog.getOpenFileName(None, "Open a MVX file")

        if not fname:
            return

        self.file_line_edit.setText(fname)

    def onTextChange(self):
        self.input_path = self.file_line_edit.text()
        self.eval()

    def setInputContent(self, val):
        self.file_line_edit.setText(val)

    def getVal(self):
        return self.input_path if not self.isInvalid() else None

    def serialize(self):
        res = super().serialize()
        res['uuid'] = ""
        res['params'] = {}
        res['params']['file_path'] = self.file_line_edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            value = data['params']['file_path']
            self.file_line_edit.setText(value)
            return True & res
        except Exception as e:
            dump_exception(e)
        return res


@register_nodes(OP_NODE_S_UUID)
class MVNode_S_UUID(MVInputNode):
    icon = str(current_file_path.joinpath(r"icons\uuid.png"))
    op_code = OP_NODE_S_UUID
    op_title = "UUID Source"
    content_label = "UUID"
    content_label_obj_name = "uuid_source_node_bg"
    colaps_widget = None
    _uuid = ""
    uuid_line_edit = None

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[], outputs=[3])
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
                self.uuid_line_edit = QLineEdit(self._uuid)
                self.uuid_line_edit.textChanged.connect(self.onTextChange)
            frame.layout().addRow(QLabel("UUID:"), self.uuid_line_edit)
            t.addWidget(frame)
            layout.addWidget(t)

        return self.colaps_widget

    def eval_impl(self):
        if not self._uuid:
            self.markInvalid()
            self.markDescendantsDirty()
            self.gr_node.setToolTip("UUID wasn't entered")
            return

        self.markDirty(False)
        self.markInvalid(False)

        self.gr_node.setToolTip("")

        self.evalChildren()

        return self._uuid

    def onTextChange(self):
        self._uuid = self.uuid_line_edit.text()
        self.eval()

    def getVal(self):
        return self._uuid if not self.isInvalid() else None

    def serialize(self):
        res = super().serialize()
        res['uuid'] = self.uuid_line_edit.text()
        res['params'] = {}
        res['params']['uuid'] = self.uuid_line_edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            value = data['params']['uuid']
            self.uuid_line_edit.setText(value)
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
