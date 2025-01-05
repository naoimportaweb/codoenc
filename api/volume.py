import os, uuid, getpass, inspect, sys, traceback;
import random
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
sys.path.append( CURRENTDIR);

class Volume:
    def __init__(self):
        self.volume_name = None;
        self.path = None;

    def password(self, tamanho):
        return str(uuid.uuid4());

    def create(self, tamanhoGB, volume_name=None):
        if volume_name == None:
            volume_name = str(uuid.uuid4());
        self.volume_name = volume_name;
        command = '/bin/bash '+ CURRENTDIR +'/bash/create_volume.sh ' + self.volume_name + ' ' + str(tamanhoGB) + ' ' + self.password(64) ;
        p = os.system('%s' % (command));
        if p == 0:
            self.path = "/tmp/" + self.volume_name;
            return self.path;
        else:
            return None;
    
    def close(self):
        command = '/bin/bash '+ CURRENTDIR +'/bash/close_volume.sh ' + self.path + " " + self.volume_name;
        p = os.system('%s' % (command));
        if p == 0:
            try:
                os.unlink( "/tmp/" + self.volume_name + ".img" );
            except:
                traceback.print_exc();
        return True;

if __name__ == "__main__":
    tamanhoGB = 1;
    v = Volume();
    retorno = v.create( tamanhoGB );


