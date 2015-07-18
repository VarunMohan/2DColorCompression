from utils.credentials import *
from utils.nav_utils import *

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    items = ls(service)
    folders = [x for x in items if is_folder(x)]
    docs = [x for x in items if not is_folder(x)]
    print("Folders:")
    for folder in folders:
        print(folder['title'])
    print("Docs:")
    for doc in docs:
        print(doc['title'])
        print(read(service, doc))

if __name__ == '__main__':
    main()
