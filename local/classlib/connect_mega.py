import uuid, sys, os, json, requests, traceback, time;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from mega import Mega 
from classlib.connect_generic import ConnectGeneric;

class ConnectMega(ConnectGeneric):
    def __init__(self):
        self.username = "";
        self.password = "";
        self.mega = None;
        self.m = None;

    def test(self):
        return True;

    def toString():
        return "Mega: " + self.username;

    def tojson(self):
        return {"id" : self.id, "type" : "mega", "password" : self.password, "username" : self.username};

    def fromjson(self, js):
        self.id = js["id"];
        self.username = js["username"];
        self.password = js["password"];
        return True;

    def start(self):
        try:
            if self.mega == None:
                self.mega = Mega() 
                self.m = self.mega.login(self.username, self.password) ;
            return True;
        except:
            traceback.print_exc();
            mega = None;
        return False;

    def download(self, file, part, volume):
        try:
            if self.start():
                filename = str(uuid.uuid4());
                local_filename = volume + "/" + filename;
                file = self.m.find( file.id + '/' + part["path"])
                self.m.download(file, volume, filename);
                return local_filename;
        except:
            traceback.print_exc();
            raise;
        return None;

    def upload(self, file, path):
        try:
            if self.start():
                file_remote = file.id + "/" + path[path.rfind("/") + 1:]
                folder = self.__criar_diretorio__( file.id );
                if folder == None:
                    raise Exception("Não foi possível criar diretório no mega upload.");
                file = self.m.upload(path, folder[0])
                return True;
        except:
            traceback.print_exc();
            raise;
        return False;
    
    def __criar_diretorio__(self, directory_create ):
        try:
            folder = self.m.find(directory_create)
            if folder == None:
                self.m.create_folder(directory_create);
            return self.m.find(directory_create);
        except:
            traceback.print_exc();
            print("erro ao criar diretorio");
        return None;