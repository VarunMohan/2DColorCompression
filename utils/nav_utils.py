from apiclient import errors
from apiclient import http
from apiclient.http import MediaFileUpload


current_directory = "/"

def ls(service, limit=100):
    results = service.files().list(maxResults=limit).execute()
    return results.get('items', [])

def is_folder(f):
    return "application/vnd.google-apps.folder" in f['mimeType']

def delete(service, f):
    try:
        service.files().delete(fileId=f['id']).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def read(service, f):
    contents = ""
    try:
        contents = service.files().get_media(fileId=f['id']).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
    return contents


def pwd():
    return current_directory
