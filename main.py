import time
import json
import os
import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

print("papermerge 2.1.x auto-importer by mxx-lxg")

print(os.getenv("PAPERMERGE_HOST"))

path = "./dropzone"
host = os.getenv("PAPERMERGE_HOST")
auth_token = os.getenv("AUTH_TOKEN")

def getInboxId():
    print("getting inbox id for user")
    r = requests.get(host + '/api/users/me/', headers={'Authorization': 'Token ' + auth_token, 'Content-Type': 'application/vnd.api+json'})
    print(r.status_code)
    data = r.json()["data"]
    print(data["relationships"]["inbox_folder"]["data"]["id"])
    inbox_id = data["relationships"]["inbox_folder"]["data"]["id"]

    return inbox_id


def createFile(inbox_id, file_name):
    print("creating file entry in papermerge")
    clean_file_name = file_name.replace('./dropzone/', '')
    print(clean_file_name)
    r = requests.post(
        host + '/api/nodes/', 
        headers={'Authorization': 'Token ' + auth_token, 'Content-Type': 'application/vnd.api+json'},
        data= json.dumps({
            "data": {
                "type": "documents",
                "attributes": {
                    "title": clean_file_name
                },
                "relationships": {
                    "parent": {
                        "data": {
                            "type": "folders",
                            "id": inbox_id
                        }
                    }
                }
            }
        }))
    print(r.status_code)
    data = r.json()["data"]
    print(data)
    print(data["id"])
    return data["id"]

def uploadFile(document_id, file_name):
    print("uploading file to papermerge ("+document_id+")")
    clean_file_name = file_name.replace('./dropzone/', '')
    print(clean_file_name)
    r = requests.put(
        host + '/api/documents/' + document_id + '/upload/' + clean_file_name, 
        headers={'Authorization': 'Token ' + auth_token, 'Content-Type': 'Content-Type: application/pdf', 'Content-Disposition': 'attachment; filename=' + clean_file_name},
        files={'file': open(file_name, 'rb')}
    )
    print(r)
    print(r.status_code)
    print(r.json()["data"])

def deleteLocalFile(file_name):
    print("deleting local file")
    os.remove(file_name)



if __name__ == "__main__":
    patterns = ["*.pdf"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    file_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def handleFile(event):
    print("********" + event.src_path + " has appeared! *****************")
    inbox_id = getInboxId()
    document_id = createFile(inbox_id, event.src_path)
    uploadFile(document_id, event.src_path)
    deleteLocalFile(event.src_path)
    print("")
    print("******** done **************************")
    print("")


file_event_handler.on_closed = handleFile

go_recursively = False
file_observer = Observer()
file_observer.schedule(file_event_handler, path, recursive=go_recursively)

file_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    file_observer.stop()
    file_observer.join()