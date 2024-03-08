from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PyXScatObserver(Observer):
    Observer().__init__()


class PyXScatHandler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if not event.is_directory:
            print(f"New data file: {event.src_path}")