import sys
from pipelineeditor.node_editor_window import NodeEditorWindow
from PyQt5.QtWidgets import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = NodeEditorWindow()

    sys.exit(app.exec_())
