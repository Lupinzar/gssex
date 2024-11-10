from typing import Tuple
from os.path import isdir, isfile, dirname, basename
from os import scandir
from ..state import SaveState

class App():
    DEFAULT_STATUS_TIMEOUT = 3000
    def __init__(self):
        self.directory = None
        self.current_file = None
        self.valid_file = False
        self.savestate: SaveState = None
        self.file_list: list = []

    def open_directory(self, path) -> bool:
        if not isdir(path):
            return False
        self.directory = path
        self.current_file = None
        self.valid_file = False
        self.savestate = None
        self.load_file_list()
        return True
    
    def open_file(self, path) -> bool:
        if not isfile(path):
            return False
        if not self.allowed_extension(path):
            return False
        self.directory = dirname(path)
        self.current_file = basename(path)
        self.valid_file = False
        self.savestate = None
        self.load_file_list()
        return True
    
    def load_file_list(self):
        self.file_list.clear()
        with scandir(self.directory) as iter:
            for entry in iter:
                if not entry.is_file():
                    continue
                if not self.allowed_extension(entry.name):
                    continue
                self.file_list.append(entry.name)
        self.file_list.sort()

    def select_first_file(self) -> bool:
        if not len(self.file_list):
            return False
        self.current_file = self.file_list[0]
        return True
        
    def adjust_file_index(self, increment: int) -> bool:
        if not self.directory:
            return False
        self.load_file_list()
        try:
            new_index = self.file_list.index(self.current_file) + increment
            print(new_index)
            if new_index < 0 or new_index >= len(self.file_list):
                return False
            self.current_file = self.file_list[new_index]
            self.valid_file = False
            self.savestate = None
            return True
        except:
            return False        

    #gens formatted for now...
    @staticmethod
    def allowed_extension(filename: str) -> bool:
        return filename.lower()[-3:-1] == 'gs'
    
class Config():
    def __init__(self):
        self.use_neutral: bool = True
        self.neutral_color: Tuple = (0xFB, 0x8C, 0xFF)
        self.state_format: str = 'gens_legacy'