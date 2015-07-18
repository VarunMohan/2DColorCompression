from apiclient import errors
from apiclient import http
from apiclient.http import MediaFileUpload


current_directory = "/"

def ls(service, limit=100):
    results = service.files().list(maxResults=limit).execute()
    return results.get('items', [])

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
