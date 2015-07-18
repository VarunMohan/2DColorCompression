import os
from apiclient import errors
from apiclient import http
from apiclient.http import MediaFileUpload

current_directory = "/"
path_file = os.path.expanduser('~') + "/.current_dir"
dir_id_file = os.path.expanduser('~') + "/.google_path_id"

def get_cur_dir_id():
    f = open(dir_id_file)
    return f.read()

def update_cur_dir_id(new_id):
    f = open(dir_id_file, "w")
    f.write(new_id)

def pwd():
    f = open(path_file)
    return f.read()

def update_pwd(new_dir):
    f = open(path_file, "w")
    f.write(new_dir)

def reset_home():
    update_pwd("")
    update_cur_dir_id("")

def ls(service, limit=100):
    cur_id = get_cur_dir_id()
    results = ""
    if not cur_id:
        results = service.files().list().execute()
        return results.get('items', [])
    else:
        children = service.children().list(folderId=cur_id).execute()
        results = []
        for child in children.get('items', []):
            results.append(service.files().get(fileId=child['id']).execute())
        return results

def cd(service, folder):
    cur_id = get_cur_dir_id()
    results = ls (service)
    new_id = None
    for file in results:
        if file['title'] == folder:
            new_id = file['id']
    if not new_id:
        return False
    update_pwd(pwd() + "/" + folder)
    update_cur_dir_id(new_id)
    return True

def is_folder(f):
    return "application/vnd.google-apps.folder" == f['mimeType']

def is_gdoc(f):
    return "application/vnd.google-apps.document" == f['mimeType']

def delete(service, f):
    try:
        service.files().delete(fileId=f['id']).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def read(service, f):
    contents = ""
    try:
        files = service.files()
        fileId = f['id']
        if is_gdoc(f):
            download_url = files.get(fileId=fileId).execute()['exportLinks']['text/plain']
            resp, contents = service._http.request(download_url)
            if resp.status != 200:
                print 'An error occurred: %s' % error
        else:
            contents = files.get_media(fileId=fileId).execute()
        print 'Contents:', contents
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
    return contents


def pwd():
    return current_directory
