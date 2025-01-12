import os, uuid, sys, importlib, hashlib;
import traceback, os, inspect, json;

sys.path.append( os.environ["ROOT"] );
import classlib.workspace;
from classlib.workspace import Workspace;

class WorkspaceService: 
    #def create(self, data, db, volume, connection, address):
    #    js = {"id" : str(uuid.uuid4()),"name" : data["parameters"]["name"], "servers" : [], "locals" : []};
    #    js["servers"].append( { "id" : "1", "type" : "http", "token" : "1111111111111111"} );
    #    return db.append( js );
    
    def workspaceremotebackup(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return w.remotebackup(data["server"]);

    def workspaceremotebackupclear(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        w.remote_backup = None;
        return True;

    def storeconfig(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        w.ignore = data["ignore"];
        w.pos_save = data["pos_save"];
        return True;
    
    def addserver(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        buffer = w.appendserver(data["server"]);
        return buffer != None and buffer.id == data["server"]["id"];# sucesso ao adicionar....
    
    def removeserverbyid(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return w.removeserverbyid(data["server_id"]);

    def listworkspace(self, data, db, volume, connection, address ):
        return db.list( "workspace" );

    def removefile(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return w.removefile(data["pos"]);

    def listfiles(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return w.listfiflesjson();

    def close(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        if w.close():
            db.delete("workspace", data["id"]);
            return db.get("workspace", data["id"]) == None;
        return False;
    
    def createworkspace(self, data, db, volume, connection, address ):
        #"path" : , "id" : , "url" , "token" 
        data["password"] = data["password"] + hashlib.md5(data["password"].encode()).hexdigest();
        w = Workspace(data["path"], data["password"][:32], id=data["id"]); 
        if data["url"] != "":
            w.appendserver( {"id" : w.id, "type" : "http", "url" : data["url"], "token" : data["token"]} );
        db.append( "workspace", w.id, w, replace=True );
        return w.tojson();
    
    def appendlocal(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        if w == None:
            raise Exception("Não existe o workspace informado.");
        return w.appendlocal( data["path"] ).tojson();
    
    def openworkspace(self, data, db, volume, connection, address ):
        data["password"] = data["password"] + hashlib.md5(data["password"].encode()).hexdigest();
        if os.path.exists( data["path"]):
            w = Workspace.fromjson(data["path"], data["password"][:32], volume);
            # Testando se já está aberto!!!!
            buffer = db.get( "workspace", w.id );
            if buffer == None:
                db.append( "workspace", w.id, w, replace=True );
                return w.tojson();
            else:
                return buffer.tojson();
        return {};

    def saveworkspace(self, data, db, volume, connection, address ):
        data["password"] = data["password"] + hashlib.md5(data["password"].encode()).hexdigest();
        w = db.get("workspace", data["id"]);
        return w.save(data["password"][:32], volume);
    
    def clearworkspace(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return w.clearworkspace();
    
    def exportworkspace(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return {"locals" : w.exportworkspace( volume ) };
    
    def importworkspace(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["id"]);
        return {"locals" : w.importworkspace( volume ) };