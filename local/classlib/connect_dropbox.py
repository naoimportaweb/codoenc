import dropbox;
import uuid, sys, os, json, requests, traceback;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from classlib.connect_generic import ConnectGeneric;

class ConnectDropbox(ConnectGeneric):
    def __init__(self):
        self.token = None;
        self.dbx = None;

    def test(self):
        return True;

    def toString():
        return "Dropbox: " + self.token[:20];

    def tojson(self):
        return {"id" : self.id, "type" : "dropbox", "token" : self.token};

    def fromjson(self, js):
        self.id = js["id"];
        self.token = js["token"];
        self.dbx = dropbox.Dropbox(self.token);
        return True;

    def download(self, file, part, volume):
        try:
            local_filename = volume + "/" + str(uuid.uuid4());
            self.dbx.files_download_to_file(local_filename, "/" + file.id + "/" + part["path"] );
            return local_filename;
        except:
            traceback.print_exc();
            raise;
        return None;

    def upload(self, file, path):
        try:
            with open(path, "rb") as f:
                data = f.read()
                self.dbx.files_upload(data, "/"+ file.id +"/" + path[path.rfind("/") + 1:] , mode=dropbox.files.WriteMode("overwrite"));
                return True;
        except:
            traceback.print_exc();
            raise;
        return False;