#!/usr/bin/python3
import os, sys, inspect;
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));

sys.path.append(CURRENTDIR);
os.environ["ROOT"] = CURRENTDIR;

from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit)

import PySide6.QtExampleIcons  # noqa: F401

from view.mdiworkspace import MdiWorkspace;
from view.dialog_open import DialogOpen;
from view.dialog_new_workspace import DialogNewWorkspace;

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._mdi_area = QMdiArea()
        self._mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self._mdi_area)
        self._mdi_area.subWindowActivated.connect(self.update_menus)
        self.create_actions()
        self.create_menus(); # desativado por padraio
        self.create_tool_bars(); # desativado por padrao
        self.create_status_bar()
        self.update_menus()
        self.read_settings()
        self.setWindowTitle("CODÓ ENCRYPT")

    def notify(self, text, time=5000):
        self.statusBar().showMessage(text, time);
    
    def closeEvent(self, event):
        self._mdi_area.closeAllSubWindows()
        if self._mdi_area.currentSubWindow():
            event.ignore()
        else:
            self.write_settings()
            event.accept()

    @Slot()
    def new_workspace(self):
        f = DialogNewWorkspace(self);
        f.exec();
        if f.routine != None:
            child = MdiWorkspace(self, f.routine);
            self._mdi_area.addSubWindow(child);
            child.showMaximized();
        return;
        #f = DialogDiagramChoice(self);
        #f.exec();
        #if f.workspace != None:
        #    child = MdiMap(self, f.map)
        #    self._mdi_area.addSubWindow(child);
        #    child.new_map()
        #    child.showMaximized();

    @Slot()
    def open(self):
        f = DialogOpen(self);
        f.exec();
        if f.routine != None:
            child = MdiWorkspace(self, f.routine);
            self._mdi_area.addSubWindow(child);
            child.showMaximized();


    @Slot()
    def save(self):
        self.active_mdi_child() and self.active_mdi_child().save()
        return;
    @Slot()
    def workspace_export(self):
        self.active_mdi_child() and self.active_mdi_child().exportworkspace()
        return;
    @Slot()
    def workspace_close(self):
        self.active_mdi_child() and self.active_mdi_child().closeworkspace()
        return;
    @Slot()
    def workspace_import(self):
        self.active_mdi_child() and self.active_mdi_child().importworkspace()
        return;
    @Slot()
    def workspace_new_local(self):
        self.active_mdi_child() and self.active_mdi_child().action_new_local_click();
        return;
    @Slot()
    def workspace_propert(self):
        self.active_mdi_child() and self.active_mdi_child().action_edit_workspace();
        return;
    @Slot()
    def workspace_errors(self):
        return;
        #buffer = (self.active_mdi_child() and self.active_mdi_child()).mapa;
        #f buffer != None:
        #    f = DialogRelationshipCheck(self, buffer);
        #    f.exec();


    @Slot()
    def about(self):
        QMessageBox.about(self, "About CODÓ ENCRYPT", "")

    @Slot()
    def update_menus(self):
        return;
        #has_mdi_child = (self.active_mdi_child() is not None)
        #if self.active_mdi_child() is not None:
        #    buffer_area = self.active_mdi_child() and self.active_mdi_child();
        #    title = "Relationship MAP: " + buffer_area.mapa.getName() ;
        #    if buffer_area.mapa.getLocked() and len(buffer_area.mapa.lock_list) > 0 :
        #        title = title + " (ReadOnly at " + buffer_area.mapa.lock_list[-1]["lock_time"] + " ISO DATE)";
        #    self.setWindowTitle( title )

    @Slot()
    def update_window_menu(self):
        self._window_menu.clear()
        self._window_menu.addAction(self._close_act)
        self._window_menu.addAction(self._close_all_act)
        self._window_menu.addSeparator()
        self._window_menu.addAction(self._tile_act)
        self._window_menu.addAction(self._cascade_act)
        self._window_menu.addSeparator()
        self._window_menu.addAction(self._next_act)
        self._window_menu.addAction(self._previous_act)
        self._window_menu.addAction(self._separator_act)

        windows = self._mdi_area.subWindowList()
        self._separator_act.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()
            f = child.user_friendly_current_file()
            text = f'{i + 1} {f}'
            if i < 9:
                text = '&' + text
            action = self._window_menu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.active_mdi_child())
            slot_func = partial(self.set_active_sub_window, window=window)
            action.triggered.connect(slot_func)

    def create_actions(self):
        #https://doc.qt.io/qt-6/qicon.html
        
        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew)
        self._new_act = QAction(icon, "&New", self, shortcut=QKeySequence.New, statusTip="Create a new Workspace",  triggered=self.new_workspace)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)
        self._open_act = QAction(icon, "&Open...", self,
                                 shortcut=QKeySequence.Open, statusTip="Open an existing workspace",
                                 triggered=self.open)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave)
        self._save_act = QAction(icon, "&Save", self,
                                 shortcut=QKeySequence.Save,
                                 statusTip="Save the document to disk", triggered=self.save)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit)
        self._exit_act = QAction(icon, "E&xit", self, shortcut=QKeySequence.Quit,
                                 statusTip="Exit the application",
                                 triggered=QApplication.instance().closeAllWindows)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties)
        self._workspace_edit_act = QAction(icon, "Property", self,
                                shortcut=QKeySequence.Cut,
                                statusTip="Edit workspace property",
                                triggered=self.workspace_propert)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.InsertLink)
        self._workspace_new_local_act = QAction(icon, "New Local", self,
                                shortcut=QKeySequence.Cut,
                                statusTip="New Local",
                                triggered=self.workspace_new_local);

        icon = QIcon.fromTheme(QIcon.ThemeIcon.GoUp)
        self._workspace_export_act = QAction(icon, "Export", self,
                                shortcut=QKeySequence.Cut,
                                statusTip="Export Workspace",
                                triggered=self.workspace_export)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.GoDown)
        self._workspace_import_act = QAction(icon, "Import", self,
                                shortcut=QKeySequence.Cut,
                                statusTip="Import Workspace",
                                triggered=self.workspace_import);

        icon = QIcon.fromTheme(QIcon.ThemeIcon.EditDelete)
        self._workspace_close_act = QAction(icon, "Close all", self,
                                shortcut=QKeySequence.Cut,
                                statusTip="Close all",
                                triggered=self.workspace_close);

        #icon = QIcon( CURRENTDIR + "/resources/check.png");
        #self._workspace_edit_check = QAction(icon, "Check", self,
        #                        shortcut=QKeySequence.Cut,
        #                        statusTip="Check workspace",
        #                        triggered=self.workspace_errors)

        self._close_act = QAction("Cl&ose", self,
                                  statusTip="Close the active window",
                                  triggered=self._mdi_area.closeActiveSubWindow)

        self._close_all_act = QAction("Close &All", self,
                                      statusTip="Close all the windows",
                                      triggered=self._mdi_area.closeAllSubWindows)

        self._tile_act = QAction("&Tile", self, statusTip="Tile the windows",
                                 triggered=self._mdi_area.tileSubWindows)

        self._cascade_act = QAction("&Cascade", self,
                                    statusTip="Cascade the windows",
                                    triggered=self._mdi_area.cascadeSubWindows)

        self._next_act = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                                 statusTip="Move the focus to the next window",
                                 triggered=self._mdi_area.activateNextSubWindow)

        self._previous_act = QAction("Pre&vious", self,
                                     shortcut=QKeySequence.PreviousChild,
                                     statusTip="Move the focus to the previous window",
                                     triggered=self._mdi_area.activatePreviousSubWindow)

        self._separator_act = QAction(self)
        self._separator_act.setSeparator(True)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout)
        self._about_act = QAction(icon, "&About", self,
                                  statusTip="Show the application's About box",
                                  triggered=self.about)

        self._about_qt_act = QAction("About &Qt", self,
                                     statusTip="Show the Qt library's About box",
                                     triggered=QApplication.instance().aboutQt)

    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("&File")
        self._file_menu.addAction(self._new_act)
        self._file_menu.addAction(self._open_act)
        self._file_menu.addAction(self._save_act)
        self._file_menu.addSeparator()
        action = self._file_menu.addAction("Switch layout direction")
        action.triggered.connect(self.switch_layout_direction)
        self._file_menu.addAction(self._exit_act)

        self._window_menu = self.menuBar().addMenu("&Window")
        self.update_window_menu()
        self._window_menu.aboutToShow.connect(self.update_window_menu)

        self.menuBar().addSeparator()

        self._help_menu = self.menuBar().addMenu("&Help")
        self._help_menu.addAction(self._about_act)
        self._help_menu.addAction(self._about_qt_act)

    def create_tool_bars(self):
        self._file_tool_bar = self.addToolBar("File")
        self._file_tool_bar.addAction(self._new_act)
        self._file_tool_bar.addAction(self._open_act)
        self._file_tool_bar.addAction(self._save_act)
        self._workspace_tool_bar = self.addToolBar("CODO")
        self._workspace_tool_bar.addAction(self._workspace_edit_act);
        self._workspace_tool_bar.addAction(self._workspace_new_local_act);
        self._workspace_tool_bar.addAction(self._workspace_export_act);
        self._workspace_tool_bar.addAction(self._workspace_import_act);
        self._workspace_tool_bar.addAction(self._workspace_close_act);
        self._workspace_tool_bar.addAction(self._workspace_close_act);
        #self._workspace_tool_bar.addAction(self._workspace_edit_check);

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def read_settings(self):
        settings = QSettings('QtProject', 'CODO')
        geometry = settings.value('geometry', QByteArray())
        if geometry.size():
            self.restoreGeometry(geometry)

    def write_settings(self):
        settings = QSettings('QtProject', 'CODO')
        settings.setValue('geometry', self.saveGeometry())

    def active_mdi_child(self):
        active_sub_window = self._mdi_area.activeSubWindow()
        if active_sub_window:
            return active_sub_window.widget()
        return None

    def find_mdi_child(self, fileName):
        canonical_file_path = QFileInfo(fileName).canonicalFilePath()

        for window in self._mdi_area.subWindowList():
            if window.widget().current_file() == canonical_file_path:
                return window
        return None

    @Slot()
    def switch_layout_direction(self):
        if self.layoutDirection() == Qt.LeftToRight:
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)

    def set_active_sub_window(self, window):
        if window:
            self._mdi_area.setActiveSubWindow(window)


if __name__ == '__main__':
    argument_parser = ArgumentParser(description='CODÓ Encrypt',
                                     formatter_class=RawTextHelpFormatter)
    argument_parser.add_argument("files", help="Files",
                                 nargs='*', type=str)
    options = argument_parser.parse_args()

    app = QApplication(sys.argv)

    icon_paths = QIcon.themeSearchPaths()
    QIcon.setThemeSearchPaths(icon_paths + [":/qt-project.org/icons"])
    QIcon.setFallbackThemeName("example_icons")

    #dlg = DialogConnect();
    #dlg.exec(); 
    #server = Server();
    #if server.status:
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
    #else:
    #    sys.exit(0);