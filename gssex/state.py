from dataclasses import dataclass
from typing import BinaryIO, Tuple, Iterable
from struct import Struct
from .static import ScrollMode

class Buffer:
    def __init__(self, data: bytearray):
        self.data = data
        self.position = 0
    def seek(self, position: int):
        if position >= len(self.data):
            raise Exception('Tried to seek beyond buffer length')
        self.position = position
    def read_bytes(self, length: int, position: int = None) -> bytearray:
        if position is None:
            position = self.position
        end = position + length
        if position >= len(self.data) or end > len(self.data):
            raise Exception('Tried to read beyond buffer')
        return self.data[position:end]
    def read_struct(self, struct: Struct, position: int = None) -> Tuple:
        return struct.unpack(self.read_bytes(struct.size, position))

@dataclass
class VDPRegisters:
    cells_high: int
    address_scroll_a: int
    address_window: int
    address_scroll_b: int
    address_sprites: int
    bg_color_index: int
    scroll_mode_v: int
    scroll_mode_h: int
    cells_wide: int
    shadow_enable: bool
    address_scroll_h: int
    scroll_width: int
    scroll_height: int
    window_right: bool
    window_split_h: int
    window_down: bool
    window_split_v: int
    SIZE = 24 #in bytes

    @staticmethod
    def get_scroll_size(bits: int) -> int:
        if bits & 3 == 3:
            return 128
        if bits & 1 == 1:
            return 64
        return 32

    @staticmethod
    def get_scroll_mode_v(bits: int) -> ScrollMode:
        if bits & 0x04:
            return ScrollMode.COLUMN
        return ScrollMode.FULL

    @staticmethod
    def get_scroll_mode_h(bits: int) -> ScrollMode:
        if (bits & 0x03) == 0:
            return ScrollMode.FULL
        if (bits & 0x03) == 2:
            return ScrollMode.CELL
        return ScrollMode.LINE
    
    @classmethod
    def read_vdp_registers(cls, buffer: Buffer) -> 'VDPRegisters':
        vdp_struct = Struct(f'{cls.SIZE}B')
        data = buffer.read_struct(vdp_struct, 0)
        return cls(
            30 if data[1] & 0x08 else 28,
            (data[2] & 0x38) << 10,
            (data[3] & 0x3E) << 10,
            (data[4] & 0x07) << 13,
            (data[5] & 0x7F) << 9,
            data[7],
            cls.get_scroll_mode_v(data[11]),
            cls.get_scroll_mode_h(data[11]),
            40 if data[12] & 0x81 else 32,
            bool(data[12] & 0x3F),
            (data[13] & 0x3F) << 10,
            cls.get_scroll_size(data[16] & 0x03),
            cls.get_scroll_size((data[16] & 0x30) >> 4),
            bool(data[17] & 0x80),
            data[17] & 0x1F,
            bool(data[18] & 0x80),
            data[18] & 0x1F
        )
    
class SaveState:
    VRAM_SIZE = 0x10000
    CRAM_SIZE = 128
    VSRAM_SIZE = 80

    def __init__(self, c_ram_buffer: bytearray, v_ram_buffer: bytearray, vs_ram_buffer: bytearray, vdp_registers: type[VDPRegisters]):
        self.c_ram_buffer: Buffer = c_ram_buffer
        self.v_ram_buffer: Buffer = v_ram_buffer
        self.vs_ram_buffer: Buffer = vs_ram_buffer
        self.vdp_registers: Buffer = vdp_registers

class Palette:
    SIZE = 16
    GROUP_SIZE = 4

    map = {
        0x0: 0x00,
        0x2: 0x24,
        0x4: 0x49,
        0x6: 0x6D,
        0x8: 0x92,
        0xA: 0xB6,
        0xC: 0xDB,
        0xE: 0xFF
    }

    def __init__(self, colors: list):
        self.colors = colors

    def flattened_colors(self) -> list:
        return [part for color in self.colors for part in color]
    
    def get_color_as_rgb(self, index: int) -> int:
        color = self.colors[index]
        return (color[0] << 16) | (color[1] << 8) | color[2]
    
    @classmethod
    def from_cram(cls, buffer: Buffer) -> 'Palette':
        data = buffer.read_struct(
            Struct(f'<{cls.SIZE * cls.GROUP_SIZE}H'),
            0
        )
        colors = []
        for gen_color in data:
            color = (
                cls.map[gen_color & 0x000E],
                cls.map[(gen_color & 0x00E0) >> 4],
                cls.map[(gen_color & 0x0E00) >> 8]
            )
            colors.append(color)
        return cls(colors)
    
    @classmethod
    def make_unique(cls) -> 'Palette':
        pals = [[],[],[],[]]
        for ndx in range(0, cls.SIZE):
            val = (ndx + 1) * 16 - 1
            pals[0].append((val, val, val))
            pals[1].append((val, 0, 0))
            pals[2].append((0, val, 0))
            pals[3].append((0, 0, val))
        return cls(pals[0] + pals[1] + pals[2] + pals[3])

    @staticmethod
    def make_index(palette: int, index: int):
        return (palette << 4) | index

    @staticmethod
    def is_transparent(index: int):
        return bool(index & 0x0F)
    
