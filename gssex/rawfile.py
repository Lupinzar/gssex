from typing import BinaryIO
from os import fstat
from os.path import basename, dirname
from mmap import mmap, ACCESS_READ

class RawFile():
    def __init__(self, path: str):
        self.path: str = path
        self.handle: BinaryIO = open(path, 'rb')
        self.size: int = fstat(self.handle.fileno()).st_size
        self.mmap: mmap = mmap(self.handle.fileno(), 0, access=ACCESS_READ)

    def basename(self) -> str:
        return basename(self.path)
    
    def dirname(self) -> str:
        return dirname(self.path)

    def close(self):
        try:
            if not self.mmap.closed:
                self.mmap.close()
            if not self.handle.closed:
                self.handle.close()
        except:
            #slient failure for now
            #TODO log me
            pass

    def __del__(self):
        self.close()

class BinarySearch():
    def __init__(self, file: RawFile, term: bytearray):
        self.found: bool = False
        self.last: int|None = None
        self.file: RawFile = file
        self.term: bytearray = term
        self.looped: bool = False

    def first(self) -> bool:
        result = self.file.mmap.find(self.term, 0)
        return self.process_result(result)
    
    def next(self) -> bool:
        self.looped = False
        if self.last is None:
            return self.first()
        result = self.file.mmap.find(self.term, self.last + 1)
        if self.process_result(result):
            return True
        self.looped = True
        result = self.file.mmap.find(self.term, 0, self.last)
        if self.process_result(result):
            return True
        return False
    
    def prev(self) -> bool:
        self.looped = False
        if self.last is None:
            return self.first()
        result = self.file.mmap.rfind(self.term, 0, self.last)
        if self.process_result(result):
            return True
        self.looped = True
        result = self.file.mmap.rfind(self.term, self.last)
        if self.process_result(result):
            return True
        return False

    def process_result(self, result: int) -> bool:
        if result < 0:
            return False
        self.found = True
        self.last = result
        return True
