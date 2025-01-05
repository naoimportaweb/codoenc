import os, random, struct, re, sys, subprocess, traceback;
import hashlib
from Crypto.Cipher import AES

class FileHelp:
    @staticmethod
    def cksum(path):
        if os.path.exists( path ):
            if os.path.islink(path):
                path = os.path.realpath(path);
            with open( path, "rb") as f:
                file_hash = hashlib.md5()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
                return file_hash.hexdigest();
        return "";

    @staticmethod
    def uniformpath(path):
        path = path.replace("//", "/");
        path = path.replace("~/", "/home/" + os.environ["SUDO_USER"] + "/"); # PROCESSO SEMPRE VAI ESTAR COM SUDO
        path = re.sub(r'\/home\/(.*?)\/', "/home/" + os.environ["SUDO_USER"] + "/",  path) #
        return os.path.normpath(path);

    @staticmethod
    def comparepath(path1, path2):
        path1 = FileHelp.uniformpath(path1);
        path2 = FileHelp.uniformpath(path2); 
        return path1 == path2;

    @staticmethod
    def subtractpath(path_folder, path_file):
        path_folder = FileHelp.uniformpath(path_folder);
        path_file = FileHelp.uniformpath(path_file); 
        return path_file[len(path_folder):];

    @staticmethod
    def splitfile(filename, tmp_dir, chunksize=1048576):
        #chunksize = chunksize * 1048576;
        i = 0;
        sequencia = [];
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    part_path =  tmp_dir + str(i);
                    i = i + 1;
                    sequencia.append( part_path );
                    with open( part_path, "wb" ) as b:
                        b.write( chunk );
                else:
                    break
        return sequencia;
    
    @staticmethod
    def joinfile(files, output_file):
        with open(output_file, "wb") as b:
            for file in files:
                with open(file, 'rb') as f:
                    b.write(f.read())
    @staticmethod
    def encrypt_file(key, iv, in_filename, out_filename, chunksize=64*1024):
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)
        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)
                    outfile.write(encryptor.encrypt(chunk))
    @staticmethod    
    def decrypt_file(key, iv, in_filename, out_filename, chunksize=24*1024):
        with open(in_filename, 'rb') as infile:
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

#if __name__ == "__main__":
#    arquivo_original = 'video.mkv';
#    arquivo_criptografado = 'video.enc.mkv';
#    arquivo_criptografado_join = 'video.enc.join.mkv';
#    arquivo_decifrado = 'video.decifrado.mkv'
#    key = b'12345678901234561234567890123456';
#    iv =  b'1234567890123456';
#    FileHelp.encrypt_file(key, iv, arquivo_original, arquivo_criptografado);
#    files = FileHelp.splitfile(arquivo_criptografado, "file/", 5);
#    FileHelp.joinfile(files, arquivo_criptografado_join);
#    FileHelp.decrypt_file(key, iv, arquivo_criptografado_join, arquivo_decifrado);

