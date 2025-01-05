import socket, json, os, sys;

class LocalConnect:
    def __init__(self, ip="127.0.0.1", port=50000):
        self.ip = ip;
        self.port = int(port);
        self.connect = None;
    
    def open(self):
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.connect.connect(( self.ip , self.port ));

    def send(self, module, classname, method, data_js):
        self.connect.send( json.dumps( {"module" : module, "class" : classname, "method" : method, "parameters" : data_js} ).encode("utf-8") );
        data = ""
        while True:
            buffer = self.connect.recv(1024);
            if not buffer: 
                break
            data = data + buffer.decode("utf-8");
        return json.loads(data) ;