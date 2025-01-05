import os, sys;

sys.path.append( os.environ["ROOT"] );

from classlib.file import File;

class Local:
    def __init__(self):
        self.id = None;
        self.files = [];
        self.workspace = None;
        self.path = None;
        self.node = None;
    
    def reloadfiles(self, js):
        for file in js:
            File.fromjson( file, self );
    
    def appendfile(self, file):
        for i in range(len(self.files)):
            if self.files[i].id == file.id:
                self.files[i].reload( file );
                return self.files[i];
        self.files.append(file);
        return file;

    @staticmethod
    def fromjson(js, workspace):
        l = Local();
        l.id = js["id"];
        l.path = js["path"];
        l.workspace = workspace;
        for file in js["files"]:
            File.fromjson( file, l );
        return workspace.appendlocal(l);