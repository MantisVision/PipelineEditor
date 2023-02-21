from PyQt5.QtCore import *
from examples.mantis.mv_config import *
from examples.mantis.mv_node_base import *
from pathlib import Path
from pipelineeditor.utils import dump_exception
from examples.mantis.nodes.colap import CollapseGB
current_file_path = Path(__file__).parent.parent


@register_nodes(OP_NODE_T_MVX_FILE)
class MVNode_T_MVX_File(MVOutputNode):

    icon = str(current_file_path.joinpath(r"icons\mvx.png"))
    op_code = OP_NODE_T_MVX_FILE
    op_title = "MVX Target File"
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
            self.colaps_widget = self.createCollapsWidget()
            layout = self.colaps_widget.layout()

            t = CollapseGB()
            t.setTitle("Output")
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
        input_node = self.getInput()
        if input_node and not self.getInput().eval():
            self.markInvalid()
            self.gr_node.setToolTip("Input node is not vaild")
            return

    def serialize(self):
        res = super().serialize()
        res['uuid'] = ""
        res['params'] = {}
        res['params']['file_path'] = self.file_line_edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.file_line_edit.setText(data['params']['file_path'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res


@register_nodes(OP_NODE_T_WAV_FILE)
class MVNode_T_WAV_File(MVOutputNode):
    icon = str(current_file_path.joinpath(r"icons\wav.png"))
    op_code = OP_NODE_T_WAV_FILE
    op_title = "WAV Target File"
    content_label = "WAV"
    content_label_obj_name = "wav_target_node_bg"
    colaps_widget = None
    file_line_edit = ""
    output_path = ""

    def __init__(self, scene) -> None:
        super().__init__(scene, inputs=[1], outputs=[])
        self.createParamWidget()

    def createParamWidget(self):
        if not self.colaps_widget:
            self.colaps_widget = self.createCollapsWidget()
            layout = self.colaps_widget.layout()

            t = CollapseGB()
            t.setTitle("Output")
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
        input_node = self.getInput(0)

        if not input_node:
            self.gr_node.setToolTip("Not connected")
            self.markInvalid()
            return

        if input_node.__class__.__name__ != "MVNode_O_Audio":
            self.gr_node.setToolTip("Input should be Audio node")
            if self.uuid_line_edit:
                self.uuid_line_edit.setText("")
            self.markInvalid()
            return

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
        fname, ffilter = QFileDialog.getOpenFileName(None, "Open a WAV file")

        if not fname:
            return

        self.file_line_edit.setText(fname)

    def onTextChange(self):
        self.output_path = self.file_line_edit.text()
        input_node = self.getInput()
        if input_node and not self.getInput().eval():
            self.markInvalid()
            self.gr_node.setToolTip("Input node is not vaild")
            return

    def serialize(self):
        res = super().serialize()
        res['uuid'] = ""
        res['params'] = {}
        res['params']['file_path'] = self.file_line_edit.text()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.file_line_edit.setText(data['params']['file_path'])
            return True & res
        except Exception as e:
            dump_exception(e)
        return res
