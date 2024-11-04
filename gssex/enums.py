from enum import Enum, auto

class ScrollMode(Enum):
    FULL = auto()
    COLUMN = auto() #v-scroll only
    CELL = auto()
    LINE = auto()
