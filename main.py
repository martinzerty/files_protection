import hashlib
from cryptography.fernet import Fernet
import os, shutil, getpass, sys

ROOT_DIRECTORY = os.path.abspath(os.getcwd())


def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')

def get_files(directory):
    file_list = []
    for i in os.listdir(directory):
        if os.path.isdir(ROOT_DIRECTORY+'/'+directory+'/'+i):
            for x in get_files(directory+'/'+i):
                file_list.append(x)
        else:
            file_list.append(directory+'/'+i)
    return file_list

def get_file_content(path):
    with open(path,'rb') as file:
        content = file.read()
    return content

def encrypt_content(f, content):
    return f.encrypt(content).decode('utf-8')

def decrypt_content(f, content):
    return f.decrypt(content).decode('utf-8')

def create_dirs(split_path):
    split_path.pop(0)
    split_path.pop(0)
    split_path.pop(-1)
    if len(split_path) > 0:
        sens = check_args()
        if sens == 'open':
            added_directory = ROOT_DIRECTORY + '/data/open/' + split_path[0]
        else:
            added_directory = ROOT_DIRECTORY + '/data/content/' + split_path[0]
        for x in range(0,len(split_path)):
            if not os.path.exists(added_directory):
                os.mkdir(added_directory)
            added_directory+=split_path[x]

def paste_content(path, content):
    split_path = path.split('/')
    create_dirs(split_path)
    with open(path, 'w') as file:
        file.write(content)

def convert_path(path):
    path = path.split('/')
    if path[1] == 'open':
        start = "data/content/"
    elif path[1] == 'content':
        start = "data/open/"
    else:
        print('C\'est pas un bon chemin ça !')
        quit()
    return start +"".join( x+'/' for x in path[2:] )[:-1]

def remove_files():
    dir = ROOT_DIRECTORY +'/data/open'
    for x in os.listdir(dir):
        current = dir + '/' + x
        if os.path.isdir(current):
            shutil.rmtree(current)
        else:
            os.remove(current)

def check_args():
    args = sys.argv
    if len(args) < 2:
        print('Veuillez indiquer un sens (\'open\' ou \'close\'')
        return False
    else:
        if args[1] in ['open', 'close']:
            return args[1]
        else:
            print('Veuillez indiquer un sens (\'open\' ou \'close\'')
            return False

def open_files():
    files = get_files('data/content')
    count = 1
    long = len(files)
    not_crypted_files = ['.DS_Store']
    print(files)
    for x in files:
        print(f'Converting [{count}/{long}]')
        if x.split('/')[-1] not in not_crypted_files:
            paste_content(convert_path(x), decrypt_content(f,get_file_content(x)))
        count+=1
        delete_last_line()
    print('Files opened')
    input('Appuyez sur entrer pour supprimer les fichiers déchiffrés.\n>')
    remove_files()

def crypt_files():
    files = get_files('data/open')
    count = 1
    long = len(files)
    not_crypted_files = ['.DS_Store']
    for x in files:
        print(f'Converting [{count}/{long}]')
        if x.split('/')[-1] not in not_crypted_files:
            paste_content(convert_path(x), encrypt_content(f,get_file_content(x)))
        delete_last_line()
        count+=1
    print('Files crypted')
    input('Appuyez sur entrer pour supprimer les fichiers déchiffrés.\n>')
    remove_files()


def ask_password():
    global f
    print('Clef de déchiffrage :')
    entry = getpass.getpass(prompt='>')
    if hashlib.md5(entry.encode('utf-8')).hexdigest() == '0fd344d9fb9c8280afdf0528ece85a23':
        sens = check_args()
        f = Fernet(entry.encode('utf-8'))
        if not sens:
            return
        elif sens == 'open':
            print('Well done.\nFiles opening..')
            open_files()
        elif sens == 'close':
            print('Well done.\nFiles crypting..')
            crypt_files()
        else:
            print('Mauvais paramètre.')
            return 
    else:
        print('Well tryed :/')
        exit()


if __name__ == '__main__':
    ask_password()