def ls(service, limit=100):
    results = service.files().list(maxResults=limit).execute()
    return results.get('items', [])

def is_folder(f):
    return "application/vnd.google-apps.folder" in f['mimeType']
