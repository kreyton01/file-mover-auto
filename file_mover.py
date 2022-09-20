from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install watchdog

import shutil
import os
import json
import time


class MyHandler(FileSystemEventHandler):
    def MoveFile(self, src, dest, copyNum):
        try:
            if not os.path.exists(dest):
                shutil.move(src, dest)
                print("New path file: {}".format(dest))
            else:
                split = dest.split('.')
                pathNoExt = split[0]
                ext = str()
                i = 1
                while i < len(split):
                    ext += "." + split[i]
                    i += 1
                pathNoExt.removesuffix("{}".format(copyNum - 1))
                dest = "{}{}{}".format(pathNoExt, copyNum, ext)
                self.MoveFile(src, dest, copyNum + 1)
        except:
            print("Error: unable to move file: " + src)


    def on_modified(self, event):
        for filename in os.listdir(sourceFolder):
            srcFilepath = sourceFolder + "/" + filename
            destDirectory = str()

            for (path, exts) in destFolders.items():
                for ext in exts:
                    if (filename.lower().endswith(ext)):
                        destDirectory = path
                        print("Extension match: '{}' ".format(ext))
                        print("Path: '{}'".format(srcFilepath))

            if (len(destDirectory) > 0):
                destPath = destDirectory + "/" + filename
                self.MoveFile(srcFilepath, destPath, 1)


sourceFolder = "C:/Users/Acer/Downloads/"
destFolders = {
    "C:/Users/Acer/Downloads/Pictures": [".png", ".jpeg", ".jpg"],
    "C:/Users/Acer/Downloads/Programs": [".exe", ".msi"],
    "C:/Users/Acer/Downloads/Music": [".mp3", ".wav", ".flac",],
    "C:/Users/Acer/Downloads/Videos": [".mp4", ".mkv"],

}

# Main
event_handler = MyHandler()

observer = Observer()
observer.schedule(event_handler, sourceFolder, recursive=True)
observer.start()

try:
    for (path, exts) in destFolders.items():
        for ext in exts:
            os.makedirs(path, exist_ok=True)
            print("File redirect: {} -> {}".format(ext, path))

    print("Entering loop")
    while True:
        time.sleep(10)
    print("Loop terminated")
except:
    observer.stop()

print("Observer joining")
observer.join()