import json
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_editor_widget import NodeEditorWidget


class NodeEditorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.filename = None

        self.initUI()

        # QApplication.instance().clipboard().dataChanged.connect(self.onClipboardChanged)

    def initUI(self):
        menubar = self.menuBar()

        filemenu = menubar.addMenu('&File')

        filemenu.addAction(self.createAct("&New", self.onFileNew, shortcut="Ctrl+N", tooltip="Create new pipeline"))
        filemenu.addSeparator()
        filemenu.addAction(self.createAct("&Open", self.onFileOpen, shortcut="Ctrl+O", tooltip="Open file"))
        filemenu.addAction(self.createAct("&Save", self.onFileSave, shortcut="Ctrl+S", tooltip="Save file"))
        filemenu.addAction(self.createAct("Save &As", self.onFileSaveAs, shortcut="Ctrl+Shift+S", tooltip="Save file as..."))
        filemenu.addSeparator()
        filemenu.addAction(self.createAct("E&xit", self.closeEvent, shortcut="ESC", tooltip="Exit application"))

        editmenu = menubar.addMenu('&Edit')
        editmenu.addAction(self.createAct("&Undo", self.onEditUndo, shortcut="Ctrl+Z", tooltip="Undo last operation"))
        editmenu.addAction(self.createAct("&Redo", self.onEditRedo, shortcut="Ctrl+Y", tooltip="Redo last operation"))
        editmenu.addAction(self.createAct("Cu&t", self.onEditCut, shortcut="Ctrl+X", tooltip="Cut Selected"))
        editmenu.addAction(self.createAct("&Copy", self.onEditCopy, shortcut="Ctrl+C", tooltip="Copy Selected"))
        editmenu.addAction(self.createAct("&Paste", self.onEditPaste, shortcut="Ctrl+V", tooltip="Paste Selected"))
        editmenu.addSeparator()
        editmenu.addAction(self.createAct("&Delete", self.onEditDelete, shortcut="Del", tooltip="Delete selected items"))

        node_editor = NodeEditorWidget(self)
        self.setCentralWidget(node_editor)
        node_editor.scene.add_has_been_modified_listener(self.changeTitle)

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
        node_editor.view.scenePosChanged.connect(self.onSceneChanged)

        self.setGeometry(200, 200, 800, 600)
        self.changeTitle()
        self.show()

    def changeTitle(self):
        title = "Pipeline Editor - "
        if not self.filename:
            title += "New"
        else:
            title += Path(self.filename).name
            print("ASDASD")

        if self.centralWidget().scene.has_been_modified:
            title += "*"

        self.setWindowTitle(title)

    def createAct(self, name, callback, shortcut="", tooltip=""):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)

        return act

    def onFileNew(self):
        if self.save_dlg:
            self.centralWidget().scene.clear()
            self.filename = None
            self.changeTitle()

    def onFileOpen(self):
        if self.save_dlg:
            fname, ffilter = QFileDialog.getOpenFileName(self, "Open pipeline from file")

            if not fname:
                return

            try:
                if Path(fname).exists():
                    self.centralWidget().scene.load_from_file(fname)
                    self.print_msg(f"File {fname} opened successfully.")
                    self.filename = fname
                    self.changeTitle()
            except (KeyError, json.decoder.JSONDecodeError) as e:
                self.print_msg("The file might be corrupted, or not in the right format.", 'red')

    def onFileSave(self):
        if not self.filename:
            return self.onFileSaveAs()

        self.centralWidget().scene.save_to_file(self.filename)
        self.print_msg(f"Successfully saved to {self.filename}")

        return True

    def onFileSaveAs(self):
        fname, ffilter = QFileDialog.getSaveFileName(self, "Save pipeline to file")

        if not fname:
            return False

        self.filename = fname
        return self.onFileSave()

    # def onExit(self):
    #     self.closeEvent()

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.gr_scene.views()[0].deleteSelected()

    def onEditCut(self):
        data = self.centralWidget().scene.clipboard.serializedSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.centralWidget().scene.clipboard.serializedSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()
        try:
            data = json.loads(raw_data)
        except Exception as e:
            print(e)
            return

        if 'nodes' not in data:
            print("Json is not contain any node")
            return

        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)

    def print_msg(self, msg, color='black', msecs=3000):
        QTimer.singleShot(msecs, lambda: self.status_bar_text.setText(""))
        self.status_bar_text.setStyleSheet(f"color : {color}")
        self.status_bar_text.setText(msg)

    def onSceneChanged(self, x, y):
        self.status_mouse_pos.setText(f"Scene Pos [{x}, {y}]")

    def is_modified(self):
        return self.centralWidget().scene.has_been_modified

    def closeEvent(self, event) -> None:
        if self.save_dlg():
            event.accept()
        else:
            event.ignore()

    def save_dlg(self):
        if not self.is_modified():
            return True

        res = QMessageBox.warning(self, "Pipeline Editor Alert", "The document has been modified.\nDo you want to save your changes?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    # def onClipboardChanged(self):
    #     clip = QApplication.instance().clipboard()
    #     clip.setText("12123123")
    #     print(clip.text())