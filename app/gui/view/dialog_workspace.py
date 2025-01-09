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
        self.page_pos_save = CustomVLayout.widget_tab(self.tab, "Pos Save");
        self.page_servers = CustomVLayout.widget_tab( self.tab, "Servers");
        layout = QVBoxLayout();
        layout.addWidget( self.tab );
        self.setLayout(   layout   );
        self.painel_info();
        self.painel_pos_save();
        self.painel_servers();

    def painel_info(self):
        lbl_part = QLabel("Ignore patters:")
        lbl_part.setProperty("class", "normal")
        self.txt_part = QLineEdit()
        self.txt_part.setMinimumWidth(500);
        self.txt_part.setText( self.routine.workspace.ignore );
        CustomVLayout.widget_linha(self, self.page_info, [lbl_part, self.txt_part] );

        lbl_backup = QLabel("Ignore patters:")
        lbl_backup.setProperty("class", "normal")
        self.txt_backup = QLineEdit()
        self.txt_backup.setReadOnly(True);
        self.txt_backup.setMinimumWidth(500);
        if self.routine.workspace.remote_backup != None and self.routine.workspace.remote_backup.get("id") != None:
            self.txt_backup.setText( self.rotulo_server( self.routine.workspace.remote_backup ) );
        btn_backup_add = QPushButton("Edit");
        btn_baclup_clear = QPushButton("Clear");
        btn_backup_add.clicked.connect(self.btn_backup_add_click);
        btn_baclup_clear.clicked.connect(self.btn_baclup_clear_click);
        CustomVLayout.widget_linha(self, self.page_info, [lbl_backup, self.txt_backup, btn_backup_add, btn_baclup_clear] );

    def painel_pos_save(self):
        lbl_part = QLabel("Pos Save: (/bin/bash script)")
        lbl_part.setProperty("class", "normal")
        self.txt_pos_save = QTextEdit()
        self.txt_pos_save.setMinimumWidth(500);
        self.txt_pos_save.setPlainText( self.routine.workspace.pos_save );
        self.txt_pos_save.textChanged.connect(self.txt_pos_save_click)
        CustomVLayout.widget_linha(self, self.page_pos_save, [lbl_part] );
        CustomVLayout.widget_linha(self, self.page_pos_save, [self.txt_pos_save] );
    
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

    def rotulo_server(self, js):
        if js["type"] == "http":
            return "http: " + js["url"] ;
        elif js["type"] == "disk":
            return "Disk: " + js["path"] ;
        elif js["type"] == "dropbox":
            return "Dropbox: " + js["token"][:20];
        elif js["type"] == "ftp":
            return "FTP: " + js["host"] ;
        elif js["type"] == "mega":
            return "Mega: " + js["username"] ;
        return "?";
    
    def load_servers(self):
        self.table_servers.setRowCount( len( self.routine.workspace.servers ) );
        for i in range(len( self.routine.workspace.servers )):
            self.table_servers.setItem( i, 0, QTableWidgetItem( self.rotulo_server(self.routine.workspace.servers[i]) ) );
    
    def txt_pos_save_click(self):
        self.routine.workspace.pos_save = self.txt_pos_save.toPlainText();
        self.routine.workspacestoreconfig();
        
    def btn_baclup_clear_click(self):
        retorno = self.routine.workspaceremotebackupclear();
        if retorno:
            self.routine.workspace.remote_backup = None ;
            self.txt_backup.setText("");
        return;

    def btn_backup_add_click(self):
        f = DialogServer(self, self.routine, None);
        f.exec();
        if f.element != None:
            retorno = self.routine.workspaceremotebackup(f.element);
            if retorno:
                self.routine.workspace.remote_backup =  f.element ;
                self.txt_backup.setText( self.rotulo_server( f.element ) );
        return;

    def btn_servers_add_click(self):
        f = DialogServer(self, self.routine, None);
        f.exec();
        if f.element != None:
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