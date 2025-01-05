import os, uuid, sys, importlib, hashlib;
import traceback, os, inspect, json;

sys.path.append( os.environ["ROOT"] );
import classlib.workspace;
from classlib.workspace import Workspace;

class LocalService: 
    
    def list(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["workspace_id"]);
        for local in w.locals:
            if local.id == data["local_id"]:
                return local.filesjson();
        return [];

    def removefile(self, data, db, volume, connection, address ):
        w = db.get("workspace", data["workspace_id"]);
        for local in w.locals:
            if local.id == data["local_id"]:
                return {"remove" : local.removefileByid( data["file_id"] )};
        return {"remove" : False };

    def exportlocal(self, data, db, volume, connection, address ):
        lista_local = [];
        w = db.get("workspace", data["workspace_id"]);
        for local in w.locals:
            if local.id == data["local_id"]:
                lista_local = local.exportlocal( volume, w.servers );
                break;
        return {"locals" :  lista_local };
    
    def importlocal(self, data, db, volume, connection, address ):
        lista_local = [];
        w = db.get("workspace", data["workspace_id"]);
        for local in w.locals:
            if local.id == data["local_id"]:
                lista_local = local.importlocal( volume );
                break;
        return {"locals" :  lista_local };