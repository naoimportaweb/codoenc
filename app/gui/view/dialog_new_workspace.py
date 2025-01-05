import os, sys, inspect;
import time, json;

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton)

sys.path.append( os.environ["ROOT"] );

from view.ui.customvlayout import CustomVLayout;
from classlib.routine import Routine;

class DialogNewWorkspace(QDialog):
    def __init__(self, form):
        super().__init__(form)
        self.setWindowTitle("New Workspace")
        self.layout_principal = CustomVLayout();
        self.setLayout( self.layout_principal );
        self.painel_new();
        self.resize(800, 500);
        self.form = form;
        self.routine = None;

    def painel_new(self):
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        btn_search = QPushButton("Search Directory:")
        btn_open   = QPushButton("Create Workspace")
        self.txt_path = QLineEdit();
        lbl_path = QLabel("Path");
        layout.addWidget(lbl_path,          0, 0);
        layout.addWidget(self.txt_path,     0, 1);
        layout.addWidget(btn_search,        0, 2);
        
        lbl_number = QLabel("Number:");
        self.txt_number = QLineEdit();
        layout.addWidget(lbl_number,        1, 0);
        layout.addWidget(self.txt_number,   1, 1);

        lbl_name = QLabel("Workspace Name:");
        self.txt_name = QLineEdit();
        layout.addWidget(lbl_name,        2, 0);
        layout.addWidget(self.txt_name,   2, 1);

        lbl_pass = QLabel("Password:");
        self.txt_pass = QLineEdit();
        self.txt_pass.setEchoMode(QLineEdit.Password);
        layout.addWidget(lbl_pass,        3, 0);
        layout.addWidget(self.txt_pass,   3, 1);

        lbl_port = QLabel("Port Local Server:");
        self.txt_port = QLineEdit();
        layout.addWidget(lbl_port,        4, 0);
        layout.addWidget(self.txt_port,   4, 1);
        
        self.txt_number.setText( str( time.time() ).replace(".", "") );
        self.txt_port.setText("50001");
        self.txt_path.setText(os.path.expanduser("~"));

        if os.path.exists( os.path.expanduser("~/codo_desenv.json") ):
            with open(os.path.expanduser("~/codo_desenv.json"), "r") as f:
                js = json.loads( f.read() );
                self.txt_port.setText(js["port"]);
                self.txt_pass.setText(js["password"]);
                self.txt_name.setText(js["name"]);

        layout.addWidget(btn_open,          6, 2);
        btn_search.clicked.connect(self.btn_search_click)
        btn_open.clicked.connect(self.btn_open_click)
        btn_open.setDefault(True)
        self.layout_principal.addLayout( "new", layout );
        

    def btn_open_click(self):
        self.routine = Routine.createworkspace(self.txt_port.text(), self.txt_number.text(), self.txt_name.text(), self.txt_path.text(), "", "", self.txt_pass.text());
        self.close();

    def btn_search_click(self):
        dirname = QFileDialog.getExistingDirectory(self, "Please pick a directory...", self.txt_path.text());
        self.txt_path.setText(dirname);
        return;
