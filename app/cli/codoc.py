#!/usr/bin/python3
import argparse, inspect, os, sys, getpass, json;
import colorama, traceback

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
sys.path.append( os.path.dirname(CURRENTDIR) );
sys.path.append( os.path.dirname(os.path.dirname(CURRENTDIR)) );

from api.localconnect import LocalConnect;
from colorama import Fore, Style
from classlib.routine import Routine;

parser = argparse.ArgumentParser(description="");
parser.add_argument("-p", "--port", required=True, help="");
args = parser.parse_args();

def wizardnew(port):
    nome  = input("Digite o nome do projeto: ");
    id    = input("Digite um número único para você que não tenha usado ainda: ");
    url   = input("Informe a URL do site para upload: ");
    token = input("Informe a token de acesso: ");
    password1 = getpass.getpass("Password: ");
    password2 = getpass.getpass("Confirme o password: ");
    if password1 != password2:
        print("O password não confere.");
        return None;
    return Routine.createworkspace(port, id, nome, url, token, password1);

def wizardopen(port):
    path  = input("Path do arquivo (caminho completo): ");
    password1 = getpass.getpass("Password: ");
    return Routine.openworkspace(port, path, password1);

def main(port):
    ultimo_error = None;
    routine = None;
    while True:
        try:
            if routine == None:
                #criar ou abrir
                print("Escolha a opção abaixo:")
                print(" 1 - Para criar um novo workspace;")
                print(" 2 - Para abrir um workspace existente;");
                print(" 0 - Sair do aplicativo.");
                opcao = input("Digite a opção: ").strip();
                if opcao == "0":
                    return;
                elif opcao == "1":
                    routine = wizardnew(port);
                elif opcao == "2":
                    routine = wizardopen(port);
                else:
                    print("Não existe esta opção: ", opcao);
            else:
                print("Escolha a opção abaixo:");
                print(" 1 - Listar o workspace;");
                print(" 2 - Adicionar diretório;");
                print(" 3 - Exportar arquivos para nuvem;");
                print(" 4 - Importar arquivos para o computador local;");
                print(" 5 - Limpar computador local;");
                print(" 6 - Listar arquivos;");
                print(" 7 - Remover arquivo;");
                print(" 8 - Salvar arquivo;");
                print(" 0 - Sair;");
                opcao = input("Digite a opção: ").strip();
                if opcao == "0":
                    if input("Deseja realmente sair do programa (s para sim ou n para não)?") == "s":
                        return;
                elif opcao == "1":
                    print(routine.listworkspace());
                elif opcao == "2":
                    path = input("Informe o path do diretório: ");
                    if os.path.exists( path ):
                        print(routine.appendlocal(path));
                    else:
                        print("Não existe o diretório: ", path);
                elif opcao == "3":
                    print(routine.exportworkspace());
                    if input("Digite (s) para salvar: ") == "s":
                        print(routine.saveworkspace());
                elif opcao == "4":
                    routine.importworkspace();
                elif opcao == "5":
                    print(routine.clearworkspace());
                elif opcao == "6":
                    routine.listfiles();
                elif opcao == "7":
                    routine.listfiles();
                    posicao = input("Informe a posicao [vazio para desistir]:");
                    if posicao.strip() != "":
                        routine.removefile(posicao);
                elif opcao == "8":
                    routine.saveworkspace();
                else:
                    print("Não existe esta opção: ", opcao);
            input("Pressione ENTER para continuar");
            os.system('clear');
        except KeyboardInterrupt:
            sys.exit(0);
        except:
            traceback.print_exc();
            ultimo_error = "Não foi possível executar.";
if __name__ == "__main__":
    main(args.port);




