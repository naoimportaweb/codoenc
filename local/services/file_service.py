import os, uuid, sys, importlib, hashlib;
import traceback, os, inspect, json;

sys.path.append( os.environ["ROOT"] );
import classlib.workspace;

from classlib.workspace import Workspace;
from classlib.file import File;

class FileService:
    def exists(self, data, db, volume, connection, address):
        return os.path.exists( data["path"] );
    
    def repath(self, data, db, volume, connection, address):
        w = db.get("workspace", data["workspace_id"]);
        f = w.getFile( data["id"] );
        retorno = f.repath( data["newname"] );
        return retorno;