import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from pathlib import Path

class Example(QtWidgets.QWidget):

    def __init__(self,):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        # formatting
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Example")

        # widgets
        self.controlGroup = QtWidgets.QGroupBox()
        self.controlGroup.setTitle("Group")
        self.controlGroup.setCheckable(True)
        self.controlGroup.setChecked(True)
        icons_root = (Path(__file__).parent.parent.joinpath("icons").as_posix())
        print(icons_root)
        self.controlGroup.setStyleSheet("QGroupBox::indicator { width: 20px; height: 20px; }"
                       "QGroupBox::indicator:unchecked { image: url(" + f"{icons_root}/small_arrow_right.png); " + "}"
                       "QGroupBox::indicator:checked { image: url(" + f"{icons_root}/small_arrow_down.png); " + "}")
        # groupbox icons
        self.groupLayout = QtWidgets.QGridLayout(self.controlGroup)
        self.btn = QtWidgets.QPushButton("FOO")
        self.groupLayout.addWidget(self.btn)
        self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())

        # signals
        self.controlGroup.toggled.connect(lambda: self.toggleGroup(self.controlGroup))

        # layout
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.mainLayout.addWidget(self.controlGroup)
        self.show()   

    def toggleGroup(self, ctrl):
        state = ctrl.isChecked()
        if state:
            ctrl.setFixedHeight(ctrl.sizeHint().height())
        else:
            ctrl.setFixedHeight(30)


# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())