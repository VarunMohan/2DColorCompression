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
    if pathname == "~":
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


##### ADD HELP MENU
if __name__ == '__main__':
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    if len(sys.argv) <= 1:
        print("No")
        sys.exit(0)
    command_arg = sys.argv[1]
    if command_arg == 'ls':
        list_files(service)
    if command_arg == 'cd':
        if sys.argv[2][0] == '.' :
            sys.argv[2] = sys.argv[2][1:]
        change_dir(service, sys.argv[2])
    if command_arg == 'more':
        more_file(service, sys.argv[2])
    if command_arg == 'rm':
        if (sys.argv[2]=='-rf') :
            delete_file(service, sys.argv[3])
        else:
            delete_file(service, sys.argv[2])
    if command_arg == 'find':
        find_file(service, sys.argv[2], sys.argv[3])
    if command_arg == 'upload':
        if sys.argv[3][0] == '.' :
            sys.argv[3] = sys.argv[3][1:]
        folder = sys.argv[3]
        getFolderPartial(service, folder)
        upload_file(service, sys.argv[2], getFile(service, folder.split("/")[-1]), "file")
    if command_arg == 'pwd':
        print pwd()
