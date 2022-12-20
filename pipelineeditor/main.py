import sys
from pathlib import Path
from PyQt5.QtWidgets import *

sys.path.insert(0, str(Path(__file__).parent.parent))
from node_editor_window import NodeEditorWindow # noqa


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = NodeEditorWindow()

    sys.exit(app.exec_())
