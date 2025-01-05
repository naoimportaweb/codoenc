import uuid, os, json, sys, time, shutil;
import threading
sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from classlib.base import Base;
from classlib.file import File;
from api.filehelp import FileHelp;

MAX = 10;

class Local(Base):
    def __init__(self, path, workspace, id=None):
        self.id = str(uuid.uuid4());
        self.files = [];
        self.workspace = workspace;
        if id != None:
            self.id = id;
        self.setPath(path);
    
    def filesjson(self):
        retorno = [];
        for file in self.files:
            retorno.append( file.tojson() );
        return retorno;
    
    def close(self):
        for file in self.files:
            if os.path.exists(file.getPath()):
                if os.path.islink( file.getPath() ):
                    os.remove(os.path.realpath( file.getPath() ));
                    os.remove(file.getPath());
        os.remove( self.getAbsPath() );
        #shutil.rmtree( self.getAbsPath() );

    def removefileByid(self, id):
        for i in range(len(self.files)):
            file = self.files[i];
            if file.id == id:
                self.files.removed = True;
                if os.path.exists( file.getPath() ):
                    if os.path.islink(file.getPath()):
                        os.remove( os.path.realpath( file.getPath() ) );
                    os.remove( file.getPath() );
                return True;
        return False;
    
    def removefile(self, pos):
        del self.files[pos];
        return True;

    def setPath(self, path):
        path = FileHelp.uniformpath(path);
        if path[-1] != "/":
            path = path + "/";
        self.path = path;
    
    def getAbsPath(self):
        return self.path.replace("~/", "/home/" + os.environ["SUDO_USER"] + "/");

    def tojson(self):
        buffer = {"id" : self.id, "path" : self.path, "files" : []};
        for file in self.files:
            buffer["files"].append(file.tojson());
        return buffer;

    def getfilesforexport(self):
        files_local = [];
        return_export = [];
        self.__tree__(self.path, files_local);
        for file in files_local: # será uma string com path complet /a/b/c.jpg
            file = FileHelp.uniformpath( file );
            buffer = next((x for x in self.files if FileHelp.comparepath( x.getPath(), file) ), None);
            if buffer == None:
                return_export.append( self.appendfile( file ) );
            else:
                if buffer.isdirt():
                    return_export.append(buffer);
        return return_export;
    
    def clearlocal(self):
        lista = self.getfilesforexport();
        if len(lista) > 0:
            print("Não pode excluir pois possuem arquivos alterados.");
            return False;
        for buffer in self.files:
            if os.path.islink( buffer.getPath() ):
                os.unlink( buffer.getPath() );
        return True;

    def exportlocal(self, volume, servers):
        lista = self.getfilesforexport();
        for file in lista:
            if not file.exportfile(volume, servers):
                return False;
        return True;
    
    def __importlocal_thread__(self, file, volume):
        file.importfile(volume);
    
    def importlocal(self, volume):
        contador = 0;

        for i in range(len( self.files )):
            file = self.files[i];
            try:
                while contador > MAX:
                    time.sleep(1);
                contador = contador + 1;
                t = threading.Thread(target=self.__importlocal_thread__, args=(file, volume,))
                t.start();
            except:
                print("Erro de importação.");
            finally:
                contador = contador - 1;


    def appendfile(self, path):
        for file in self.files:
            if FileHelp.comparepath(path, file.getPath()):
                return file;
        path = FileHelp.subtractpath(self.path, path);
        self.files.append( File.new(path, self) );
        return self.files[-1];

    def filesearch(self, local, path):
        return next((x for x in local.files if x.getPath() == path), None);
    
    def __tree__(self, path, lista):
        buffers =  os.listdir( path );
        for buffer in buffers:
            path_file = path + "/" + buffer;
            if os.path.islink(path_file):
                reallinkpath = os.path.realpath(path_file);
                if os.path.isfile(reallinkpath):
                    lista.append( path_file );
                continue;
                #return; # evitar entrar em loop de link para diretórios......
            if os.path.isfile(path_file):
                lista.append( path_file );
            if os.path.isdir(path_file):
                self.__tree__( path_file, lista );