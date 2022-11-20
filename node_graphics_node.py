from PyQt5.QtWidgets import *

class QDMGraphicsNode:
    def __init__(self, node, title) -> None:
        self.node = node
        self.title = title

        self.initUI()

    def initUI(self):
        pass