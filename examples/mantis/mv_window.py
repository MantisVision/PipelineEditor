import sys
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from examples.mantis.mv_config import *                        # noqa
from examples.mantis.mv_sub_window import MVSubWindow          # noqa
from pipelineeditor.node_editor_window import NodeEditorWindow # noqa
from examples.mantis.mv_node_base import *                     # noqa
from examples.mantis.mv_drag_listbox import QDMDragListBox     # noqa
from examples.mantis.nodes.colap import CollapseGB             # noqa
from pipelineeditor.utils import loadStylesheets               # noqa
from pipelineeditor.utils import dump_exception, pp            # noqa
from minimap.minimap_child import MinimapChild                 # noqa
from qss import nodeeditor_dark_resources                      # noqa


class MantisWindow(NodeEditorWindow):

    def initUI(self):
        self.author_name = "ZikriBen"
        self.module_name = "Pipeline Editor - Mantis"

        loadStylesheets(
            str(Path(__file__).parent.joinpath("qss/nodeeditor-dark.qss")),
            str(Path(__file__).parent.joinpath("qss/calc_nodeeditor.qss"))
        )

        self.empty_icon = QIcon(".")

        print("Registered Nodes:")
        pp(MV_NODES)

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

        self.createNodeDock()
        # self.createMinimapDock()
        self.createParameterDock()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.createStatusBar()

        widget = QWidget(self)
        widget.setLayout(QHBoxLayout())
        spacerItem = QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Preferred)
        widget.layout().addWidget(self.status_bar_text)
        widget.layout().addItem(spacerItem)
        widget.layout().addWidget(self.status_mouse_pos)

        self.statusBar().addPermanentWidget(widget)
        self.readSettings()

        self.setWindowTitle("Mantis Pipeline Editor")
        print(str(Path(__file__).joinpath(r"icons\mv_favicon.ico")))
        self.setWindowIcon(QIcon(str(Path(__file__).parent.joinpath(r"icons\mv_favicon.ico"))))

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            import sys
            sys.exit(0)

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
        self.menubar = self.menuBar()
        self.createFileMenu()
        self.createEditMenu()
        self.createWindowMenu()
        self.createRunMenu()
        self.createHelpMenu()

        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        self.editMenu.aboutToShow.connect(self.updateEditMenu)
        self.runMenu.aboutToShow.connect(self.updateRunMenu)

    def createWindowMenu(self):
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()

    def createHelpMenu(self):
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
        self.updateEditMenu()

    def updateMinimap(self):
        print("update minimap")
        pipeline_editor = self.getcurrentPipelineEditorWidget()
        if pipeline_editor:
            self.minimap.scene.deserialize(pipeline_editor.scene.serialize())

    def updateEditMenu(self):
        try:
            active = self.activeMdiChild()
            hasMdiChild = active is not None

            self.actPaste.setEnabled(hasMdiChild)
            self.actSelectAll.setEnabled(hasMdiChild)
            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e:
            dump_exception(e)

    def updateRunMenu(self):
        try:
            active = self.activeMdiChild()
            hasMdiChild = active is not None
            self.onEvalSelected.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.onEvalAll.setEnabled(hasMdiChild)
            self.actBake.setEnabled(hasMdiChild)
        except Exception as e:
            dump_exception(e)

    def updateWindowMenu(self):
        self.windowMenu.clear()

        nodes_toolbar = self.windowMenu.addAction("Nodes Toolbar")
        nodes_toolbar.setCheckable(True)
        nodes_toolbar.triggered.connect(self.onNodeWindowToolbar)
        nodes_toolbar.setChecked(self.nodes_dock.isVisible())

        self.windowMenu.addSeparator()
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

    def onEditDelete(self):
        # Hide param_dock widget if deleted node colaps widget is attached to it
        active_mdi_child = self.activeMdiChild()
        selected = active_mdi_child.scene.gr_scene.selectedItems()
        for sel in selected:
            if hasattr(sel, "node") and hasattr(sel.node, "colaps_widget"):
                if sel.node.colaps_widget == self.param_dock.widget():
                    self.param_dock.hide()
                    break

        return super().onEditDelete()

    def onNodeWindowToolbar(self):
        if self.nodes_dock.isVisible():
            self.nodes_dock.hide()
        else:
            self.nodes_dock.show()

    def onNodeClick(self, event):
        active_mdi_child = self.activeMdiChild()
        selected = active_mdi_child.scene.gr_scene.selectedItems()
        if selected:
            node = selected[0].node
            self.param_dock.setWidget(node.createParamWidget())
            self.param_dock.setVisible(True)

    def createToolBars(self):
        pass

    def createNodeDock(self):
        self.nodes_dock = QDockWidget("Nodes")
        self.nodes_list_widget = QDMDragListBox([OP_NODE_S_MVX_FILE, OP_NODE_S_UUID])
        self.nodes_list_widget.verticalScrollBar().hide()
        self.nodes_list_widget2 = QDMDragListBox([OP_NODE_O_HARVEST, OP_NODE_O_JOIN, OP_NODE_O_UPLOAD, OP_NODE_O_TSDF, OP_NODE_O_AUDIO])
        self.nodes_list_widget2.verticalScrollBar().hide()
        self.nodes_list_widget3 = QDMDragListBox([OP_NODE_T_MVX_FILE, OP_NODE_T_WAV_FILE])
        self.nodes_list_widget3.verticalScrollBar().hide()

        frame = QFrame()
        frame.setLayout(QVBoxLayout())
        frame.layout().setSpacing(10)
        frame.layout().setAlignment(Qt.AlignTop)

        input_nodes_gb = CollapseGB(self.nodes_list_widget.sizeHintForRow(0) * (self.nodes_list_widget.count() + 1), list_nodes=True)
        input_nodes_gb.setTitle("Input Nodes")
        input_nodes_gb.setLayout(QVBoxLayout())
        input_nodes_gb.layout().setContentsMargins(0, 0, 0, 0)
        input_nodes_gb.layout().addWidget(self.nodes_list_widget)
        frame.layout().addWidget(input_nodes_gb)

        ops_nodes_gb = CollapseGB(self.nodes_list_widget2.sizeHintForRow(0) * (self.nodes_list_widget2.count() + 1), list_nodes=True)
        ops_nodes_gb.setTitle("Operation Nodes")
        ops_nodes_gb.setLayout(QVBoxLayout())
        ops_nodes_gb.layout().setContentsMargins(0, 0, 0, 0)
        ops_nodes_gb.layout().addWidget(self.nodes_list_widget2)
        frame.layout().addWidget(ops_nodes_gb)

        output_nodes_gb = CollapseGB(self.nodes_list_widget3.sizeHintForRow(0) * (self.nodes_list_widget3.count() + 1), list_nodes=True)
        output_nodes_gb.setTitle("Output Nodes")
        output_nodes_gb.setLayout(QVBoxLayout())
        output_nodes_gb.layout().setContentsMargins(0, 0, 0, 0)
        output_nodes_gb.layout().addWidget(self.nodes_list_widget3)
        frame.layout().addWidget(output_nodes_gb)

        self.nodes_dock.setWidget(frame)
        self.nodes_dock.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.nodes_dock)

    def createMinimapDock(self):
        self.minimap = MinimapChild()
        self.minimap.setMaximumWidth(270)
        self.minimap.setMaximumHeight(200)
        self.minimap.fileLoad(r"C:\Personal\PipelineEditor\examples\mantis\flow.json")

        self.minimap_dock = QDockWidget("Minimap")
        self.minimap_dock.setWidget(self.minimap)
        self.minimap_dock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.minimap_dock)
        self.minimap_dock.setVisible(True)

    def createParameterDock(self):
        self.colaps_widget = QWidget()
        self.colaps_widget.setMinimumHeight(10)
        self.colaps_widget.setMinimumWidth(270)

        self.param_dock = QDockWidget("Parameter")
        self.param_dock.setWidget(self.colaps_widget)
        self.param_dock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.param_dock)
        self.param_dock.setVisible(False)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusBar().setStyleSheet('QStatusBar::item {border: None;}')
        self.status_mouse_pos = QLabel("")
        self.status_bar_text = QLabel("")

    def readSettings(self):
        settings = QSettings(self.author_name, self.module_name)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        dockSize = settings.value('dockSize', QSize(20, 20))
        self.move(pos)
        self.resize(size)
        self.nodes_list_widget.resize(dockSize)

    def writeSettings(self):
        settings = QSettings(self.author_name, self.module_name)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue('dockSize', self.nodes_list_widget.size())

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
        try:
            sub_window = self.createMdiChild()
            sub_window.widget().fileNew()
            sub_window.show()
        except Exception as e:
            dump_exception(e)

    def onFileOpen(self):
        fnames, ffilter = QFileDialog.getOpenFileNames(self, "Open pipeline from file", self.getFileDialogDirectory(), self.getFileDialogFilter())
        try:
            for fname in fnames:
                existing = self.findMdiChild(fname)
                if existing:
                    self.mdiArea.setActiveSubWindow(existing)
                else:
                    pipeline_editor = MVSubWindow()
                    if pipeline_editor.fileLoad(fname):
                        self.statusBar().showMessage(f"File {fname} opened successfully.", 3000)
                        pipeline_editor.setTitle()
                        sub_window = self.createMdiChild(pipeline_editor)
                        sub_window.show()
                    else:
                        pipeline_editor.close()
        except Exception as e:
            dump_exception(e)

    def onRunBake(self):
        pipelines = []
        data = []
        if not self.getcurrentPipelineEditorWidget():
            return

        for node in self.getcurrentPipelineEditorWidget().scene.nodes:
            if node.isInvalid():
                self.print_msg("Some node are not valid, can't bake Pipline", color='red')
                QMessageBox.critical(self, "Pipeline Editor Error", "Some node are not valid, can't bake Pipline", QMessageBox.Ok)
                return
            if isinstance(node, MVInputNode):
                pipelines.append([])
                data.append([])
                data[-1] = self.createFlow(node)
                self.traverse_tree(node, pipelines[-1])

        for i, tree_of_nodes in enumerate(pipelines):
            for node in tree_of_nodes:
                current = data[i]
                self.traverse_dict(node, current)

        print(data)

    def traverse_tree(self, node, tree_of_nodes):
        if not node.getOutputs:
            return

        for out in node.getOutputs():
            if isinstance(out, MVOutputNode):
                continue
            tree_of_nodes.append(out)
            self.traverse_tree(out, tree_of_nodes)

    def traverse_dict(self, node, current):
        while current:
            if node.getInput().id == current['id']:
                current['next'].append(self.createFlow(node))
            if current['next']:
                current = current['next'][0]
            else:
                break

    def createFlow(self, node):
        data = node.serialize()
        flow = {
            'uuid': "",
            'flow': {
                'type': "",
                'params': {
                },
            },
            'next': [],
            'retries': 0
        }
        flow['uuid'] = data['uuid']
        flow['id'] = data['id']
        flow['flow']['type'] = data['title']
        flow['flow']['params'] = data['params']

        return flow

    def createMdiChild(self, child_widget=None):
        pipeline_editor = child_widget if child_widget else MVSubWindow()
        sub_window = self.mdiArea.addSubWindow(pipeline_editor)
        sub_window.setWindowIcon(self.empty_icon)
        # TODO: Submit here callback function on item selection (only for nodes)
        pipeline_editor.scene.add_item_doubleclick_listener(self.onNodeClick)
        pipeline_editor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        # pipeline_editor.scene.history.addHistoryModifiedListener(self.updateMinimap)
        pipeline_editor.addCloseEventListener(self.onSubwindowClose)

        return sub_window

    def onSubwindowClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.save_dlg():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, fname):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == fname:
                return window
        return None

    def about(self):
        QMessageBox.about(
            self,
            "About Piepline Editor",
            "The <b>Piepline Editor</b> Mantis Pipeline example demonstrates how to write multiple "
            "document interface applications using Qt. For more information please visit: "
            "<a href='https://github.com/ZikriBen/pipelineeditor'> Git Repository</a>"
        )