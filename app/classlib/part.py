
class Part:
    def __init__(self):
        self.path = None;
        self.version = None;
        self.cksum = None;
        self.server = None;

    @staticmethod
    def fromjson(js, version):
        p = Part();
        p.path = js["path"];
        p.cksum = js["cksum"];
        p.server = js["server"];
        p.version = version;
        return version.appendpart( p );

#{'path': 'a9d980a4-32c7-4961-b521-19a98593542b', 'cksum': '1631655501', 'server': {'id': '2', 'type': 'http', 'url': 'http://localhost/', 'token': '123456'}}