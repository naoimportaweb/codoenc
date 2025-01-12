# CADA MAPA PRECISA DEUMA CASCA, UMA PONTE ENTRE OS DADOS E A TELA.
import os, sys, inspect, json;

sys.path.append( os.environ["ROOT"] );
sys.path.append(os.path.dirname(os.path.dirname( os.environ["ROOT"] )) + "/api"); # tem API equivalente para cliente e servidor

from PySide6.QtCore import ( QModelIndex, QSize, Qt, Slot)
from PySide6.QtGui import  QStandardItemModel, QStandardItem, QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (  QStyleFactory, QTreeView, QSplitter, QFrame, QToolBar,  QApplication, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout)

from filehelp import FileHelp;
from view.dialog_merge import DialogMerge;
from view.ui.widget_file import WidgetFile;
from classlib.directory import Directory;
from view.dialog_new_local import DialogNewLocal
from view.dialog_workspace import DialogWorkspace;

def show_alert(form, title, text_small, text_large):
    #https://coderslegacy.com/python/pyqt5-qmessagebox/
    msg = QMessageBox(form)
    msg.setWindowTitle(title)
    msg.setText( text_small )
    msg.setIcon(QMessageBox.Question)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setInformativeText(text_large[:10] + "....")
    msg.setDetailedText(text_large)
    x = msg.exec_()

