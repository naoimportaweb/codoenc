import os, sys;

sys.path.append( os.environ["ROOT"] );

from classlib.local import Local;

class Workspace:
    def __init__(self):
        self.id = None;
        self.ignore = "";
        self.servers = [];
        self.locals = [];

    def appendlocal(self, local):
        if len([obj for obj in self.locals if obj.path == local.path]) == 0:  #https://www.geeksforgeeks.org/python-json-data-filtering/
            self.locals.append(local);
        return local;

    @staticmethod
    def fromjson(js):
        w = Workspace();
        w.id = js["id"];
        if js.get("ignore") != None:
            w.ignore = js["ignore"];
        if js.get("servers") != None:
            w.servers = js["servers"];
        for local in js["locals"]:
            Local.fromjson( local, w );
        return w;
