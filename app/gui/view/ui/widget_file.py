# CADA MAPA PRECISA DEUMA CASCA, UMA PONTE ENTRE OS DADOS E A TELA.
import os, sys, inspect, json;

sys.path.append( os.environ["ROOT"] );

from PySide6.QtCore import ( QModelIndex, QSize, Qt, Slot)
from PySide6.QtGui import  QStandardItemModel, QStandardItem, QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QMessageBox, QPushButton, QLabel, QLineEdit, QStyleFactory, QTreeView, QSplitter, QFrame, QToolBar,  QApplication, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout)

from view.ui.customvlayout import CustomVLayout;

class WidgetFile(QWidget):
    def __init__(self,  file, routine, parent):
        super().__init__();
        self.file = file;
        self.parent = parent;
        self.routine = routine;
        self.layout = QVBoxLayout();
        self.setLayout(self.layout);
        lbl_path = QLabel("Path:");
        self.txt_path = QLineEdit();
        self.txt_path.textEdited.connect(self.txt_path_changed)
        CustomVLayout.widget_linha(None, self.layout, [lbl_path, self.txt_path]);
        btn_delete = QPushButton("Delete File");
        btn_delete.clicked.connect(self.btn_delete_click);
        CustomVLayout.widget_linha(None, self.layout, [btn_delete], stretch_inicio=True);
        self.txt_path.setText( file.path );
        self.layout.addStretch();

    def txt_path_changed(self):
        if self.txt_path.text() != self.file.path:
            retorno = self.routine.repathfile(self.file, self.txt_path.text());
            self.file.reloadjson(retorno);
            self.file.node.setText( retorno["name"] );
        return False;

    def btn_delete_click(self):
        qm = QMessageBox();
        ret = qm.question(self,'', "Deseja excluir este arquivo pernamentemente?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            return;
        self.routine.removeByid(self.file.local, self.file);
        self.file.removed = True;
        self.parent.load();
        #self.parent.removerow( self.file.node.parent(), self.file.node );
