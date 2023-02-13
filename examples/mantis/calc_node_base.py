from PyQt5.QtWidgets import *
from pathlib import Path
from pipelineeditor.node_node import Node
from pipelineeditor.node_content_widget import QDMNodeContentWidget
from pipelineeditor.graphics.node_graphics_node import QDMGraphicsNode
from pipelineeditor.node_socket import *
from pipelineeditor.utils import dump_exception


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 8
        self.edge_padding = 0
        self._title_horizontal_padding = 8
        self._title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        current_file_path = Path(__file__).parent
        self.icons = QImage(str(current_file_path.joinpath(r"icons/status_icons.png")))

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24
        if self.node.isDirty():
            offset = 0
        if self.node.isInvalid():
            offset = 48

        painter.drawImage(
            QRectF(-10, -10, 24, 24),
            self.icons,
            QRectF(offset, 0, 24, 24)
        )


class CalcContentWidget(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_obj_name)


class CalcNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_obj_name = "calc_node_bg"

    def __init__(self, scene, inputs=[2, 2], outputs=[1]) -> None:
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None

        # mark all nodes by default to dirty
        self.markDirty()

    def initInnerClasses(self):
        self.content = CalcContentWidget(self)
        self.gr_node = CalcGraphicsNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def eval_operation(self, input1, input2):
        return 123

    def eval_impl(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if not i1 or not i2:
            self.markInvalid()
            self.markDescendantsDirty()
            self.gr_node.setToolTip("Connecet all inputs")
            return None
        else:
            val = self.eval_operation(i1.eval(), i2.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.gr_node.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()

            return val

    def eval(self):
        # Eval only when node is either dirty or invalid
        # if not self._is_dirty and not self._is_invalid:
        #     return self.value

        try:
            val = self.eval_impl()
            return val
        except ValueError as e:
            self.markInvalid()
            self.gr_node.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.gr_node.setToolTip(str(e))
            dump_exception(e)

    def onInputChanged(self, new_edge):
        self.markDirty()
        self.eval()

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        # print(f"Deserialize CalcNode {self.__class__.__name__} res: {res}")
        return res
