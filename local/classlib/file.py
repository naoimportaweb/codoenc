import uuid, sys, os, json, subprocess, requests;
import pwd, shutil, traceback,random, json
import grp

sys.path.append( os.environ["ROOT"] );
sys.path.append( os.path.dirname(os.environ["ROOT"]) );

from datetime import datetime, timezone
from classlib.base import Base;
from api.filehelp import FileHelp;
from classlib.connect_utils import ConnectUtils;

def gerarkey(tamanho):
    caracters = "abcdefghijklmnopqrstuvxzABCDEFGHIJKLMNOPQRSTUVXZ1234567890*!@#$%&()-_+?><,.|=";
    saida = "";
    for i in range(tamanho):
        saida += caracters[ random.randint(0, len(caracters) - 1) ];
    return saida;

MAX_PART_SIZE = 2097152; #TODO: parametrizar em um arquivo de configuraçao
class File(Base):
    def __init__(self, path, local, id=None):
        self.id  = str(uuid.uuid4());
        self.key = gerarkey(32);
        self.iv  = gerarkey(16);
        self.cksum = "";
        self.removed = False;
        self.datetime = None;
        self.local = local;
        self.name = None; # path[path.rfind("/") + 1:]
        self.versions = [];
        self.relative_path = None;
        if id != None:
            self.id = id;
        self.setPath( path ); 
    
    def getDir(self):
        return self.getPath()[:self.getPath().rfind("/")];
        
    def getPath(self):
        return self.local.getAbsPath() + self.relative_path;

    def repath(self, newname):
        newfullpath = os.path.join( self.local.getAbsPath() , newname);
        if os.path.exists( self.getPath() ):
            shutil.move(self.getPath(), newfullpath);
        if newname.find("/") > 0:
            self.name = newname[newname.rfind("/"):];
        else:
            self.name = newname;
        self.relative_path = newname;
        return self.tojson();

    def setPath(self, path):
        if path[0] == "/":
            path = path[1:];
        self.name = path;
        self.relative_path =  path; # No passado tinha a ideia de fazer um 
                                    # endereço relativo. vou tirar isso em versao
                                    # futura

    def __upload_generic__(self, path, server):
        return server.upload(self, path);

    def __download_generic__(self, part, volume):
        server = self.local.workspace.serverbyid( part["server"]["id"] );
        if server == None: # tentar reaproveitar inicializaçao de serviço externo
            server = ConnectUtils.fromjson( part["server"] );
        return server.download(self, part, volume);
    
    def download(self, version, volume):
        parts = [];
        for part in version.parts:
            buffer = self.__download_generic__(part, volume);
            if buffer == None:
                print("Falha em fazer download de um pedaço.");
                return None;
            parts.append( buffer );
        return parts;

    def __localizarcksum__(self, cksum):
        for version_buffer in self.versions:
            for part_buffer in version_buffer.parts:
                if part_buffer["cksum"] == cksum:
                    return part_buffer;
        return None;
    def upload(self, paths, cksums, servers):
        try:
            v = Version();
            sumario = [0, 0]
            for i in range(len( paths )):
                path = paths[i];
                cksum = cksums[i];
                part_localizado = self.__localizarcksum__(cksum);
                if part_localizado == None:
                    sumario[0] += 1;
                    server = servers[ random.randint(0, len(servers) - 1)  ];
                    if not self.__upload_generic__(path, server):
                        return None;
                    else:
                        v.appendpart( path, cksum, server.tojson() );
                else:
                    sumario[1] += 1;
                    v.parts.append(part_localizado);
            return v;
        except:
            traceback.print_exc();
        return None;
    
    def chown(self, path):
        os.system('chown -R '+  os.environ["SUDO_USER"] +':'+ os.environ["SUDO_USER"] +' "' + path + '"')
        return;

    def appendversion(self, version):
        self.versions.append(version);
        return self.versions[-1];

    def importfile(self, volume):
        file_remove = [];
        try:
            if os.path.islink( self.getPath() ):
                os.unlink( self.getPath() );
            lista_pedacos_arquivo_nao_criptografados = [];
            last_version = self.versions[-1];
            returns_download = self.download(last_version, volume);
            if returns_download != None:
                for parte_criptografada in returns_download:
                    name_fake = str( uuid.uuid4() );
                    path_fake = volume + "/" + name_fake;
                    FileHelp.decrypt_file( self.key.encode(), self.iv.encode(), parte_criptografada, path_fake);
                    lista_pedacos_arquivo_nao_criptografados.append(path_fake);
                    file_remove.append( parte_criptografada );
                    file_remove.append( path_fake );
                name_fake = str( uuid.uuid4() );
                path_fake_descriptografado = volume + "/" + name_fake;
                if len(lista_pedacos_arquivo_nao_criptografados) > 1:
                    FileHelp.joinfile(lista_pedacos_arquivo_nao_criptografados, path_fake_descriptografado);
                else:
                    shutil.copy2(lista_pedacos_arquivo_nao_criptografados[0], path_fake_descriptografado );
                if os.path.exists(self.getPath()):
                    os.unlink(self.getPath());
                if not os.path.exists(path_fake_descriptografado):
                    raise Exception("O path " + path_fake_descriptografado + " não existe.");
                if not os.path.exists( self.getDir() ):
                    os.makedirs(self.getDir(), exist_ok=True);
                os.symlink(path_fake_descriptografado, self.getPath() );
                self.chown(path_fake_descriptografado);
                self.chown(self.getPath());
                self.chown(self.local.path);
                self.cksum = self.__cksum__();
                return True;
        except:
            traceback.print_exc();
        finally:
            for file in file_remove:
                if os.path.exists(file):
                    os.unlink(file);
        return False;

    def exportfile(self, volume, servers):
        parts = [];
        cksums = [];
        file_remove = [];
        try:
            path_to_upload = self.getPath();
            tamanho_pedacos = MAX_PART_SIZE;
            if os.stat( path_to_upload ).st_size <= tamanho_pedacos:  # arquivo pequeno, entáo vamos dividir somente pela metad
                tamanho_pedacos = int( tamanho_pedacos / 2 );
            tmp_dir_parts = volume + "/" + str(uuid.uuid4());
            if not os.path.exists(tmp_dir_parts):
                os.mkdir( tmp_dir_parts );
            parts = FileHelp.splitfile(path_to_upload , tmp_dir_parts, chunksize=tamanho_pedacos);
            for i in range(len(parts)):
                if not os.path.exists(parts[i]):
                    raise Exception("Arquivo não existe.");
                name_fake = str( uuid.uuid4() );
                path_fake = volume + "/" + name_fake;
                FileHelp.encrypt_file( self.key.encode(), self.iv.encode(), parts[i], path_fake);
                cksums.append( FileHelp.cksum( parts[i] ) );
                file_remove.append(parts[i]); # será removido.
                file_remove.append(path_fake); # será removido.
                parts[i] = path_fake;

            return_upload = self.upload(parts, cksums, servers);
            if return_upload != None:
                #TODO: SE FFOR UM LINK SELF.GETPATH(), ENTÃO COPIAR PARA VOLUME E FAZER UM LINK.
                self.appendversion( return_upload ); 
                self.cksum = self.__cksum__();
                self.datetime = datetime.now(timezone.utc).isoformat();
                path_fake = volume + "/" + str( uuid.uuid4() );
                if not os.path.islink(self.getPath()):
                    shutil.move( self.getPath(), path_fake);
                    os.symlink(path_fake, self.getPath() );
                    self.chown(self.getPath());
                    self.chown(path_fake);
                return True;
            else:
                raise Exception("O arquivo não pode ser enviado.");
        except:
            traceback.print_exc();
        finally:
            for file in file_remove:
                if os.path.exists(file):
                    os.unlink(file);
        return False;
        
    def isdirt(self):
        if not os.path.exists( self.getPath() ): # se existir o link ma nao exisitir o arquivo o linux retorna que náo existe, tem que exisitir os 2
            return False;
        return self.__cksum__() != self.cksum;

    def __cksum__(self):
        return FileHelp.cksum( self.getPath() );
    
    def tojson(self):
        buffer = {"id" : self.id, "name" : self.name, "datetime" : self.datetime, "key" : self.key, "iv" : self.iv, "cksum" : self.cksum, "path" : self.relative_path, "removed" : self.removed, "versions" : []};
        for item in self.versions:
            buffer["versions"].append( item.tojson() );
        return buffer;
    
    @staticmethod
    def new(path, local):
        f = File(path, local);
        #f.cksum = f.__cksum__();
        return f;

class Version:
    def __init__(self):
        self.parts = [];
        self.datetime = datetime.now(timezone.utc).isoformat()
    
    def appendpart(self, path, cksum, server):
        if path.rfind("/") > 0:
            path = path[path.rfind("/") + 1:];
        self.parts.append( {"path" : path, "cksum" : cksum , "server" : server} );
    
    def tojson(self):
        return { "parts" : self.parts, "datetime" : self.datetime }; 
