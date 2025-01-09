#!/usr/bin/python3
import argparse, inspect, os, sys, getpass, json;
import colorama, traceback

sys.path.append( os.environ["ROOT"] );

from api.localconnect import LocalConnect;
from colorama import Fore, Style;
from classlib.workspace import Workspace;

class Routine:
    def __init__(self, port, workspace_path, password, id=None):
        self.workspace_path = workspace_path;
        self.password = password;
        self.id = 0;
        self.port = port;
        self.workspace = None;
        if id != None:
            self.id = str(id);

    def listfiles(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "listfiles", { "id" : self.id });
        retorno = retorno["return"];
        i = 0;
        for local in retorno:
            print("[+] -", local["path"] );
            j = 0;
            for file in local["files"]:
                print("  |--->", str(i) + "." + str(j) + "\t", file["path"], str( len(file["versions"]) )  );
                j = j + 1;
            i = i + 1;
            print("_________________________________________________________");
            print();
        return retorno;

    def listworkspace(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "listworkspace", { "id" : self.id });
        retorno = retorno["return"];
        return retorno;

    def addserver(self, server):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "addserver", { "id" : self.id, "server" : server });
        retorno = retorno["return"];
        return retorno;

    def removeserverbyid(self, server_id):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "removeserverbyid", { "id" : self.id, "server_id" : server_id });
        retorno = retorno["return"];
        return retorno;
    
    def repathfile(self, file, newname):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.file", "File", "repath", { "workspace_id" :  self.id, "id" : file.id, "newname" : newname });
        retorno = retorno["return"];
        return retorno;

    def removeByid(self, local, file):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.local", "Local", "removefile", { "workspace_id" : self.id, "local_id" : local.id, "file_id" : file.id });
        retorno = retorno["return"];
        return retorno;

    def listfiles(self, local):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.local", "Local", "list", { "workspace_id" : self.id, "local_id" : local.id});
        retorno = retorno["return"];
        return retorno;
    
    def removefile(self, pos):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "removefile", { "id" : self.id, "pos" : pos });
        retorno = retorno["return"];
        return retorno;

    def workspacestoreconfig(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "storeconfig", self.workspace.tojson() );
        retorno = retorno["return"];
        return retorno;

    def appendlocal(self, path):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "appendlocal", { "id" : self.id, "path" : path });
        retorno = retorno["return"];
        return retorno;

    def clearworkspace(self, path):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "clearworkspace", { "id" : self.id });
        return retorno;

    def closeworkspace(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "close", { "id" : self.id });
        return retorno;

    @staticmethod
    def createworkspace(port, id, nome, path, url, token, password1):
        buffer = Routine(port, os.path.join(path, id + ".json"), password1, id=id);
        #buffer = Routine(port, "/home/" + os.environ["USER"] + "/" + id + ".json", password1, id=id);
        socket = LocalConnect(port=port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "createworkspace", { "path" : buffer.workspace_path, "id" : id, "url" : url, "token" : token, "password" : password1});
        retorno = retorno["return"];
        print(retorno);
        buffer.id = retorno["id"];
        buffer.workspace = Workspace.fromjson( retorno );
        return buffer;
    
    @staticmethod
    def openworkspace(port, workspace_path, password):
        workspace_path = workspace_path.replace("~/", "/home/" + os.environ["USER"] + "/" );
        if not os.path.exists(workspace_path):
            print("O caminho não existe: ", workspace_path);
            return;
        buffer = Routine(port, workspace_path, password);
        socket = LocalConnect(port=port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "openworkspace", {"path" : buffer.workspace_path, "password" : buffer.password });
        retorno = retorno["return"];
        buffer.id = retorno["id"];
        buffer.workspace = Workspace.fromjson( retorno );
        return buffer

    def saveworkspace(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "saveworkspace", {"id" : self.id, "password" : self.password });
        retorno = retorno["return"];
        return retorno

    # Importa um workspace para o serviço local, vem na saida um JSON com tudo.
    def importworkspace(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "importworkspace", {"id" : self.id });
        retorno = retorno["return"];
        return retorno

    def importlocal(self, local_id):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.local", "Local", "importlocal", {"workspace_id" : self.id, "local_id" : local_id });
        retorno = retorno["return"];
        return retorno

    def exportworkspace(self):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.workspace", "Workspace", "exportworkspace", {"id" : self.id });
        retorno = retorno["return"];
        return retorno

    def exportlocal(self, local_id):
        socket = LocalConnect(port=self.port);
        socket.open();
        retorno = socket.send("services.local", "Local", "exportlocal", {"workspace_id" : self.id, "local_id" : local_id });
        retorno = retorno["return"];
        return retorno
    
    def clearworkspace(self, args):
        print("Não implementado, muito perigoso, vou pensar melhor.....");
