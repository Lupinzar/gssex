from enum import Enum, auto

APPLICATION_NAME = 'gssex'
RELEASE = 'Development Release'

class ScrollMode(Enum):
    FULL = auto()
    COLUMN = auto() #v-scroll only
    CELL = auto()
    LINE = auto()

class Plane(Enum):
    SCROLL_A = 0
    SCROLL_B = 1
    WINDOW = 2