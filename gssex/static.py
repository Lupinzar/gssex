from enum import Enum, auto, Flag

APPLICATION_NAME = 'gssex'
AUTHOR_STRING = 'Lupinzar'
GIT_HUB_URL = 'https://github.com/Lupinzar/gssex'
SAVESTATE_DIALOG_TYPES = 'Save states (*.gs? *.exs)'

class ScrollMode(Enum):
    FULL = auto()
    COLUMN = auto() #v-scroll only
    CELL = auto()
    LINE = auto()

class Plane(Enum):
    SCROLL_A = 0
    SCROLL_B = 1
    WINDOW = 2

class Priority(Flag):
    LOW = 0x1
    HIGH = 0x2
    BOTH = 0x3

class Endian(Enum):
    BIG = auto()
    LITTLE = auto()

class Exodus():
    CRAM_NAME: str = 'MD1600.VDP - CRAM.bin'
    VRAM_NAME: str = 'MD1600.VDP - VRAM.bin'
    VSRAM_NAME: str = 'MD1600.VDP - VSRAM.bin'
    VDP_REG_NAME: str = 'MD1600.VDP.Registers.bin'
    FORMAT: str = 'exodus'
    FILE_EXT: str = '.exs'
