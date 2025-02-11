from enum import Enum, auto, Flag

APPLICATION_NAME = 'gssex'
AUTHOR_STRING = 'Lupinzar'
GIT_HUB_URL = 'https://github.com/Lupinzar/gssex'

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
