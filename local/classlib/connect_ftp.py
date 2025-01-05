import uuid, sys, os, json, requests, traceback, time;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from ftplib import FTP
from classlib.connect_generic import ConnectGeneric;

class ConnectFtp(ConnectGeneric):
    def __init__(self):
        self.username = "";
        self.password = "";
        self.host = "";
        self.ftp = None;

    def test(self):
        return True;

    def toString():
        return "FTP: " + self.host;

    def tojson(self):
        return {"id" : self.id, "type" : "ftp", "password" : self.password, "username" : self.username, "host" : self.host};

    def fromjson(self, js):
        self.id = js["id"];
        self.username = js["username"];
        self.password = js["password"];
        self.host = js["host"];
        self.ftp = FTP(self.host, user=self.username, passwd=self.password)  # connect to host, default port
        print(self.host, self.username, self.password);
        return True;

    def download(self, file, part, volume):
        try:
            ftp = FTP(self.host, user=self.username, passwd=self.password)
            local_filename = volume + "/" + str(uuid.uuid4());
            ftp.cwd('/')
            with open(local_filename, 'wb') as fp:
                filename = "/htdocs/uploads/" + file.id + "/" + part["path"];
                ftp.retrbinary(f"RETR {filename}", fp.write);
                for i in range(100):
                    time.sleep(1); # essa bosta é assincrona, e pode dar DOS no servidor FTP. Que merda do universo.
                    if os.path.exists(local_filename):
                        break;
                return local_filename;
        except:
            traceback.print_exc();
            raise;
        return None;

    def upload(self, file, path):
        try:
            file_remote = '/htdocs/uploads/' + file.id + "/" + path[path.rfind("/") + 1:]
            if self.__criar_diretorio__( "/htdocs/uploads/", file.id):
                with open(path, "rb") as file:
                    self.ftp.storbinary(f"STOR {file_remote}", file);
                    return True;
        except:
            traceback.print_exc();
            raise;
        return False;
    
    def __criar_diretorio__(self,  directory_parent, directory_create ):
        try:
            filelist = []
            exite = False;
            self.ftp.cwd(directory_parent);
            self.ftp.retrlines('LIST',filelist.append)
            for f in filelist:
                if f.split()[-1] == directory_create and f.upper().startswith('D'):
                    exite = True
            if not exite:
                self.ftp.mkd( directory_create );
            return True;
        except:
            traceback.print_exc();
            print("erro ao criar diretorio");
        finally:
            self.ftp.cwd('/')
        return False;