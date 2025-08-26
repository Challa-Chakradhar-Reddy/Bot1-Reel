import os

def deleteDownloads():
    downloadsPath = os.path.join(os.getcwd(), "downloads")

    if os.path.exists(downloadsPath):
        deleted_any = False
        for file in os.listdir(downloadsPath):
            if file.endswith(".mp4"):
                try:
                    os.remove(os.path.join(downloadsPath, file))
                    deleted_any = True
                except Exception as e:
                    print(f"⚠️ Could not delete {file}: {e}")
        if deleted_any:
            print("✅ Deleted all downloaded .mp4 files")
        else:
            print("ℹ️ No .mp4 files found to delete")
    else:
        print("ℹ️ Downloads folder does not exist")

if __name__ == "__main__":
    deleteDownloads()