class MdiWorkspace(QWidget):
    def __init__(self, parent, routine):
        super().__init__();
        self.parent = parent;
        self.routine = routine;
        #self.workspace = None;
        self.model = None;
        self.local_selected_index = None;
        self.abertos = [];
        self.isloaded = False;
        self.ui();
        self.load();

    def addToolbar(self, parent):
        toolbar = QToolBar("Local")
        toolbar.setIconSize(QSize(16,16))
        parent.addWidget( toolbar );
        button_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.GoUp), "Export local", self)
        button_action.setStatusTip("Exportar esse local")
        button_action.triggered.connect(self.btn_export_local_click)
        toolbar.addAction(button_action)
        button_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.GoDown), "Import local", self)
        button_action.setStatusTip("Importar esse local")
        button_action.triggered.connect(self.btn_import_local_click)
        toolbar.addAction(button_action)
        button_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh), "Refresh", self)
        button_action.setStatusTip("Refresh")
        button_action.triggered.connect(self.btn_refresh_local_click)
        toolbar.addAction(button_action)

    def __chavebynode__(self, buffer):
        array = [];
        teste = buffer;
        while(teste != None):
            array.insert(0, teste.text() );
            teste = teste.parent();
        return '/'.join( array ).replace("//", "/");
    
    # Cria um ou mais nós, se tiver pictures/janja.jpg irá criar 2 nós, o pictures e o janaja.jpg, isso vem em um array [pictures, janja.jpg]
    #                       que é o array, já a raiz é o nó raiz que deve ser adicionado.
    def createnode(self, raiz, array, file_object): #
        itens_adicionados = 0;
        for item in array:
            encontrou = False;
            for i in range(raiz.rowCount()):
                if raiz.child(i) != None and raiz.child(i).text() == item:
                    encontrou = True;
                    raiz = raiz.child(i);
                    break;
            if not encontrou:
                buffer = QStandardItem( item );
                if item == array[-1]:
                    file_object.node = buffer;
                    buffer.setData( file_object );
                else:
                    d = Directory( item );
                    d.node = buffer;
                    buffer.setData( d );
                raiz.appendRow(buffer);
                if self.__chavebynode__(buffer) in self.abertos:
                    self.tree.expand( buffer.index() );
                raiz = buffer;

    def appenddir(self, buffer, raiz):
        i = 0;
        while(i < len(buffer.files) ):
            file = buffer.files[i];
            if file.removed:
                i = i + 1;
                continue;
            if buffer.files[i].path.find("/") < 0:  # arquivos que ficam na raiz ou soltos
                bufferl = QStandardItem( file.path );
                bufferl.setData( file );
                bufferl.data().node = bufferl;
                raiz.appendRow(bufferl);
            else:
                self.createnode(raiz, buffer.files[i].path.strip().split("/"), file);
            i = i + 1;

    def removerow(self, qparent, qindex):
        self.tree.rowsRemoved( qparent.index() , qindex.index().row(), qindex.index().row());
    
    def load(self):
        self.isloaded = False;
        for local in self.routine.workspace.locals:
            local.reloadfiles(self.routine.listfiles(local));
            
        self.model = QStandardItemModel();
        self.tree.setModel(self.model);
        for buffer in self.routine.workspace.locals:
            bufferw1 = QStandardItem( buffer.path );
            bufferw1.setEditable(False);
            self.model.appendRow( bufferw1 );
            if self.__chavebynode__(bufferw1) in self.abertos:
                self.tree.expand( bufferw1.index() );
            self.appenddir( buffer , bufferw1);
        self.isloaded = True;

    def ui(self):
        hbox = QHBoxLayout(self)
        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)
        splitter1 = QSplitter(Qt.Horizontal)
        topright = QFrame()
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        self.rightlayout = QVBoxLayout();
        topright.setLayout(self.rightlayout);
        splitter1.setSizes([400,600])
        hbox.addWidget(splitter1);
        self.setLayout(hbox)

        self.tree = QTreeView()
        self.tree.setHeaderHidden(False);
        self.tree.clicked.connect(self.somethingExpanded_tree);
        self.tree.collapsed.connect(self.collapsed_tree);
        self.tree.expanded.connect(self.expanded_tree);
        self.tree.setModel(self.model)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")
        windowLayout = QVBoxLayout()
        self.addToolbar( windowLayout );
        windowLayout.addWidget(self.tree)
        topleft.setLayout(windowLayout);
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
    
    def __item__(self, a):
        array = [];
        self.indexs( a, array );
        self.local_selected_index = array[0];
        buffer = self.model;
        for i in range(len(array)):
            item = array[i];
            if type(buffer).__name__ == "QStandardItemModel":
                buffer = buffer.item(item);
            else:
                buffer = buffer.child(item);
            array[i] = buffer.text();
        item_selecionado = buffer;
        return array;

    def collapsed_tree(self, a):
        if not self.isloaded:
            return;
        item = self.__item__(a);
        chave = '/'.join( item ).replace("//", "/");
        index = self.abertos.index( chave );
        if index >= 0:
            self.abertos.pop( index );
    
    def expanded_tree(self, a):
        if not self.isloaded:
            return;
        item = self.__item__(a);
        chave = '/'.join( item ).replace("//", "/");
        self.abertos.append(chave);

    def somethingExpanded_tree(self, a):
        obj_item_model = self.model.itemFromIndex( a );
        if type( obj_item_model.data() ).__name__ == "File":
            tela = WidgetFile(  obj_item_model.data(), self.routine, self );
            for i in reversed(range(self.rightlayout.count())): 
                self.rightlayout.itemAt(i).widget().setParent(None);
            self.rightlayout.addWidget(tela);

    
    def indexs(self, element, array):
        if element.row() < 0:
            return;
        array.insert(0, element.row() );
        self.indexs(element.parent(), array);
    
    def save(self):
        if self.routine.saveworkspace()["status"]:
            self.parent.notify("Salvo com sucesso em: " + self.routine.workspace_path);
        else:
            self.parent.notify("Falha ao salvar o workspace.");

    def exportworkspace(self):
        self.routine.exportworkspace();
        self.load();

    def alterado(self): # que gambiarra da porra, quando curtir a cachaça vou melhorar!!!
        for diretorio in self.routine.workspace.locals:
            for arquivo in diretorio.files:
                if arquivo.path[0] == '/':  # GAMBIARRA !!!!! RESOLVIDO
                    arquivo.path = arquivo.path[1:];
                path =  os.path.join(diretorio.path, arquivo.path);
                if not os.path.exists(path):
                    continue;
                cksum_agora = FileHelp.cksum(path);
                if cksum_agora != arquivo.cksum:
                    return path;
        return None;
    
    def action_new_local_click(self):
        f = DialogNewLocal(self.parent, self, self.routine);
        f.exec();
        self.load();

    def btn_refresh_local_click(self):
        self.load();                                                                                # Atualiza a TreeView
    
    def btn_export_local_click(self):
        self.routine.exportlocal( self.routine.workspace.locals[ self.local_selected_index  ].id );      # 1 - Exporta os arquivos do diretórios
        self.load();                                                                                # 2 - Recarrega a Tree View

    def btn_import_local_click(self):
        self.routine.importlocal( self.routine.workspace.locals[ self.local_selected_index  ].id );      # 1 - Importa os arquivos do diretórios
        self.load();                                                                                            # 2 - Recarrega a Tree View

    def closeworkspace(self):
        buffer = self.alterado();
        if buffer != None:
            qm = QMessageBox();
            ret = qm.question(self,'', "Existem arquivos alterados, deseja realmente APAGAR TUDO em sue COMPUTADOR?", QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                return;
        self.save();
        self.routine.closeworkspace();
        self.close();
    
    def importworkspace(self):
        buffer = self.alterado();
        if buffer != None:
            qm = QMessageBox();
            ret = qm.question(self,'', "Existem arquivos alterados, deseja realmente fazer o download?", QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                return;
        self.routine.importworkspace();
    
    def closeEvent(self, event):
        alterado = self.alterado();
        if alterado:
            qm = QMessageBox();
            ret = qm.question(self,'', "Existem arquivos alterados, deseja realmente fechar?", QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.Yes:
                event.accept();
            else:
                event.ignore();
            
    def action_edit_workspace(self):
        f = DialogWorkspace(self.parent, self, self.routine);
        f.exec();
        self.save();