import uuid, sys, os, json, requests, traceback;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from classlib.connect_generic import ConnectGeneric;
from classlib.connect_http import ConnectHttp;
from classlib.connect_dropbox import ConnectDropbox;
from classlib.connect_disk import ConnectDisk;
from classlib.connect_ftp import ConnectFtp;
from classlib.connect_mega import ConnectMega;

class ConnectUtils():
    @staticmethod
    def fromjson(js):
        if js["type"] == "http":
            obj = ConnectHttp();
            if obj.fromjson(js):
                return obj;
        elif js["type"] == "dropbox":
            obj = ConnectDropbox();
            if obj.fromjson(js):
                return obj;
        elif js["type"] == "disk":
            obj = ConnectDisk();
            if obj.fromjson(js):
                return obj;
        elif js["type"] == "ftp":
            obj = ConnectFtp();
            if obj.fromjson(js):
                return obj;
        elif js["type"] == "mega":
            obj = ConnectMega();
            if obj.fromjson(js):
                return obj;
        return None;


