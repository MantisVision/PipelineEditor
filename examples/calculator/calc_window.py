import sys
import json
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipelineeditor.utils import dump_exception # noqa
from pipelineeditor.utils import loadStylesheets # noqa
from pipelineeditor.node_editor_window import NodeEditorWindow # noqa
from examples.calculator.calc_sub_window import CalculatorSubWindow # noqa


class CalculatorWindow(NodeEditorWindow):

    def initUI(self):
        self.author_name = "ZikriBen"
        self.module_name = "Pipeline Editor - Calculator"

        loadStylesheets(
            str(Path(__file__).parent.joinpath("qss/nodeeditor-dark.qss")),
            str(Path(__file__).parent.joinpath("qss/nodeeditor.qss")),
        )

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)

        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.createNodeDock()

        self.readSettings()

        self.setWindowTitle("Calculator Example")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)
        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)
        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

    def updateMenus(self):
        active = self.activeMdiChild()
        hasMdiChild = active is not None

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setEnabled(hasMdiChild)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendltFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createNodeDock(self):
        self.listWidget = QListWidget()
        self.listWidget.addItem("Add")
        self.listWidget.addItem("Substract")
        self.listWidget.addItem("Multiply")
        self.listWidget.addItem("Divide")

        self.items = QDockWidget("Nodes")
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def readSettings(self):
        settings = QSettings(self.author_name, self.module_name)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        dockSize = settings.value('dockSize', QSize(20, 20))
        self.move(pos)
        self.resize(size)
        self.listWidget.resize(dockSize)

    def writeSettings(self):
        settings = QSettings(self.author_name, self.module_name)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue('dockSize', self.listWidget.size())

    def getcurrentPipelineEditorWidget(self):
        return self.activeMdiChild()

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        sub_window = self.createMdiChild()
        sub_window.show()

    def onFileOpen(self):
        fnames, ffilter = QFileDialog.getOpenFileNames(self, "Open pipeline from file")
        try:
            for fname in fnames:
                existing = self.findMdiChild(fname)
                if existing:
                    self.mdiArea.setActiveSubWindow(existing)
                else:
                    pipeline_editor = CalculatorSubWindow()
                    if pipeline_editor.fileLoad(fname):
                        self.statusBar().showMessage(f"File {fname} opened successfully.")
                        pipeline_editor.setTitle()
                        sub_window = self.mdiArea.addSubWindow(pipeline_editor)
                        sub_window.show()
                    else:
                        pipeline_editor.close()
        except Exception as e:
            dump_exception(e)

    # def onFileSave(self):
    #     current_editor = self.getcurrentPipelineEditorWidget()
    #     if current_editor:
    #         if not current_editor.isFilenameSet():
    #             return self.onFileSaveAs()
    #         else:
    #             current_editor.fileSave()
    #             current_editor.setTitle()
    #             self.statusBar().showMessage(f"Successfully saved to {current_editor.filename}")
    #             return True

    def onFileSaveAs(self):
        current_editor = self.activeMdiChild()
        if current_editor:
            fname, ffilter = QFileDialog.getSaveFileName(self, "Save pipeline to file")

            if not fname:
                return False

            current_editor.fileSave(fname)
            current_editor.setTitle()
            self.statusBar().showMessage(f"Successfully saved to {fname}")

            return True

    def createMdiChild(self):
        pipeline_editor = CalculatorSubWindow()
        sub_window = self.mdiArea.addSubWindow(pipeline_editor)
        return sub_window

    def findMdiChild(self, fname):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == fname:
                return window
        return None

    def about(self):
        QMessageBox.about(
            self,
            "About Piepline Editor",
            "The <b>Piepline Editor</b> calculator example demonstrates how to write multiple "
            "document interface applications using Qt. For more information please visit: "
            "<a href='https://github.com/ZikriBen/pipelineeditor'> Git Repository</a>"
        )
