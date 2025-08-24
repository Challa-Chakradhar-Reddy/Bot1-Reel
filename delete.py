import shutil
import os

def deleteDownloads():
    downloadsPath = os.path.join(os.getcwd(), "downloads")
    if os.path.exists(downloadsPath):
        shutil.rmtree(downloadsPath)
        print("delted")
    else : print("downloads not exist to delete")
    

if __name__ == "__main__": deleteDownloads()