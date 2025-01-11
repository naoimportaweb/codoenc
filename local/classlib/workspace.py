import uuid, sys, os, json, subprocess, requests, uuid, hashlib, datetime, traceback;
import ssl, datetime, shutil, threading;

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
    def __init__(self, path_file, passowrd, id=None):
        self.config = Config( os.environ["ROOT"] + "/data/config.json" );
        self.id = str(Workspace.tick());
        if id != None:
            self.id = id;
        self.locals = [];    
        self.servers = [];
        self.ignore = "";
        self.path_file = path_file;
        self.path_backup = os.path.join( path_file[:path_file.rfind("/")], "~" + path_file[path_file.rfind("/") + 1:]);
        self.password = passowrd;
        self.remote_backup = None;
        self.pos_save = "";

    def remotebackup(self, server_js):
        server = ConnectUtils.fromjson(server_js);
        if server.test():
            if self.remote_backup == None or self.remote_backup.id != server.id:
                self.remote_backup = server;
            return True;
        return False;

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
        #self.backup(self.password, volume );
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
        self.backup(self.password, volume );
        return {"status" : True};

    def backup(self, password, volume):
        return {"status" : self.__save__(password, volume, self.path_backup) };
    
    def save(self, password, volume):
        retorno = self.__save__(password, volume, self.path_file );
        if retorno:
            if os.path.exists( self.path_backup ):
                os.unlink( self.path_backup );
            if self.pos_save.strip() != "":
                path_script = volume + "/" + str(uuid.uuid4());
                with open(path_script, 'w') as s:
                    s.write( self.pos_save.replace("~/", os.path.join("/home", os.environ["SUDO_USER"] + "/") ) );
                os.system( "sudo -u "+ os.environ["SUDO_USER"] + " /bin/bash " +  path_script );
            if self.remote_backup != None:
                path_backup_buffer = os.path.join(volume, datetime.now().isoformat().replace(":", "-").replace(".", "-"));
                shutil.copy2( self.path_file , path_backup_buffer);
                #self.remote_backup.upload( self, path_backup_buffer );
                t = threading.Thread(target=self.remote_backup.upload, args=(self, path_backup_buffer, ));
                t.start();
        return {"status" :  retorno};

    def __save__(self, password, volume, final_file_name):
        path_fake = volume + "/" + str(uuid.uuid4());
        with open( path_fake, "w") as f:
            f.write( json.dumps( self.tojson() ) );
        FileHelp.encrypt_file( password.encode(), hashlib.md5(password.encode()).hexdigest()[:16].encode(), path_fake, final_file_name);
        return os.path.exists( final_file_name ); # };

    def tojson(self):
        buffer = {"id" : self.id, "locals" : [], "servers" : [], "ignore" : self.ignore, "pos_save" : self.pos_save, "remote_backup" : None };
        
        if self.remote_backup != None:
            buffer["remote_backup"] = self.remote_backup.tojson();
        
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
            buffer = Workspace(path_file, password);
            js = json.loads( open(path_fake, 'r').read() );
            
            buffer.id = js['id'];
            if js.get("ignore") != None:
                buffer.ignore = js["ignore"];
            if js.get("pos_save") != None:
                buffer.pos_save = js["pos_save"];
            if js.get("remote_backup") != None:
                buffer.remotebackup( js["remote_backup"] );
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
