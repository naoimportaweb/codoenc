import os, sys;

sys.path.append( os.environ["ROOT"] );

from classlib.part import Part;

class Version:
    def __init__(self):
        self.id = None;
        self.parts = [];
        self.file = None;

    def appendpart(self, part):
        self.parts.append( part );
        return part;

    @staticmethod
    def fromjson(js, file):
        v = Version();
        v.file = file;
        for part in js["parts"]:
            Part.fromjson( part, v);
        return file.appendversion(v);