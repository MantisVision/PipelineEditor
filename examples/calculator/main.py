import sys
from calc_window import CalculatorWindow
from PyQt5.QtWidgets import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec_())
