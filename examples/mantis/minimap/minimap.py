import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initial_pixmap = QPixmap(r"C:\Personal\PipelineEditor\test.png")
        self.initial_pixmap.fill(Qt.white)
        self.current_pixmap = self.initial_pixmap.copy()
        self.current_pixmap.fill(Qt.white)
        self.window_width, self.window_height = self.initial_pixmap.width(), self.initial_pixmap.height()
        self.setMinimumSize(self.window_width, self.window_height)
        self.mid_point = QPoint(self.window_width // 2, self.window_height // 2)
        self.roi_width, self.roi_height = self.window_height // 2,  self.window_height // 4

        self.pixmap = QPixmap(self.rect().size())
        self.pixmap.fill(Qt.white)

        self._color = QColor("#FF4433")
        self._width = 3

        self._pen = QPen(self._color)
        self._pen.setWidthF(self._width)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.begin, self.destination = QPoint(), QPoint()

        self.CalcRectFromMid(self.mid_point)

        self.roi_painter = QPainter(self.pixmap)
        self.roi_painter.setPen(self._pen)
        self.roi_painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.roi_painter.drawRect(self.rect_roi.normalized())
        self.update()

    def paintEvent(self, event):
        self.pixmap.fill(Qt.white)
        self.drawScene()
        # painter = QPainter(self)
        # painter.drawPixmap(QPoint(), self.pixmap)

    def drawScene(self):
        # self.pixmap.fill(Qt.white)

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  1))
        painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        painter.drawRect(40, 40, 400, 200)
        self.paintROI()
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            print('Point 1')
            print(event.pos())

            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()

            if not self.isRectInBounds(self.destination):
                return

            self.CalcRectFromMid(self.destination)
            self.paintROI()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            print('Point 3')
            self.paintROI()

    def paintROI(self):
        self.roi_painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.roi_painter.setPen(self._pen)
        self.roi_painter.drawRect(self.rect_roi.normalized())
        self.update()

    def CalcRectFromMid(self, point):
        self.roi_top_left  = QPoint(point.x() - self.roi_width // 2, point.y() - self.roi_height // 2)
        self.roi_bot_right = QPoint(point.x() + self.roi_width // 2, point.y() + self.roi_height // 2)
        self.rect_roi = QRect(self.roi_top_left, self.roi_bot_right)

    def isRectInBounds(self, point):
        if point.x() - self.roi_width // 2 < 0:
            return False
        if point.y() - self.roi_height // 2 < 0:
            return False
        if point.x() + self.roi_width // 2 > self.window_width:
            return False
        if point.y() + self.roi_height // 2 > self.window_height:
            return False
        return True

    def pointInRect(self, point):
        x1, y1, w, h = self.rect_roi.getRect()
        x2, y2 = x1 + w, y1 + h
        x, y = point.x(), point.y()
        if (x1 < x and x < x2):
            if (y1 < y and y < y2):
                return True
        return False


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')