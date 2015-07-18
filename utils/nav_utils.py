from apiclient import errors
from apiclient import http

current_directory = "/"

def ls(service, limit=100):
    results = service.files().list(maxResults=limit).execute()
    return results.get('items', [])

def is_folder(f):
    return "application/vnd.google-apps.folder" in f['mimeType']

def read(service, f):
    contents = ""
    try:
        contents = service.files().get_media(fileId=f['id']).execute()
    except errors.HttpError, error:
        print(error)
    return contents


def pwd():
    return current_directory
