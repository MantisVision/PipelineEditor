from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math


class QDMGraphicsScene(QGraphicsScene):
    itemSelected = pyqtSignal()
    itemsDeselected = pyqtSignal()

    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        self.grid_size = 20
        self.grid_squares = 5
        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self.pen_light = QPen(self._color_light)
        self.pen_light.setWidth(1)

        self.pen_dark = QPen(self._color_dark)
        self.pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect) -> None:
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []

        # Draw horizontal Lines (every self.grid_squares draw darker line)
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) == 0:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_light.append(QLine(x, top, x, bottom))

        # Draw vertical Lines (every self.grid_squares draw darker line)
        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) == 0:
                lines_dark.append(QLine(left, y, right, y))
            else:
                lines_light.append(QLine(left, y, right, y))

        painter.setPen(self.pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self.pen_dark)
        painter.drawLines(*lines_dark)
