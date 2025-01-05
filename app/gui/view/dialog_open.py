import os, sys, inspect, json;

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton)

sys.path.append( os.environ["ROOT"] );

from view.ui.customvlayout import CustomVLayout;
from classlib.routine import Routine;

class DialogOpen(QDialog):
    def __init__(self, form):
        super().__init__(form)
        self.setWindowTitle("Open Workspace")
        self.layout_principal = CustomVLayout();
        self.setLayout( self.layout_principal );
        self.painel_new();
        self.resize(800, 500);
        self.routine = None;

    def painel_new(self):
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        btn_search = QPushButton("Search File")
        btn_open   = QPushButton("Open Workspace")

        self.txt_port = QLineEdit();
        self.txt_path = QLineEdit();
        self.txt_key = QLineEdit();
        self.txt_key.setEchoMode(QLineEdit.Password);
        self.txt_port.setText("50000");

        lbl_path = QLabel("Path");
        lbl_port = QLabel("Port");
        lbl_key  = QLabel("Key (encripted)");

        layout.addWidget(lbl_path,          0, 0);
        layout.addWidget(self.txt_path,     0, 1);
        layout.addWidget(btn_search,        0, 2);
        layout.addWidget(lbl_key,           1, 0);
        layout.addWidget(self.txt_key,      1, 1);
        layout.addWidget(lbl_port,          2, 0);
        layout.addWidget(self.txt_port,     2, 1);
        layout.addWidget(btn_open,          3, 2);

        self.txt_port.setText("50001");
        self.txt_path.setText(os.path.expanduser("~"));

        if os.path.exists( os.path.expanduser("~/codo_desenv.json") ):
            with open(os.path.expanduser("~/codo_desenv.json"), "r") as f:
                js = json.loads( f.read() );
                self.txt_path.setText(js["path"]);
                self.txt_port.setText(js["port"]);
                self.txt_key.setText(js["password"]);

        btn_search.clicked.connect(self.btn_search_click)
        btn_open.clicked.connect(self.btn_open_click)
        btn_open.setDefault(True)
        self.layout_principal.addLayout( "new", layout );

    def btn_open_click(self):
        self.routine = Routine.openworkspace(int(self.txt_port.text()), self.txt_path.text(), self.txt_key.text());
        self.close();

    def btn_search_click(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/',"Json file (*.json)")
        self.txt_path.setText( fname[0] );
        return;
