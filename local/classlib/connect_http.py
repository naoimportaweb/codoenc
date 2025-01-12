import uuid, sys, os, json, requests, traceback;

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from classlib.connect_generic import ConnectGeneric;

class ConnectHttp(ConnectGeneric):
    def __init__(self):
        self.url = None;
        self.token = None;
        self.headers = None;
        self.session = None;
    
    def start(self):
        try:
            if self.session == None:
                self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
                    };
                self.session = requests.Session()
                self.session.verify = False
            return True;
        except:
            traceback.print_exc();
            self.session = None;
        return False;

    def tojson(self):
        return {"id" : self.id, "type" : "http", "url" : self.url, "token" : self.token};

    def toString():
        return "HTTP: " + self.url;

    def test(self):
        r = None;
        try:
            if self.start():
                r = self.session.get(url=self.url + "status.php?token=" + self.token, headers=self.headers)
                retorno_json = json.loads( r.text );
                return r.status_code == 200 and retorno_json["status"] == True;
        except:
            traceback.print_exc();
            if r != None:
                print(r.text);
            raise;
        return False;

    def fromjson(self, js):
        self.id = js["id"];
        self.url = js["url"];
        self.token = js["token"];
        return True;

    def download(self, file, part, volume):
        if self.start():
            print("URL: ", part["server"]["url"] + "uploads/" + file.id + "/" + part["path"]);
            r = requests.get(part["server"]["url"] + "uploads/" + file.id + "/" + part["path"], stream=True, verify=False, headers=self.headers);
            if r.status_code != 200:
                print("Falha de download.", str(r.status_code) + ":", part["server"]["url"] + "uploads/" + part["path"]);
                return None;
            local_filename = volume + "/" + str(uuid.uuid4());
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
            return local_filename
        return None;

    def upload(self, file, path):
        r = None;
        try:
            if self.start():
                files = {'userfile': open( path ,'rb')}
                r = self.session.post(url=self.url + "upload.php?id=" + file.id + "&token=" + self.token, files=files, json={'name': 'filename', "token" : self.token}, headers=self.headers)
                retorno_json = json.loads( r.text );
                return r.status_code == 200 and retorno_json["status"] == True;
        except:
            traceback.print_exc();
            if r != None:
                print(r.text);
            raise;
        return False;