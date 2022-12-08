from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
from pathlib import Path
from node_editor_widget import NodeEditorWidget


class NodeEditorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.filename = None

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()

        filemenu = menubar.addMenu('&File')

        filemenu.addAction(self.createAct("&New", self.onFileNew, shortcut="Ctrl+N", tooltip="Create new pipeline"))
        filemenu.addSeparator()
        filemenu.addAction(self.createAct("&Open", self.onFileOpen, shortcut="Ctrl+O", tooltip="Open file"))
        filemenu.addAction(self.createAct("&Save", self.onFileSave, shortcut="Ctrl+S", tooltip="Save file"))
        filemenu.addAction(self.createAct("Save &As", self.onFileSaveAs, shortcut="Ctrl+Shift+S", tooltip="Save file as..."))
        filemenu.addSeparator()
        filemenu.addAction(self.createAct("E&xit", self.onExit, shortcut="ESC", tooltip="Exit application"))

        editmenu = menubar.addMenu('&Edit')
        editmenu.addAction(self.createAct("&Undo", self.onEditUndo, shortcut="Ctrl+Z", tooltip="Undo last operation"))
        editmenu.addAction(self.createAct("&Redo", self.onEditRedo, shortcut="Ctrl+Y", tooltip="Redo last operation"))
        editmenu.addSeparator()
        editmenu.addAction(self.createAct("&Delete", self.onEditDelete, shortcut="Del", tooltip="Delete selected items"))

        node_editor = NodeEditorWidget(self)
        self.setCentralWidget(node_editor)

        self.statusBar().showMessage("")
        self.statusBar().setStyleSheet('QStatusBar::item {border: None;}')
        self.status_mouse_pos = QLabel("")
        self.status_bar_text = QLabel("")

        widget = QWidget(self)
        widget.setLayout(QHBoxLayout())
        widget.layout().addWidget(self.status_bar_text)
        spacerItem = QSpacerItem(800, 0, QSizePolicy.Preferred, QSizePolicy.Preferred)
        widget.layout().addItem(spacerItem)
        widget.layout().addWidget(self.status_mouse_pos)

        self.statusBar().addPermanentWidget(widget)
        # self.statusBar().addPermanentWidget(self.status_bar_text)
        node_editor.view.scenePosChanged.connect(self.onSceneChanged)

        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Pipeline Editor")
        self.show()

    def createAct(self, name, callback, shortcut="", tooltip=""):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)

        return act

    def onFileNew(self):
        self.centralWidget().scene.clear()

    def onFileOpen(self):
        fname, ffilter = QFileDialog.getOpenFileName(self, "Open pipeline from file")

        if not fname:
            return

        try:
            if Path(fname).exists():
                self.centralWidget().scene.load_from_file(fname)
                self.print_msg(f"File {fname} opened successfully.")
        except (KeyError, json.decoder.JSONDecodeError) as e:
            self.print_msg("The file might be corrupted, or not in the right format.", 'red')

    def onFileSave(self):
        if not self.filename:
            return self.onFileSaveAs()

        self.centralWidget().scene.save_to_file(self.filename)
        self.print_msg(f"Successfully saved to {self.filename}")

    def onFileSaveAs(self):
        fname, ffilter = QFileDialog.getSaveFileName(self, "Save pipeline to file")

        if not fname:
            return

        self.filename = fname
        self.onFileSave()

    def onExit(self):
        print("Exit")

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.gr_scene.views()[0].deleteSelected()

    def print_msg(self, msg, color='black', msecs=3000):
        QTimer.singleShot(msecs, lambda: self.status_bar_text.setText(""))
        self.status_bar_text.setStyleSheet(f"color : {color}")
        self.status_bar_text.setText(msg)

    def onSceneChanged(self, x, y):
        self.status_mouse_pos.setText(f"Scene Pos [{x}, {y}]")