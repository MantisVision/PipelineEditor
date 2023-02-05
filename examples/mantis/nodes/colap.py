import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FrameLayout(QWidget):
    def __init__(self, parent=None, title=None):
        QFrame.__init__(self, parent=parent)
        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QVBoxLayout(self)
        self._main_v_layout.setSpacing(0)
        self._main_v_layout.setContentsMargins(0, 0, 0, 0)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))
        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QWidget()
        self._content_layout = QVBoxLayout()
        self._content_layout.setSpacing(0)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        self._title_frame.clicked.connect(self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        # set Title size base on collaps
        # self._title_frame.setMinimumHeight([50, 25][int(self._is_collasped)])
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QPushButton):
        def __init__(self, parent=None, title="", collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(24)  # height of the button
            self.move(QPoint(24, 0))
            # self.setStyleSheet("border:2px solid rgb(41, 41, 41); ")
            self.setStyleSheet("border:0px; background:transparent;")
            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

        def initArrow(self, collapsed):
            self._arrow = FrameLayout.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QLabel(title)
            self._title.setMinimumHeight(17)
            self._title.move(QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

    #############################
    #           ARROW           #
    #############################
    class Arrow(QFrame):
        def __init__(self, parent=None, collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QPointF(7.0, 8.0), QPointF(17.0, 8.0), QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QPointF(8.0, 7.0), QPointF(13.0, 12.0), QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            painter = QPainter()
            painter.begin(self)
            painter.setBrush(QColor(192, 192, 192))
            painter.setPen(QColor(64, 64, 64))
            painter.drawPolygon(*self._arrow)
            painter.end()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    win = QMainWindow()
    w = QWidget()
    w.setMinimumWidth(350)
    win.setCentralWidget(w)
    l = QVBoxLayout()
    l.setSpacing(0)
    l.setAlignment(Qt.AlignTop)
    w.setLayout(l)

    t = FrameLayout(title="Buttons")
    t.addWidget(QPushButton('a'))
    t.addWidget(QPushButton('b'))
    t.addWidget(QPushButton('c'))

    f = FrameLayout(title="TableWidget")
    rows, cols = (6, 3)
    data = {'col1': ['1', '2', '3', '4', '5', '6'],
            'col2': ['7', '8', '9', '10', '11', '12'],
            'col3': ['13', '14', '15', '16', '17', '18']}
    table = QTableWidget(rows, cols)
    headers = []
    for n, key in enumerate(sorted(data.keys())):
        headers.append(key)
        for m, item in enumerate(data[key]):
            newitem = QTableWidgetItem(item)
            table.setItem(m, n, newitem)
    table.setHorizontalHeaderLabels(headers)
    f.addWidget(table)

    l.addWidget(t)
    l.addWidget(f)

    win.show()
    win.raise_()
    print("\2")
    sys.exit(app.exec_())