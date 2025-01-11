import uuid, sys, os, json, requests, traceback, shutil;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from classlib.connect_generic import ConnectGeneric;

class ConnectDisk(ConnectGeneric):
    def __init__(self):
        self.path = None;

    def start(self):
        return True;

    def test(self):
        return os.path.exists( self.path );

    def toString():
        return "Disk: " + self.path;

    def tojson(self):
        return {"id" : self.id, "type" : "disk", "path" : self.path};

    def fromjson(self, js):
        self.id = js["id"];
        self.path = js["path"];
        return True;

    def download(self, file, part, volume):
        try:
            local_filename = volume + "/" + str(uuid.uuid4());
            shutil.copy2( os.path.join( self.path, file.id, part["path"] ) , local_filename );
            return local_filename;
        except:
            traceback.print_exc();
            raise;
        return None;

    def upload(self, file, path):
        try:
            dir_buffer = os.path.join( self.path, file.id );
            if not os.path.exists( dir_buffer ):
                os.makedirs( dir_buffer );
            shutil.copy2(path, os.path.join( dir_buffer, path[path.rfind("/") + 1:] ));
            return True;
        except:
            traceback.print_exc();
            raise;
        return False;