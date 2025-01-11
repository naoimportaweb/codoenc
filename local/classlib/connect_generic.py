
import uuid, sys, os, json, requests, traceback;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

class ConnectGeneric():
    def __init__(self):
        self.id = None;
    
    def start(self):
        return False;
    
    def test(self):
        return False;

    def toString():
        return "";

    def tojson(self):
        return None;

    def fromjson(self, js):
        return None;

    def download(self, file, part, volume):
        return None;

    def upload(self, file, path):
        return False;

