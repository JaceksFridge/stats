



import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json


assets_dir = './assets/'

with open(os.getcwd() + '/assets.json') as file:
    data = json.load(file)
    hashmap_ext = data['extension_to_folder']


class AssetHandler(FileSystemEventHandler):
    def on_created(self, event):
        
        _, ext = os.path.splitext(event.src_path)
        ext = ext[1:]

        if ext not in hashmap_ext:
            pass
        else:
            try:
                shutil.move(event.src_path, assets_dir + hashmap_ext[ext])
                print(f"{event.src_path} was teleported to {hashmap_ext[ext]}")
            except Exception as e:
                print(f"coulnd't move {event.src_path} to Target Path because of {e}")
                


observer = Observer()
observer.schedule(AssetHandler(), path=".", recursive=False)
observer.start()


try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()
    
    
    