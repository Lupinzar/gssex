from .state import SaveState, PatternData, HardwareSprite, Palette, mask_from_bytes
from .static import Plane
from .rawfile import RawFile
from PIL import Image, ImageDraw
from struct import Struct
from dataclasses import dataclass
from typing import Tuple
import enum

class SpriteImage:
    def __init__(self, patterns: PatternData, sprite: HardwareSprite):
        self.sprite = sprite
        self.patterns = patterns
        self.rendered = False
        self.enable_flips = True
        self.image: Image.Image
        self.mask: Image.Image

    def render(self):
        pixel_width = self.patterns.tile_width * self.sprite.width
        pixel_height = self.patterns.tile_height * self.sprite.height
        pattern_count = self.sprite.width * self.sprite.height
        self.image = Image.new('P', (pixel_width, pixel_height))
        self.mask = Image.new('1', (pixel_width, pixel_height))

        #render image
        for tile_num in range(0, pattern_count):
            x = (tile_num // self.sprite.height) * self.patterns.tile_width
            y = (tile_num % self.sprite.height) * self.patterns.tile_height

            tile_data = self.patterns.get_pattern_by_number(
                self.sprite.start + tile_num, 
                self.sprite.pal)
            tile = Image.new('P', (self.patterns.tile_width, self.patterns.tile_height))
            tile.putdata(tile_data)
            self.image.paste(tile, (x, y))
            tile.close()

        #flips
        if self.enable_flips and self.sprite.hflip:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        if self.enable_flips and self.sprite.vflip:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

        #create mask
        self.mask.putdata(mask_from_bytes(self.image.getdata()))
        self.rendered = True
    
    def get_image(self) -> Image.Image:
        if not self.rendered:
            self.render()
        return self.image

    def get_mask(self) -> Image.Image:
        if not self.rendered:
            self.render()
        return self.mask
    
class PaletteImage():
    def __init__(self, palette: Palette, swatch_size=16):
        self.palette = palette
        self.swatch_size = 16

    def get_image(self) -> Image.Image:
        image = Image.new('P', (Palette.SIZE * self.swatch_size, Palette.GROUP_SIZE * self.swatch_size))
        draw = ImageDraw.Draw(image)
        for k in range(0, Palette.SIZE * Palette.GROUP_SIZE):
            x = k % Palette.SIZE
            y = k // Palette.SIZE
            draw.rectangle(
                ((
                    x * self.swatch_size,
                    y * self.swatch_size
                ),(
                    x * self.swatch_size + self.swatch_size - 1,
                    y * self.swatch_size + self.swatch_size - 1
                )),
                k
            )
        image.putpalette(self.palette.flattened_colors())
        return image

@dataclass
class VramRender():
    patterns: PatternData
    palette: int = 0
    bgcolor: int = 0
    tiles_wide: int = 16
    pivot: bool = False  #rwar

    def get_image(self) -> Image.Image:
        size_in_tiles = self.get_size_in_tiles()
        size_in_px = (
            size_in_tiles[0] * self.patterns.tile_width,
            size_in_tiles[1] * self.patterns.tile_height
        )
        image = Image.new('P', size_in_px, self.bgcolor)
        for tc in range(0, self.patterns.get_tile_count()):
            pos = (tc % self.tiles_wide, tc // self.tiles_wide)
            if self.pivot:
                pos = (pos[1], pos[0])
            image_data = tile_image_and_mask(self.patterns.get_pattern_by_number(tc, self.palette), self.patterns.tile_size)
            image.paste(image_data[0], (pos[0] * self.patterns.tile_width, pos[1] * self.patterns.tile_height), mask=image_data[1])
            for img in image_data:
                img.close()
        return image

    def get_size_in_tiles(self) -> Tuple[int, int]:
        tile_count = self.patterns.get_tile_count()
        size = (
            self.tiles_wide,
            (tile_count // self.tiles_wide) + bool(tile_count % self.tiles_wide)
        )
        if self.pivot:
            size = (size[1], size[0])
        return size
    
class RawRender:
    def __init__(self, file: RawFile):
        self.file: RawFile = file
        self.tiles_drawn: int = 0

    def get_image(self, offset: int, tiles_wide: int, tiles_tall: int, palette: int, bgcolor: int = 0, tile_height: int = 8, pivot: bool = False) -> Image.Image:
        self.tiles_drawn = 0
        tile_width = 8
        tile_bytes = tile_width * tile_height // 2
        data_to_read = tile_bytes * tiles_wide * tiles_tall

        #adjust tiles to read if we need to
        if offset + data_to_read >= self.file.size:
            data_to_read = self.file.size - offset
            tile_count = data_to_read // tile_bytes
        else:
            tile_count = tiles_wide * tiles_tall
        tile_size = (tiles_wide, tiles_tall)

        image = Image.new('P', (tile_width * tile_size[0], tile_height * tile_size[1]), bgcolor)
        self.file.mmap.seek(offset)
        for ndx in range(0, tile_count):
            if pivot:
                pos = (ndx // tiles_tall, ndx % tiles_tall)
            else:
                pos = (ndx % tiles_wide, ndx // tiles_wide)
            image_data = tile_image_and_mask(self.expand_tile(self.file.mmap.read(tile_bytes), palette), (tile_width, tile_height))
            image.paste(image_data[0], (pos[0] * tile_width, pos[1] * tile_height), mask=image_data[1])
            for img in image_data:
                img.close()
            self.tiles_drawn += 1
        return image
    
    def expand_tile(self, bytes: bytearray, palette: int) -> bytearray:
        data = bytearray()
        for b in bytes:
            data.append(((b & 0xF0) >> 4) | (palette << 4))
            data.append((b & 0x0F) | (palette << 4))
        return data
    
    def get_tiles_drawn(self) -> int:
        return self.tiles_drawn
    
class Map:
    """
    Represents a tilemap as indexed pixel values
    """
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.bytes: bytearray = bytearray(width * height)

    def __len__(self) -> int:
        return len(self.bytes)
    
    def get_bytes(self, bg_replace: None|int = None):
        if bg_replace is None:
            return self.bytes
        return bytearray([b if b & 0x0F else bg_replace for b in self.bytes])

class Mapper:
    """
    Generates Map objects from a SaveState
    """
    DATA_STRUCT = Struct('>H')
    class PRIORITY(enum.Flag):
        LOW = 0x1
        HIGH = 0x2
        BOTH = 0x3
    def __init__(self, savestate: SaveState, enable_cache: bool = True):
        self.savestate: SaveState = savestate
        self.enable_cache: bool = enable_cache
        self.cache: dict[Plane, Map] = {}
    
    def get_map(self, plane: Plane, priorities: PRIORITY = PRIORITY.BOTH) -> Map:
        cache_key = f'{plane.value}_{priorities.value}'
        if self.enable_cache and cache_key in self.cache:
            return self.cache[cache_key]
        regs = self.savestate.vdp_registers
        #TODO Window testing/handling
        map = Map(regs.scroll_width * 8, regs.scroll_height * regs.tile_height)
        entries = regs.scroll_width * regs.scroll_height
        base_address = self.get_base_address(plane)

        for ndx in range(0, entries):
            raw_bytes = self.savestate.v_ram_buffer.read_struct(
                self.DATA_STRUCT, 
                ndx * self.DATA_STRUCT.size + base_address)[0]
            td = self.decode_tile_data(raw_bytes)
            if not self.include_tile(td['priority'], priorities):
                continue
            pattern = self.savestate.pattern_data.get_pattern(td['address'], td['pal'])
            tile_x = ndx % regs.scroll_width
            tile_y = ndx // regs.scroll_width

            for pndx, pixel in enumerate(pattern):
                px = pndx % 8
                py = pndx // 8
                if td['hflip']:
                    px = 7 - px
                if td['vflip']:
                    py = regs.tile_height - 1 - py
                byte_address = tile_x * 8 + px + (tile_y * regs.tile_height * map.width + py * map.width)
                map.bytes[byte_address] = pixel

        if self.enable_cache:
            self.cache[cache_key] = map
        return map
    
    def get_base_address(self, plane: Plane):
        match plane:
            case Plane.SCROLL_A:
                return self.savestate.vdp_registers.address_scroll_a
            case Plane.SCROLL_B:
                return self.savestate.vdp_registers.address_scroll_b
            case _:
                return self.savestate.vdp_registers.address_window
            
    def decode_tile_data(self, raw_bytes: int) -> dict:
        return {
            'pal': (raw_bytes & 0x6000) >> 13,
            'address': (raw_bytes & 0x07FF) << 5,
            'priority': bool(raw_bytes & 0x8000),
            'vflip': bool(raw_bytes & 0x1000),
            'hflip': bool(raw_bytes & 0x0800)
        }
    
    def include_tile(self, priority: bool, priorities: PRIORITY) -> bool:
        if priorities == self.PRIORITY.BOTH:
            return True
        if priority and priorities & self.PRIORITY.HIGH:
            return True
        if not priority and priorities & self.PRIORITY.LOW:
            return True
        return False
        
    
'''
Helper functions
'''

def tile_image_and_mask(pattern: bytearray, size: Tuple[int, int]) -> Tuple[Image.Image, Image.Image]:
    image = Image.new('P', size)
    image.putdata(pattern)
    mask = Image.new('1', size)
    mask.putdata(mask_from_bytes(pattern))
    return (image, mask)