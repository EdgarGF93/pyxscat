import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from pathlib import Path
import numpy as np
import random
import fabio
from datetime import datetime
import os

LOG_ARGS = {
    "name" : "logger",
    "level" : logging.INFO,
    "format" : "%(asctime)s - %(message)s",
    "datefmt" : "%Y-%m-%d %H:%M:%S",
}
logger = logging.getLogger(LOG_ARGS["name"])
logger.setLevel(LOG_ARGS["level"])

console_handler = logging.StreamHandler()
formatter = logging.Formatter(LOG_ARGS["format"])
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

class FileGenerator():
    def __init__(self, directory=None, extension=".edf", number=5, latency=1) -> None:
        if directory is None:
            epoch = int(datetime.timestamp(datetime.now()))
            self.directory = Path(f"/tmp/dummydata_{str(epoch)}")
            self.directory.mkdir(exist_ok=True)
        self.extension = extension
        self.number = number
        self.latency = latency

    def generate(self):
        for _ in range(self.number):
            time.sleep(self.latency)
            arr = np.random.random((1000,1000))
            obj = fabio.edfimage.EdfImage(data=arr)
            epoch = int(datetime.timestamp(datetime.now()))
            name = f"data_{str(epoch)}.edf"
            path = self.directory.joinpath(name)
            obj.write(path)
    
    def _dispose(self):
        os.system(f"rm -rf {self.directory}")

            
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, pattern="*.edf"):
        self._pattern = pattern
        
    def on_any_event(self, event):
        if event.event_type == "created" and event.is_directory == False:
            filename = event.src_path
            if Path(filename).match(self._pattern):
                print("hola")
                
        
        
class RootDirObserver():
    def __init__(self, root_directory=None) -> None:
        self._observer = Observer()
        self._event_handler = NewFileHandler()        
        self.root_directory = root_directory

    def __repr__(self) -> str:
        return f"This observer is watching at {self._root_directory}"
    
    def __str__(self) -> str:
        return str(self.root_directory)
    
    @property
    def root_directory(self):
        return self._root_directory
    
    @root_directory.setter
    def root_directory(self, path):
        if path is None:
            return
        if isinstance(path, (Path, str)):
            path = Path(path)
            if path.exists():
                self._root_directory = path
                self._observer.schedule(
                    event_handler=self._event_handler, 
                    path=path, 
                    recursive=True,
                )
            else:
                logger.warning(f"Path {path} does not exists.")
                return
        else:
            logger.warning(f"{path} is not pathlib.")
            return
        
    def start_observer(self):
        self._observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
        self._observer.join()






# if __name__ == "__main__":
#     # path = Path("/home/edgar/work/nankurunaisa")
#     # observer = RootDirObserver(root_directory=path)
#     # observer
#     # observer.start_observer()
#     gen = FileGenerator()
#     gen.generate()
    



