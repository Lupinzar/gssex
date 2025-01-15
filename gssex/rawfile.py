from typing import BinaryIO
from os import fstat
from os.path import basename, dirname

class RawFile():
    def __init__(self, path: str):
        self.path: str = path
        self.handle: BinaryIO = open(path, 'rb')
        self.size: int = fstat(self.handle.fileno()).st_size

    def basename(self) -> str:
        return basename(self.path)
    
    def dirname(self) -> str:
        return dirname(self.path)

    def close(self):
        if self.handle:
            self.handle.close()

    def __del__(self):
        self.close()