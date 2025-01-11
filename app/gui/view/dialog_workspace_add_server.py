import os, sys, inspect, uuid;

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSettings, QSaveFile, QTextStream, Qt, Slot)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QComboBox, QTabWidget,QHeaderView, QTableWidgetItem, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton)

sys.path.append( os.environ["ROOT"] );

from view.ui.customvlayout import CustomVLayout;
from classlib.routine import Routine;

class DialogServer(QDialog):
    def __init__(self, form, routine, element):
        super().__init__(form);
        self.form = form;
        self.routine = routine;
        self.element = element;
        self.layout_principal = CustomVLayout();
        self.setLayout( self.layout_principal );
        self.cmb_type = QComboBox();
        for buffer in ["disk", "http", "mega", "ftp"]:
            self.cmb_type.addItem( buffer );
        if element != None:
            index = self.cmb_type.findText(element["type"], Qt.MatchFixedString)
            if index >= 0:
                 self.cmb_type.setCurrentIndex(index);
        self.cmb_type.currentTextChanged.connect(self.cmb_type_changed);
        
        CustomVLayout.widget_linha(self, self.layout_principal, [QLabel("Type:") , self.cmb_type], stretch_inicio=True );
        self.painel_disk();
        self.painel_http();
        self.painel_dropbox();
        self.painel_ftp();
        self.painel_mega();
        self.layout_principal.disable( "disk" );
        self.layout_principal.disable( "http" );
        self.layout_principal.disable( "dropbox" );
        self.layout_principal.disable( "ftp" );
        self.layout_principal.disable( "mega" );

        if self.element != None:
            self.layout_principal.enable( self.element["type"] );
        else:
            self.layout_principal.enable( "disk" );
            #if self.element["type"] == "http":
            #    self.painel_http();
            #elif self.element["type"] == "disk":
            #    self.painel_disk();
            #elif self.element["type"] == "dropbox":
            #    self.painel_dropbox();
            

        btn_save = QPushButton("Save");
        btn_save.clicked.connect(self.btn_save_click);
        CustomVLayout.widget_linha(self, self.layout_principal, [btn_save], stretch_inicio=True );
    
    def cmb_type_changed(self):
        self.layout_principal.disable( "disk" );
        self.layout_principal.disable( "http" );
        self.layout_principal.disable( "dropbox" );
        self.layout_principal.disable( "ftp" );
        self.layout_principal.enable( self.cmb_type.currentText() );
        return;
    
    def painel_http(self):
        #-------------
        layout = QVBoxLayout();
        lbl_server = QLabel("Server:")
        lbl_server.setProperty("class", "normal")
        self.txt_server_http = QLineEdit()
        self.txt_server_http.setMinimumWidth(500);
        if self.element != None and self.element.get("url") != None:
            self.txt_server_http.setText( self.element["url"] );
        CustomVLayout.widget_linha(self, layout, [lbl_server, self.txt_server_http] );
        #-------------
        lbl_token = QLabel("Token:")
        lbl_token.setProperty("class", "normal")
        self.txt_token_http = QLineEdit()
        self.txt_token_http.setEchoMode(QLineEdit.Password);
        self.txt_token_http.setMinimumWidth(500);
        if self.element != None and self.element.get("token") != None:
            self.txt_token_http.setText( self.element["token"] );
        CustomVLayout.widget_linha(self, layout, [lbl_token, self.txt_token_http] );
        self.layout_principal.addLayout( "http", layout );
    
    def painel_ftp(self):
        #-------------
        layout = QVBoxLayout();
        lbl_server = QLabel("Host:")
        lbl_server.setProperty("class", "normal")
        self.txt_server_ftp = QLineEdit()
        self.txt_server_ftp.setMinimumWidth(500);
        if self.element != None and self.element.get("host") != None:
            self.txt_server_ftp.setText( self.element["host"] );
        CustomVLayout.widget_linha(self, layout, [lbl_server, self.txt_server_ftp] );
        #-------------
        lbl_username = QLabel("Username:")
        lbl_username.setProperty("class", "normal")
        self.txt_username_ftp = QLineEdit()
        self.txt_username_ftp.setMinimumWidth(500);
        if self.element != None and self.element.get("username") != None:
            self.txt_username_ftp.setText( self.element["username"] );
        CustomVLayout.widget_linha(self, layout, [lbl_username, self.txt_username_ftp] );
        #-------------
        lbl_password = QLabel("Password:")
        lbl_password.setProperty("class", "normal")
        self.txt_password_ftp = QLineEdit()
        self.txt_password_ftp.setMinimumWidth(500);
        self.txt_password_ftp.setEchoMode(QLineEdit.Password);
        if self.element != None and self.element.get("password") != None:
            self.txt_password_ftp.setText( self.element["password"] );
        CustomVLayout.widget_linha(self, layout, [lbl_password, self.txt_password_ftp] );
        #-------------
        lbl_directory_ftp = QLabel("Directory:")
        lbl_directory_ftp.setProperty("class", "normal")
        self.txt_directory_ftp = QLineEdit()
        self.txt_directory_ftp.setMinimumWidth(500);
        if self.element != None and self.element.get("directory") != None:
            self.txt_directory_ftp.setText( self.element["directory"] );
        else:
            self.txt_directory_ftp.setText( "/htdocs/" );
        CustomVLayout.widget_linha(self, layout, [lbl_directory_ftp, self.txt_directory_ftp] );

        self.layout_principal.addLayout( "ftp", layout );
    def painel_mega(self):
        layout = QVBoxLayout();
        #-------------
        lbl_username = QLabel("Username:")
        lbl_username.setProperty("class", "normal")
        self.txt_username_mega = QLineEdit()
        self.txt_username_mega.setMinimumWidth(500);
        if self.element != None and self.element.get("username") != None:
            self.txt_username_mega.setText( self.element["username"] );
        CustomVLayout.widget_linha(self, layout, [lbl_username, self.txt_username_mega] );
        #-------------
        lbl_password = QLabel("Password:")
        lbl_password.setProperty("class", "normal")
        self.txt_password_mega = QLineEdit()
        self.txt_password_mega.setMinimumWidth(500);
        self.txt_password_mega.setEchoMode(QLineEdit.Password);
        if self.element != None and self.element.get("password") != None:
            self.txt_password_mega.setText( self.element["password"] );
        CustomVLayout.widget_linha(self, layout, [lbl_password, self.txt_password_mega] );
        self.layout_principal.addLayout( "mega", layout );
    
    def painel_dropbox(self):
        #-------------
        layout = QVBoxLayout();
        lbl_token = QLabel("Token:")
        lbl_token.setProperty("class", "normal")
        self.txt_token_dropbox = QLineEdit()
        self.txt_token_dropbox.setMinimumWidth(500);
        if self.element != None and self.element.get("token") != None:
            self.txt_token_dropbox.setText( self.element["token"] );
        CustomVLayout.widget_linha(self, layout, [lbl_token, self.txt_token_dropbox] );
        self.layout_principal.addLayout( "dropbox", layout );

    def painel_disk(self):
        #-------------
        layout = QVBoxLayout();
        lbl_path = QLabel("Path:")
        lbl_path.setProperty("class", "normal")
        self.txt_path_disk = QLineEdit()
        self.txt_path_disk.setMinimumWidth(500);
        if self.element != None and self.element.get("path") != None:
            self.txt_path_disk.setText( self.element["path"] );
        CustomVLayout.widget_linha(self, layout, [lbl_path, self.txt_path_disk] );
        self.layout_principal.addLayout( "disk", layout );

    def btn_save_click(self):
        if self.cmb_type.currentText() == "http":
            if self.element == None:
                self.element = {"type" : "http", "id" : str(uuid.uuid4()), "url" : "", "token" : ""};
            self.element["url"] = self.txt_server_http.text();
            self.element["token"] = self.txt_token_http.text();
            if self.element["url"][-1] != "/":  # Tem que terminar com / para juntar strings de URL
                self.element["url"] += "/";
        elif self.cmb_type.currentText() == "dropbox":
            if self.element == None:
                self.element = {"type" : "dropbox", "id" : str(uuid.uuid4()), "token" : ""};
            self.element["token"] = self.txt_token_dropbox.text();
        elif self.cmb_type.currentText() == "disk":
            if self.element == None:
                self.element = {"type" : "disk", "id" : str(uuid.uuid4()), "path" : ""};
            self.element["path"] = self.txt_path_disk.text();
            if self.element["path"][-1] != "/":  # Tem que terminar com / para juntar com ou sem os.path.join()
                self.element["path"] += "/";
        elif self.cmb_type.currentText() == "ftp":
            if self.element == None:
                self.element = {"type" : "ftp", "id" : str(uuid.uuid4()), "password" : "", "username" : "", "host" : ""};
            self.element["host"] = self.txt_server.text();
            self.element["username"] = self.txt_username_ftp.text();
            self.element["password"] = self.txt_password_ftp.text();
            self.element["directory"] = self.txt_directory_ftp.text();
        elif self.cmb_type.currentText() == "mega":
            if self.element == None:
                self.element = {"type" : "mega", "id" : str(uuid.uuid4()), "password" : "", "username" : ""};
            self.element["username"] = self.txt_username_mega.text();
            self.element["password"] = self.txt_password_mega.text();