from enum import Enum, auto

APPLICATION_NAME = 'gssex'
RELEASE = 'Development Release'

class ScrollMode(Enum):
    FULL = auto()
    COLUMN = auto() #v-scroll only
    CELL = auto()
    LINE = auto()