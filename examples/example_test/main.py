
import sys
import inspect
from pathlib import Path
from PyQt5.QtWidgets import *

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipelineeditor.utils import loadStylesheet # noqa
from pipelineeditor.node_editor_window import NodeEditorWindow # noqa

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = NodeEditorWindow()
    module_apth = Path(inspect.getfile(window.__class__)).parent
    loadStylesheet(str(module_apth.joinpath("qss/node_style.qss")))

    sys.exit(app.exec_())
