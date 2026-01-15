from typing import Tuple
from os.path import isdir, isfile, dirname, basename, realpath
from os import scandir
from gssex.state import SaveState, Palette, FORMAT_FUNCTIONS, load_wrapper
import json
from PIL.ImageQt import ImageQt as ImageQt
from PIL.Image import Image
from PySide6.QtGui import QGuiApplication, QKeySequence
from copy import deepcopy

class App():
    DEFAULT_STATUS_TIMEOUT = 4000
    def __init__(self):
        self.config: Config = Config()
        self.shortcuts: Shortcuts = Shortcuts()
        self.directory: str|None = None
        self.current_file: str|None = None
        self.valid_file: bool = False
        self.savestate: SaveState|None = None
        self.file_list: list = []
        self.global_pal: Palette = Palette.make_unique()
        self.state_pal: Palette
        self.use_global_pal: bool = False

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
            if new_index < 0 or new_index >= len(self.file_list):
                return False
            self.current_file = self.file_list[new_index]
            self.valid_file = False
            self.savestate = None
            return True
        except:
            return False
        
    def load_state(self, format: str) -> bool:
        #important to reset this
        self.valid_file = False
        try:
            self.savestate = load_wrapper(self.make_path(), format)
            self.state_pal = Palette.from_cram(self.savestate.c_ram_buffer)
            self.valid_file = True
        except Exception as e:
            #TODO: logging
            pass
        return self.valid_file

    def make_path(self) -> str:
        return f'{self.directory}/{self.current_file}'
    
    #does the dirty work of figuring out which palette to use and if we need to replace the bg color based on our config
    def get_palette_and_background(self) -> Tuple[int, Palette]:
        if self.use_global_pal or not self.valid_file:
            palref = self.global_pal
        else:
            palref = self.state_pal
        palette = deepcopy(palref)

        if self.config.override_background:
            bgindex = 0
            palette.colors[0] = Palette.int_to_tuple(self.config.override_color)
        else:
            bgindex = self.savestate.vdp_registers.bg_color_index #type: ignore
        return (bgindex, palette)

    def save_image(self, image: Image, path: str) -> bool:
        try:
            image.save(path)
            return True
        except Exception:
            return False
        
    def build_image_output_path(self, key: str) -> str:
        return f'{self.config.output_path}/{basename(self.current_file)}_{key}.png' #type: ignore

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
        
class Shortcuts:
    FIELD_DESC = 0
    FIELD_SEQUENCE = 1
    
    SAVE_PATH = realpath("./keys.json")
    KEY_MAP = {
        'shortcut_palette_swap': ('Toggle Palette', 'R'),
        'save_primary': ('Save (primary)', 'F'),
        'copy_primary': ('Copy to clipboard (primary)', 'C'),
        'save_secondary': ('Save (secondary)', 'Ctrl+F'),
        'copy_secondary': ('Copy to clipboard (secondary)', 'Ctrl+C'),
        'loupe_inc_single': ('Tile Loupe forward single tile', 'Right'),
        'loupe_dec_single': ('Tile Loupe backward single tile', 'Left'),
        'loupe_inc_whole': ('Tile Loupe forward sprite size', 'Up'),
        'loupe_dec_whole': ('Tile Loupe backward sprite size', 'Down'),
        'loupe_inc_width': ('Tile Loupe increase width', 'Ctrl+Right'),
        'loupe_dec_width': ('Tile Loupe decrease width', 'Ctrl+Left'),
        'loupe_inc_height': ('Tile Loupe increase height', 'Ctrl+Up'),
        'loupe_dec_height': ('Tile Loupe decrease height', 'Ctrl+Down'),
        'raw_inc_byte': ('RAW Tiles increase 1 byte', 'D'),
        'raw_dec_byte': ('RAW Tiles decrease 1 byte', 'A'),
        'raw_inc_tile': ('RAW Tiles increase 1 tile', 'W'),
        'raw_dec_tile': ('RAW Tiles decrease 1 tile', 'S'),
        'raw_inc_width': ('RAW Tiles increase width', 'Ctrl+D'),
        'raw_dec_width': ('RAW Tiles decrease width', 'Ctrl+A'),
        'raw_inc_height': ('RAW Tiles increase height', 'Ctrl+W'),
        'raw_dec_height': ('RAW Tiles decrease height', 'Ctrl+S'),
        'raw_inc_line': ('RAW Tiles increase line', 'Shift+D'),
        'raw_dec_line': ('RAW Tiles decrease line', 'Shift+A'),
        'raw_inc_page': ('RAW Tiles increase page', 'Shift+W'),
        'raw_dec_page': ('RAW Tiles decrease page', 'Shift+S')
    }
    sequences: dict[str, str] = {}

    def __init__(self):
        self.load_defaults()

    def load(self) -> bool:
        if not isfile(self.SAVE_PATH):
            self.load_defaults()
            return True
        try:
            with open(self.SAVE_PATH, 'r') as fp:
                data = json.load(fp)
            if not isinstance(data, dict):
                return False
            for k, v in data.items():
                if k not in self.KEY_MAP or not isinstance(v, str): #bogus entries (errors, hand editing)
                    continue
                self.sequences[k] = v
            return True
        except:
            return False
        
    def save(self) -> bool:
        try:
            with open(self.SAVE_PATH, 'w') as fp:
                json.dump(self.sequences, fp)
            return True
        except Exception as e:
            return False
        
    def load_defaults(self):
        for name in self.KEY_MAP:
            self.sequences[name] = self.KEY_MAP[name][self.FIELD_SEQUENCE]

    def get_sequence(self, name: str) -> QKeySequence:
        return QKeySequence.fromString(self.sequences.get(name, ''))
    
    def get_sequences(self) -> dict[str, str]:
        return self.sequences
    
    def set_sequence(self, name: str, str_sequence: str):
        self.sequences[name] = str_sequence
        
def pil_to_qimage(image: Image) -> ImageQt:
    return ImageQt(image)

def pil_to_clipboard(image: Image):
    clipboard = QGuiApplication.clipboard()
    clipboard.setImage(pil_to_qimage(image))