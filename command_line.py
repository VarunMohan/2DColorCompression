import sys
from utils.credentials import *
from utils.nav_utils import *

def list_files(service):
    files = ls(service)
    directories = [x for x in files if is_folder(x)]
    docs = [x for x in files if not is_folder(x)]
    for doc in docs:
        print("doc: " + doc['title'])
    for dir in directories:
        print("dir: " + dir['title'])

def change_dir(service, pathname):
    if pathname is None:
        reset_home()
    else:
        ret_val = getFolder(service, pathname)
        if not ret_val:
            print("Not a valid path")
    print "Current Path: ", pwd()

def more_file(service, filename):
    file = getFile(service, filename)
    if (file == None):
        print("No such file")
        return
    contents = read(service, file)
    if (contents == None):
        print("No such file")
        return
    print (contents)

def delete_file(service, filename):
    file = getFile(service, filename)
    if file == None:
        print("No such file")
        return
    ret_val = delete(service, file)

def find_file(service, path, pattern):
    results = find(service, path, pattern)
    for result in results:
        path, filename = result[0], result[1]
        print(path)

def ls_command(argv):
    if len(argv) > 0:
        raise Exception('Too many arguments')
    list_files(service)

def cd_command(argv):
    if len(argv) > 1:
        raise Exception('Too many arguments')
    if len(argv) == 0 or argv[0] == '~':
        pathname = None
    elif argv[0][0] == '.':
        pathname = argv[0][1:]
    else:
        pathname = argv[0]
    change_dir(service, pathname)

def more_command(argv):
    if len(argv) < 1:
        raise Exception('Too few arguments')
    if len(argv) > 1:
        raise Exception('Too many arguments')
    more_file(service, argv[0])

def rm_command(argv):
    if argv[0] == '-rf':
        if len(argv) < 2:
            raise Exception('Too few arguments')
        if len(argv) > 2:
             raise Exception('Too many arguments')
        delete_file(service, argv[1])
    else:
        if len(argv) < 1:
            raise Exception('Too few arguments')
        if len(argv) > 1:
             raise Exception('Too many arguments')
        delete_file(service, argv[0])

def find_command(argv):
    if len(argv) < 2:
        raise Exception('Too few arguments')
    if len(argv) > 2:
        raise Exception('Too many arguments')
    find_file(service, argv[0], argv[1])

def upload_command(argv):
    if len(argv) < 1:
        raise Exception('Too few arguments')
    if len(argv) > 2:
        raise Exception('Too many arguments')
    if len(argv) == 1:
        folder = None
    elif argv[1][0] == '.':
        folder = argv[1][1:]
    else:
        folder = argv[1]
    getFolderPartial(service, folder)
    upload_file(service, argv[0], getFile(service, folder.split("/")[-1]), "file")

def pwd_command(argv):
    if len(argv) > 0:
        raise Exception('Too many arguments')
    print pwd()

##### ADD HELP MENU
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Too few arguments')
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    command_arg = sys.argv[1]
    if command_arg == 'ls':
        ls_command(sys.argv[2:])
    elif command_arg == 'cd':
        cd_command(sys.argv[2:])
    elif command_arg == 'more':
        more_command(sys.argv[2:])
    elif command_arg == 'rm':
        more_command(sys.argv[2:])
    elif command_arg == 'find':
        find_command(sys.argv[2:])
    elif command_arg == 'upload':
        upload_command(sys.argv[2:])
    elif command_arg == 'pwd':
        pwd_command(sys.argv[2:])
    else:
        raise Exception('Unrecognized options: {0}'.format(' '.join(sys.argv[1:])))
