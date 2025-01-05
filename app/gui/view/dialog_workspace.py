import os, sys, inspect;

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QTabWidget,QHeaderView, QTableWidgetItem, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton)

sys.path.append( os.environ["ROOT"] );

from view.ui.customvlayout import CustomVLayout;
from view.dialog_workspace_add_server import DialogServer;
from classlib.routine import Routine;
from classlib.local import Local;

class DialogWorkspace(QDialog):
    def __init__(self, form, widget, routine):
        super().__init__(form)
        self.setWindowTitle("Workspace")
        self.resize(800, 500);
        self.routine = routine;
        self.form = form;
        self.widget = widget;
        self.tab = QTabWidget();  
        self.page_info = CustomVLayout.widget_tab(    self.tab, "Information");
        self.page_servers = CustomVLayout.widget_tab( self.tab, "Servers");
        layout = QVBoxLayout();
        layout.addWidget( self.tab );
        self.setLayout(   layout   );
        self.painel_info();
        self.painel_servers();

    def painel_info(self):
        lbl_part = QLabel("Ignore patters:")
        lbl_part.setProperty("class", "normal")
        self.txt_part = QLineEdit()
        self.txt_part.setMinimumWidth(500);
        self.txt_part.setText( self.routine.workspace.ignore );
        CustomVLayout.widget_linha(self, self.page_info, [lbl_part, self.txt_part] );
    
    def painel_servers(self):
        lbl_part = QLabel("Servers")
        lbl_part.setProperty("class", "normal")
        CustomVLayout.widget_linha(self, self.page_servers, [lbl_part], stretch_fim=True );
        btn_servers_add = QPushButton("Add");
        btn_servers_del = QPushButton("Remove");
        btn_servers_add.clicked.connect(self.btn_servers_add_click);
        btn_servers_del.clicked.connect(self.btn_servers_del_click);
        CustomVLayout.widget_linha(self, self.page_servers, [btn_servers_add, btn_servers_del] );
        self.table_servers = CustomVLayout.widget_tabela(self, ["Server"], tamanhos=[QHeaderView.Stretch], double_click=self.table_servers_click);
        self.page_servers.addWidget(self.table_servers);
        self.load_servers();

    def load_servers(self):
        self.table_servers.setRowCount( len( self.routine.workspace.servers ) );
        for i in range(len( self.routine.workspace.servers )):
            if self.routine.workspace.servers[i]["type"] == "http":
                self.table_servers.setItem( i, 0, QTableWidgetItem( self.routine.workspace.servers[i]["url"] ) );
            elif self.routine.workspace.servers[i]["type"] == "disk":
                self.table_servers.setItem( i, 0, QTableWidgetItem( self.routine.workspace.servers[i]["path"] ) );
            elif self.routine.workspace.servers[i]["type"] == "dropbox":
                self.table_servers.setItem( i, 0, QTableWidgetItem( self.routine.workspace.servers[i]["token"][:20] ) );
            elif self.routine.workspace.servers[i]["type"] == "ftp":
                self.table_servers.setItem( i, 0, QTableWidgetItem( self.routine.workspace.servers[i]["host"] ) );
            elif self.routine.workspace.servers[i]["type"] == "mega":
                self.table_servers.setItem( i, 0, QTableWidgetItem( self.routine.workspace.servers[i]["username"] ) );
    
    def btn_servers_add_click(self):
        f = DialogServer(self, self.routine, None);
        f.exec();
        if f != None:
            retorno = self.routine.addserver(f.element);
            if retorno:
                self.routine.workspace.servers.append( f.element );
                self.load_servers();
        return;
    
    def btn_servers_del_click(self):
        element = self.routine.workspace.servers[ self.table_servers.index() ];
        self.routine.removeserverbyid(element["id"]);
        for i in range(len(self.routine.workspace.servers)):
            if self.routine.workspace.servers[i]["id"] == element["id"]:
                self.routine.workspace.servers.pop(i);
                break;
        self.load_servers();
        return;
    
    def table_servers_click(self):
        element = self.routine.workspace.servers[ self.table_servers.index() ];
        f = DialogServer(self, self.routine, element);
        f.exec();
        if f.element != None:
            retorno = self.routine.addserver(f.element);
            if retorno:
                self.routine.workspace.servers[ self.table_servers.index() ] = f.element;
                self.load_servers();
        return;