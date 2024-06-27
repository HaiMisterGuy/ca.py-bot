import pyinotify
import importlib
import re
import os

def is_module(filepath):
    return os.path.splitext(filepath)[1] == ".py"

class ModuleLoader(pyinotify.ProcessEvent):
    def my_init(self, module_dir_path, verbose=False):
        self.module_dir_path = module_dir_path
        self.verbose = verbose
        self.__modules = dict()
        self.__notifier = None
        self.__watch_flags = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE
        self.__exclude_list = ["__init__.py"]
    
    def run(self, loop):
        self.load_all_modules()

        wm = pyinotify.WatchManager()
        self.__notifier = pyinotify.AsyncioNotifier(wm, loop, default_proc_fun=self)
        wm.add_watch(self.module_dir_path, self.__watch_flags, exclude_filter=pyinotify.ExcludeFilter(self.__exclude_list))

    def get_modules(self):
        return [m for m in self.__modules.values()]

    def stop(self):
        if self.__notifier:
            self.__notifier.stop()

    def reload_module(self, filepath):
        try:
            module = importlib.reload(self.__modules.get(filepath))
            return module
        except Exception as ex:
            print("Failed to reload module at %s: %s" % (filepath, ex))

    def force_load_module(self, filepath):
        file_basename = os.path.splitext(os.path.basename(filepath))[0]
        module_name = "." + os.path.basename(self.module_dir_path) + "." + file_basename
        parent_name = os.path.basename(os.path.dirname(__file__))
        try:
            module = importlib.import_module(module_name, parent_name)
            return module
        except Exception as ex:
            print("Failed to load module at %s: %s" % (filepath, ex))

    def load_module(self, filepath):
        if is_module(filepath):
            should_reload = filepath in self.__modules
            module = self.reload_module(filepath) if should_reload else self.force_load_module(filepath)
            if module:
                if self.verbose:
                    print("Loaded module at %s" % filepath)
                self.__modules[filepath] = module

    def load_all_modules(self):
        for filename in os.listdir(self.module_dir_path):
            if is_module(filename) and filename not in self.__exclude_list:
                filepath = self.module_dir_path + "/" + filename
                self.load_module(filepath)

    def unload_module(self, filepath):
        if filepath in self.__modules:
            print("deleting %s", filepath)
            del self.__modules[filepath]

    def process_IN_CREATE(self, event):
        self.load_module(event.pathname)
    
    def process_IN_DELETE(self, event):
        self.unload_module(event.pathname)
    
    def process_IN_CLOSE_WRITE(self, event):
        self.load_module(event.pathname)
