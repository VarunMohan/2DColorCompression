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
    #print("Folders:")
    for folder in folders:
        pass
        #print(folder['title'])
    #print("Docs:")
    for doc in docs:
        print 'Title:', doc['title']
    for doc in docs:
        read(service, doc)
        if doc['id'] == "12DCkdFVRNSTTeFQOgVRODq-wcqp_gqjpeQJD8hKFqo0":
            delete(service, doc)
        #if doc['id'] == "0Bza7xsC4hvoAc3RhcnRlcl9maWxl":
        #    print(read(service, doc))
        #print(doc['title'])
        #read(service, doc)
        #print(doc['id'])
        #print doc['title'], doc['id']
    for doc in docs:
        print doc['title']

if __name__ == '__main__':
    main()
