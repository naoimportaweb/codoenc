import os, sys, inspect;

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton)

sys.path.append( os.environ["ROOT"] );

from view.ui.customvlayout import CustomVLayout;
from classlib.routine import Routine;
from classlib.local import Local;

class DialogNewLocal(QDialog):
    def __init__(self, form, widget, routine):
        super().__init__(form)
        self.setWindowTitle("New Local")
        self.layout_principal = CustomVLayout();
        self.setLayout( self.layout_principal );
        self.painel_new();
        self.resize(800, 500);
        self.routine = routine;
        self.form = form;
        self.widget = widget;

    def painel_new(self):
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        btn_search = QPushButton("Search Directory:")
        btn_open   = QPushButton("Add local")

        self.txt_path = QLineEdit();

        lbl_path = QLabel("Path");

        layout.addWidget(lbl_path,          0, 0);
        layout.addWidget(self.txt_path,     0, 1);
        layout.addWidget(btn_search,        0, 2);
        layout.addWidget(btn_open,          3, 2);

        btn_search.clicked.connect(self.btn_search_click)
        btn_open.clicked.connect(self.btn_open_click)
        btn_open.setDefault(True)
        self.layout_principal.addLayout( "new", layout );
        self.txt_path.setText(os.path.expanduser("~"));

    def btn_open_click(self):
        self.routine.appendlocal( self.txt_path.text() );
        l = Local();
        l.path = self.txt_path.text();
        l.workspace = self.routine.workspace;
        self.routine.workspace.appendlocal( l );
        self.widget.load();
        #self.routine.workspace.appendlocal( self.txt_path.text() );
        self.close();

    def btn_search_click(self):
        dirname = QFileDialog.getExistingDirectory(self, "Please pick a directory...", self.txt_path.text());
        self.txt_path.setText(dirname);
        return;
