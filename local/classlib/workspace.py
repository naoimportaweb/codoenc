import uuid, sys, os, json, subprocess, requests, uuid, hashlib, datetime, traceback;
import ssl;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from datetime import datetime, timezone
from classlib.base import Base;
from classlib.file import File, Version;
from classlib.local import Local;
from api.filehelp import FileHelp;
from classlib.config import Config;
from classlib.connect_utils import ConnectUtils;

#import urllib3
#urllib3.disable_warnings()
import certifi

class Workspace(Base):
    def __init__(self, path_file, id=None):
        self.config = Config( os.environ["ROOT"] + "/data/config.json" );
        self.id = str(Workspace.tick());
        if id != None:
            self.id = id;
        self.locals = [];    
        self.servers = [];
        self.ignore = "";
        self.path_file = path_file;

    def appendserver(self, server_js):
        for server in self.servers:
            if server.id == server_js["id"]:
                return server; # já existe 
        server = ConnectUtils.fromjson(server_js);
        if server.test():
            self.servers.append( server );
            return server;
        return None;
    
    def removeserverbyid(self, id):
        for i in range(len(self.servers)):
            if self.servers[i].id == id:
                self.servers.pop(i);
                return True;
        return False;

    def serverbyid(self, id):
        for i in range(len(self.servers)):
            if self.servers[i].id == id:
                return self.servers[i];
        return None;

    def getFile(self, id):
        for local in self.locals:
            for file in local.files:
                if file.id == id:
                    return file;
        return None;
    
    @staticmethod
    def tick():
        midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0);
        now = datetime.now();
        delta = now - midnight;
        return delta.seconds;
    
    def close(self):
        try:
            for local in self.locals:
                local.close();
            return True;
        except:
            traceback.print_exc();
        return False;
    
    def removefile(self, pos):
        pos = pos.strip().split(".");
        return self.locals[int(pos[0])].removefile(int(pos[1]));

    def listfiflesjson(self):
        buffer = [];
        for local in self.locals:
            buffer.append( local.tojson() );
        return buffer;

    def clearworkspace(self):
        for local in self.locals:
            if local.clearlocal() == False:
                return False;
        return True;
    
    def appendlocal(self, path):
        for local in self.locals:
            if local.path == path:
                return local; 
        l = Local(path, self);
        self.locals.append(l);
        return l;

    def importworkspace(self, volume):
        for local in self.locals:
            if local.importlocal( volume ) == False:
                return False;
        return True;
    
    def exportworkspace(self, volume):
        for local in self.locals:
            if os.path.exists( local.getAbsPath() ):
                lista_local = local.exportlocal( volume, self.servers );
        return {"status" : True};

    def save(self, password, volume):
        path_fake = volume + "/" + str(uuid.uuid4());
        with open( path_fake, "w") as f:
            f.write( json.dumps( self.tojson() ) );
        FileHelp.encrypt_file( password.encode(), hashlib.md5(password.encode()).hexdigest()[:16].encode(), path_fake, self.path_file);
        return {"status" : os.path.exists( self.path_file )};

    def tojson(self):
        buffer = {"id" : self.id, "locals" : [], "servers" : [], "ignore" : self.ignore};
        
        for server in self.servers:
            buffer["servers"].append( server.tojson() );
        
        for local in self.locals:
            buffer["locals"].append( local.tojson() );
        return buffer;
    
    def tolabel(self):
        locals_str = "";
        for local in self.locals:
            locals_str += "\t|------>" + local.path + " ["+ str( len(local.files) ) +"]" + "\n";
        return self.id +"\t" + self.path_file + "\n" + locals_str;

    def testeworkspace(self):
        with open("/tmp/teste.json", "w") as f:
            f.write( json.dumps( self.tojson() ) );

    @staticmethod
    def fromjson(path_file, password, volume):
        if not os.path.exists( path_file ):
            return {"status" : False};
        path_fake = volume + "/" + str(uuid.uuid4());
        try:
            FileHelp.decrypt_file( password.encode(), hashlib.md5(password.encode()).hexdigest()[:16].encode(), path_file, path_fake);
            print("Descriptografado com sucesso.");
            buffer = Workspace(path_file);
            
            js = json.loads( open(path_fake, 'r').read() );
            
            buffer.id = js['id'];
            if js.get("ignore") != None:
                buffer.ignore = js["ignore"];
            for local in js['locals']:
                buffer_local = Local( local["path"], buffer, id=local["id"] );
                for file in local["files"]:
                    buffer_file = File(file["path"], buffer_local, id=file["id"]);
                    buffer_file.key = file["key"];
                    buffer_file.iv = file["iv"];
                    buffer_file.name = file["name"];
                    buffer_file.cksum = file["cksum"];
                    if file.get("removed") != None:
                        buffer_file.removed = file["removed"];
                    if file.get("datetime") == None:
                        buffer_file.datetime = datetime.now(timezone.utc).isoformat();
                    buffer_file.versions = [];
                    for version in file["versions"]:
                        buffer_version = Version();
                        if version.get("datetime") != None:
                            buffer_version.datetime = version["datetime"];
                        for part_version in version["parts"]:
                            buffer_cksum = "";
                            if part_version.get("cksum") != None:
                                buffer_cksum = part_version["cksum"];
                            buffer_version.appendpart( part_version["path"], buffer_cksum, part_version["server"] );
                        buffer_file.versions.append( buffer_version );
                    buffer_local.files.append( buffer_file );
                buffer.locals.append( buffer_local );
            for server in js['servers']:
                buffer.appendserver(server);
            return buffer;
        except Exception as e:
            traceback.print_exc();
            print(str(e));
            return None; 
        finally:
            os.unlink(path_fake);