@dataclass
class HardwareSprite:
    x: int
    y: int
    width: int
    height: int
    link: int
    pal: int
    priority: bool
    vflip: bool
    hflip: bool
    start: int

class SpriteTable:
    SIZE = 80
    
    def __init__(self, state: SaveState):
        self.save_state = state
        self.sprites: list[HardwareSprite] = []
        self.load()

    def load(self):
        record_struct = Struct('>hBBHh')
        buffer = self.save_state.v_ram_buffer
        buffer.seek(self.save_state.vdp_registers.address_sprites)
        for ndx in range(0, SpriteTable.SIZE):
            data = buffer.read_struct(record_struct)
            sprite = HardwareSprite(
                data[4],
                data[0],
                ((data[1] & 0x0C) >> 2) + 1,
                (data[1] & 0x03) + 1,
                data[2] & 0x7F,
                (data[3] & 0x6000) >> 13,
                bool(data[3] & 0x8000),
                bool(data[3] & 0x1000),
                bool(data[3] & 0x0800),
                data[3] & 0x07FF
            )
            self.sprites.append(sprite)
    
    def get_draw_list(self) -> list:
        order = []
        index = 0
        while True:
            order.append(index)
            link = self.sprites[index].link
            if link == 0:
                break
            #infinite loop check
            if link in order:
                break
            index = link
        return reversed(order)

class PatternData:

    def __init__(self, buffer: Buffer, tile_size: Tuple = (8, 8), use_cache=False):
        self.buffer: Buffer = buffer
        self.tile_width: int = tile_size[0]
        self.tile_height: int = tile_size[1]
        self.tile_byte_size: int = (self.tile_width * self.tile_height) // 2
        self.use_cache: bool = use_cache
        self.cache: dict = {}

    def get_pattern(self, address: int, palette: int) -> list:
        cache_key = f'{address}_{palette}'
        if self.use_cache and cache_key in self.cache:
            #print('cache hit')
            return self.cache[cache_key]
        data = []
        bytes = self.buffer.read_bytes(self.tile_byte_size, address)
        for b in bytes:
            data.append(((b & 0xF0) >> 4) | (palette << 4))
            data.append((b & 0x0F) | (palette << 4))
        if self.use_cache:
            self.cache[cache_key] = data
        return data
        
    def to_mask(self, pattern: list) -> list:
        return mask_from_bytes(pattern)

    def get_pattern_by_number(self, number: int, palette: int) -> list:
        return self.get_pattern(number * self.tile_byte_size, palette)



'''
Savestate loading functions
'''
def load_wrapper(filepath: str, format: str):
    if not format in FORMAT_FUNCTIONS:
        raise Exception(f'Unknown save state format {format}')
    func = FORMAT_FUNCTIONS[format]
    return func(filepath)

def load_gens_legacy_state(filepath: str) -> SaveState:
    with open(filepath, 'rb') as f:
        cram = read_block_and_validate(f, 0x0112, SaveState.CRAM_SIZE)
        vram = read_block_and_validate(f, 0x012478, SaveState.VRAM_SIZE)
        vsram = read_block_and_validate(f, 0x0192, SaveState.VSRAM_SIZE)
        vdp_regs = read_block_and_validate(f, 0xFA, VDPRegisters.SIZE)

    return SaveState(
        Buffer(cram),
        Buffer(vram),
        Buffer(vsram),
        VDPRegisters.read_vdp_registers(Buffer(vdp_regs))
    )

FORMAT_FUNCTIONS = {
    'gens_legacy': load_gens_legacy_state
}

FORMAT_NAMES = {
    'gens_legacy': 'Gens Legacy / KMOD'
}

NAMES_FORMAT = dict(reversed(item) for item in FORMAT_NAMES.items())

'''
Helper Functions
'''
def read_block_and_validate(handle: BinaryIO, offset: int, length: int) -> bytearray:
    handle.seek(offset)
    data = handle.read(length)
    if len(data) != length:
        raise Exception('Bytes read was not bytes requested')
    return data

def mask_from_bytes(data: Iterable) -> list:
    return [1 if b & 0x0F else 0 for b in data]