import os, sys, inspect;

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton)

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( os.path.dirname( CURRENTDIR ) );
sys.path.append( ROOT );

from view.ui.customvlayout import CustomVLayout;
from classlib.routine import Routine;

class DialogMerge(QDialog):
    def __init__(self, form, routine):
        super().__init__(form)
        self.routine = routine;
        self.setWindowTitle("Merge Workspace")
        self.layout_principal = CustomVLayout();
        self.setLayout( self.layout_principal );
        self.painel_merge();
        self.opcao = False;
        self.resize(800, 500);

    def painel_merge(self):
        layout = QVBoxLayout();
        self.table = CustomVLayout.widget_tabela(self, ["File Name"]);
        btn_server = QPushButton("Servidor é mais atual");
        btn_local  = QPushButton("Computador local é mais atual");
        btn_fechar = QPushButton("Fechar");
        CustomVLayout.widget_linha(self, layout, [btn_server, btn_local]);
        layout.addWidget( self.table );
        CustomVLayout.widget_linha(self, layout, [btn_fechar]);
        self.layout_principal.addLayout( "new", layout );


