import os, sys;

sys.path.append( os.environ["ROOT"] );

from classlib.version import Version;


class File:
    def __init__(self):
        self.id  = None;
        self.cksum = None;
        self.datetime = None;
        self.name = None;
        self.versions = [];
        self.path = None;
        self.removed = False;
        self.node = None;

    def appendversion(self, version):
        self.versions.append(version);
        return version;
    
    @staticmethod
    def fromjson(js, local):
        f = File();
        f.__fromjson__(js);
        f.local = local;
        for version in js["versions"]:
            Version.fromjson( version, f );
        return local.appendfile(f);

    def reloadjson(self, js):
        self.__fromjson__(js);

    def reload(self, obj):
        self.cksum = obj.cksum;
        self.datetime = obj.datetime;
        self.name = obj.name;
        self.path = obj.path;
        self.removed = obj.removed;

    def __fromjson__(self, js):
        self.id = js["id"];
        self.cksum = js["cksum"];
        self.datetime = js["datetime"];
        self.name = js["name"];
        self.path = js["path"];
        self.removed = js["removed"];
        