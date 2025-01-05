import socket, traceback, sys, os, threading, inspect, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
sys.path.append( CURRENTDIR );
sys.path.append( os.path.dirname( CURRENTDIR ) + "/api" );

from socket_python_io import SocketPythonIO;

class Db:
    def __init__(self):
        self.data = {};
    
    def closeall(self, table):
        if self.data.get(table) != None:
            for key in self.data[table]:
                value = self.data[table][key];
                value.close();
    
    def list(self, table):
        retorno = "";
        for key in self.data[table]:
            value = self.data[table][key];
            retorno += "[+] " + value.tolabel();
        return retorno;

    def delete(self, table, id):
        self.data[table][id]
    
    def append(self, table, id, js, replace=False):
        if self.data.get(table) == None:
            self.data[ table ] = {};
        self.data[table][id] = js;
    
    def get(self, table, id):
        if self.data.get(table) == None:
            return None;
        return self.data[table][id];

    def clear(self, table, id):
        if self.data.get(table) == None:
            return None;
        del self.data[table][id];
        return True;