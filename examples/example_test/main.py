
import sys
import inspect
from pathlib import Path
from pipelineeditor.utils import loadStylesheet
from pipelineeditor.node_editor_window import NodeEditorWindow
from PyQt5.QtWidgets import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = NodeEditorWindow()
    module_apth = Path(inspect.getfile(window.__class__)).parent
    loadStylesheet(str(module_apth.joinpath("qss/node_style.qss")))

    sys.exit(app.exec_())
