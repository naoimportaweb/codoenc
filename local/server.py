#!/usr/bin/python3

import socket, traceback, sys, os, threading, inspect, json, argparse;
import importlib, shutil;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
sys.path.append( CURRENTDIR );
sys.path.append( os.path.dirname( CURRENTDIR ) + "/api" );

os.environ["ROOT"] = CURRENTDIR;

from socket_python_io import SocketPythonIO;
from volume import Volume;
from classlib.config import Config;
from classlib.db import Db;

parser = argparse.ArgumentParser(description="");
parser.add_argument("-s", "--size", required=False, help="");
parser.add_argument("-p", "--port", required=False, help="");
args = parser.parse_args();

volume = Volume();

class Server:
    def __init__(self, port, size):
        self.config = Config( CURRENTDIR + "/data/config.json" );
        if port == None:
            port = self.config.port;
        if size == None:
            size = self.config.size;
        self.port = int(port);
        self.size = size;
        
        self.db = Db();
        self.volumes = [ self.createvolume() ];
    
    def __del__(self):
        self.db.closeall("workspace"); # fechar todos os workspaces....
        for volume in self.volumes:
            volume.close();
    
    def createvolume(self):
        v = Volume();
        v.create( self.size ); # X * 120GB
        if v.path == None:
            raise Exception("Não foi possível criar volume");
        return v;
        #return path_volume;

    def process(self, connection, address):
        try:
            io = SocketPythonIO();
            receved = io.read(connection, address);
            data_js = json.loads( receved.decode("utf-8") );
            module = importlib.import_module( data_js["module"] + "_service" ) #'my_package.my_module'
            importlib.reload( module );
            class_din = getattr(module, data_js["class"] + "Service")
            object_inst = class_din();
            method_ = getattr(object_inst, data_js["method"]);
            retorno =  { "status" : True, "return" :  method_(data_js["parameters"], self.db, self.volumes[-1].path, connection, address) }; 
        except:
            traceback.print_exc();
            retorno = {"status" : False};
        connection.sendall( json.dumps(retorno).encode("utf-8") );
        connection.close();

    def open(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
            serversocket.bind(('127.0.0.1', self.port));
            serversocket.listen(10);
            print(('127.0.0.1', self.port));
            while True:
                try:
                    connection, address = serversocket.accept();
                    threading.Thread(target=self.process, args=(connection, address)).start();
                except KeyboardInterrupt:
                    sys.exit(0);
                except:
                    traceback.print_exc();

if __name__ == "__main__": 
    if os.geteuid() == 0:
        shutil.copy2( CURRENTDIR + "/data/meuwork.json", "/tmp/work.json");
        server = Server(args.port, args.size);
        server.open();
    else:
        print("Não é root, abortando.");







