from typing import Tuple
from os.path import isdir, isfile, dirname, basename, realpath
from os import scandir
from ..state import SaveState, Palette, FORMAT_FUNCTIONS
import json

class App():
    DEFAULT_STATUS_TIMEOUT = 3000
    def __init__(self):
        self.directory = None
        self.current_file = None
        self.valid_file = False
        self.savestate: SaveState = None
        self.file_list: list = []
        self.global_pal: Palette = Palette.make_unique()

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
    CONFIG_PATH = realpath("./gssex.json")

    def __init__(self):
        self.override_background: bool = True
        self.override_color: int = 0xFB8CFF
        self.state_format: str = 'gens_legacy'
        self.output_path: str = realpath('.')

    def load(self) -> bool:
        if not isfile(self.CONFIG_PATH):
            return False
        try:
            with open(self.CONFIG_PATH, 'r') as fp:
                data = json.load(fp)
            if 'override_background' in data:
                self.override_background = bool(data['override_background'])
            if 'override_color' in data:
                self.override_color = int(data['override_color'])
            if 'state_format' in data and data['state_format'] in FORMAT_FUNCTIONS:
                self.state_format = data['state_format']
            if 'output_path' in data and isdir(data['output_path']):
                self.output_path = data['output_path']
            return True
        except:
            return False
        
    def save(self) -> bool:
        try:
            data = {}
            members = ['override_background', 'override_color', 'state_format', 'output_path']
            for key in members:
                data[key] = getattr(self, key)
            with open(self.CONFIG_PATH, 'w') as fp:
                json.dump(data, fp)
            return True
        except Exception as e:
            return False