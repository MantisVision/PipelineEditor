import sys
from pathlib import Path
from PyQt5.QtWidgets import *

sys.path.insert(0, str(Path(__file__).parent.parent))
from mv_window import MantisWindow # noqa

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MantisWindow()
    window.show()

    sys.exit(app.exec_())
