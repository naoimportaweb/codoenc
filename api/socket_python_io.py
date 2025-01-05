
class SocketPythonIO:
    def encrypt(self, text, key):
        return text;
    def decrypt(self, data, key):
        return data;
    def read(self, connection, address):
        return connection.recv(102400);
        #return self.decrypt(connection.recv(1024), "");
    def write(self, text, connection, address):
        return self.encrypt(connection.send( text ), "");
