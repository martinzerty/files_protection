import hashlib
from cryptography.fernet import Fernet
import os, shutil

ROOT_DIRECTORY = os.path.abspath(os.getcwd())

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

def create_dirs(split_path):
    split_path.pop(0)
    split_path.pop(0)
    split_path.pop(-1)
    if len(split_path) > 0:
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
    return "data/content/" +"".join( x+'/' for x in path[2:] )[:-1]

def remove_files():
    dir = ROOT_DIRECTORY +'/data/open'
    for x in os.listdir(dir):
        current = dir + '/' + x
        if os.path.isdir(current):
            shutil.rmtree(current)
        else:
            os.remove(current)

def ask_password():
    global f
    print('Clef de déchiffrage :')
    entry = input('>')
    if hashlib.md5(entry.encode('utf-8')).hexdigest() == '0fd344d9fb9c8280afdf0528ece85a23':
        print('Well done.\nFiles opening..')
        f = Fernet(entry.encode('utf-8'))
        for x in get_files("data/open"):
            paste_content(convert_path(x), encrypt_content(f,get_file_content(x)))
        print('Files opened')
        input('Appuyez sur entrer pour supprimer les fichiers déchiffrés.\n>')
        remove_files()
    else:
        print('Well tryed :/')
        exit()


if __name__ == '__main__':
    ask_password()