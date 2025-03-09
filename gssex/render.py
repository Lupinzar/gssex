from .state import SaveState, PatternData, HardwareSprite, Palette, SpriteTable, mask_from_bytes
from .static import Plane, Priority, ScrollMode, Endian
from .rawfile import RawFile
from PIL import Image, ImageDraw
from struct import Struct
from dataclasses import dataclass
from typing import Tuple
from enum import Enum

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
    
    def __init__(self, savestate: SaveState, enable_cache: bool = True):
        self.savestate: SaveState = savestate
        self.enable_cache: bool = enable_cache
        self.cache: dict[Plane, Map] = {}
        #if we're in 8x16 tile mode, addresses need to be doubled, so shift an extra bit
        self.address_shift = 5 if self.savestate.vdp_registers.tile_height == 8 else 6
    
    def get_map(self, plane: Plane, priorities: Priority = Priority.BOTH) -> Map:
        cache_key = f'{plane.value}_{priorities.value}'
        if self.enable_cache and cache_key in self.cache:
            return self.cache[cache_key]
        regs = self.savestate.vdp_registers
        if plane == Plane.WINDOW:
            cell_width, cell_height = regs.get_window_cell_size()
        else:
            cell_width = regs.scroll_width
            cell_height = regs.scroll_height
        map = Map(cell_width * 8, cell_height * regs.tile_height)
        entries = cell_width * cell_height
        base_address = self.get_base_address(plane)

        for ndx in range(0, entries):
            raw_bytes = self.savestate.v_ram_buffer.read_struct(
                self.DATA_STRUCT, 
                ndx * self.DATA_STRUCT.size + base_address)[0]
            td = self.decode_tile_data(raw_bytes)
            if not self.include_tile(td['priority'], priorities):
                continue
            pattern = self.savestate.pattern_data.get_pattern(td['address'], td['pal'])
            tile_x = ndx % cell_width
            tile_y = ndx // cell_width

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
            'address': (raw_bytes & 0x07FF) << self.address_shift,
            'priority': bool(raw_bytes & 0x8000),
            'vflip': bool(raw_bytes & 0x1000),
            'hflip': bool(raw_bytes & 0x0800)
        }
    
    def include_tile(self, priority: bool, priorities: Priority) -> bool:
        if priorities == Priority.BOTH:
            return True
        if priority and priorities & Priority.HIGH:
            return True
        if not priority and priorities & Priority.LOW:
            return True
        return False

class MapRender:
    """
    Does the actual rendering of Tile Maps either raw, or as they appear on screen
    """
    def __init__(self, savestate: SaveState):
        self.savestate = savestate
        self.mapper = Mapper(self.savestate, True)
        self.scroll_table: ScrollTable = ScrollTable(savestate)

    def render_map(self, plane: Plane, priority: Priority, bgcolor: int) -> Image.Image:
        map = self.mapper.get_map(plane, priority)
        img = Image.new('P', (map.width, map.height))
        img.putdata(map.get_bytes(bgcolor))
        return img
    
    def render_screen(self, plane: Plane, priority: Priority, bgcolor: int) -> Image.Image:
        if plane == Plane.WINDOW:
            return self.render_screen_window(priority, bgcolor)
        return self.render_screen_scroll(plane, priority, bgcolor)
    
    def render_screen_scroll(self, plane: Plane, priority: Priority, bgcolor: int) -> Image.Image:
        map = self.mapper.get_map(plane, priority)
        size = self.savestate.vdp_registers.get_screen_size()
        img = Image.new('P', size)
        map_bytes = map.get_bytes(bgcolor)
        data = bytearray()

        for pix in range(0, size[0] * size[1]):
            x = pix % size[0]
            y = pix // size[0]
            mx, my = self.scroll_table.translate(plane, x, y)
            address = mx + my * map.width
            data.append(map_bytes[address])
        img.putdata(data)
        return img
    
    def render_screen_window(self, priority: Priority, bgcolor: int) -> Image.Image:
        map = self.mapper.get_map(Plane.WINDOW, priority)
        vdp = self.savestate.vdp_registers
        size = self.savestate.vdp_registers.get_screen_size()
        width = vdp.window_split_h * 8
        height = vdp.window_split_v * vdp.tile_height
        img = Image.new('P', size, bgcolor)
        map_img = Image.new('P', (map.width, map.height))
        map_img.putdata(map.get_bytes(bgcolor))

        img.paste(map_img, (0, 0))

        no_draw = (0, 0, size[0], size[1])
        if vdp.window_down:
            if vdp.window_right:
                no_draw = (0, 0, width - 1, height - 1)
            else:
                no_draw = (width, 0, size[0] - 1, height - 1)
        elif not vdp.window_down:
            if vdp.window_right:
                no_draw = (0, height, width - 1, size[1] - 1)
            else:
                no_draw = (width, height, size[0] - 1, size[1] - 1)
        
        #nothing else to do
        if no_draw[2] < no_draw[0] or no_draw[3] < no_draw[1]:
            return img
        
        draw = ImageDraw.Draw(img)
        draw.rectangle(no_draw, fill=bgcolor)

        return img
    
    def render_scoll_marks(self, plane: Plane, thickness: int = 16) -> Image.Image:
        size = self.savestate.vdp_registers.get_screen_size()
        new_size = (size[0] + thickness, size[1] + thickness)
        img = Image.new('RGBA', new_size, (0,0,0,0))
        if plane == Plane.WINDOW:
            return img
        draw = ImageDraw.Draw(img)

        v_table = self.scroll_table.v_table[plane]
        h_table = self.scroll_table.h_table[plane]
        v_increments = size[0] // len(v_table)
        h_increments = size[1] // len(h_table)

        for ndx, offset in enumerate(v_table):
            x = ndx * v_increments + thickness
            draw.rectangle((x, 0, x+v_increments-1, thickness-1), fill=self.offset_to_color(offset))

        for ndx, offset in enumerate(h_table):
            y = ndx * h_increments + thickness
            draw.rectangle((0, y, thickness-1, y+h_increments-1), fill=self.offset_to_color(offset))

        return img
    
    def offset_to_color(self, offset: int) -> Tuple[int, int, int]:
        if offset < 0:
            r = 0xFF
            offset = abs(offset)
        else:
            r = 0
        g = (offset & 0xFF00) >> 8
        b = offset & 0x00FF
        return r, g, b
        
class ScrollTable:
    """
    Reads in the scroll tables for A/B planes and does scroll translations
    """
    H_DATA_STRUCT = Struct('>2h')
    def __init__(self, savestate: SaveState):
        self.savestate = savestate
        self.map_width = savestate.vdp_registers.scroll_width * 8
        self.map_height = savestate.vdp_registers.scroll_height * savestate.vdp_registers.tile_height
        self.h_mode = savestate.vdp_registers.scroll_mode_h
        self.v_mode = savestate.vdp_registers.scroll_mode_v
        self.layer_offset = 0
        self.address = savestate.vdp_registers.address_scroll_h
        self.v_table = {
            Plane.SCROLL_A: [],
            Plane.SCROLL_B: []
        }
        self.h_table = {
            Plane.SCROLL_A: [],
            Plane.SCROLL_B: []
        }
        self.h_index_callback: callable
        self.v_index_callback: callable
        self.load_table()
        self.set_callbacks()
        
    def load_table(self):
        v_total = 1 if self.v_mode == ScrollMode.FULL else (self.savestate.vdp_registers.cells_wide // 2)
        vsr_struct = Struct(self.get_vs_ram_format())
        for k in range(0, v_total):
            values = self.savestate.vs_ram_buffer.read_struct(vsr_struct, k * vsr_struct.size)
            self.v_table[Plane.SCROLL_A].append(values[0])
            self.v_table[Plane.SCROLL_B].append(values[1])
        
        multi = 1
        match self.h_mode:
            case ScrollMode.FULL:
                h_total = 1
            case ScrollMode.CELL:
                h_total = self.savestate.vdp_registers.cells_high
                #CELL mode stores its values in VRAM with gaps, we need to account for that
                multi = self.savestate.vdp_registers.tile_height
            case _:
                h_total = self.savestate.vdp_registers.cells_high * 8 #yes, a hard 8 even in double res mode
        for k in range(0, h_total):
            values = self.savestate.v_ram_buffer.read_struct(self.H_DATA_STRUCT, k * self.H_DATA_STRUCT.size * multi + self.address)
            self.h_table[Plane.SCROLL_A].append(values[0])
            self.h_table[Plane.SCROLL_B].append(values[1])

    def set_callbacks(self):
        if self.v_mode == ScrollMode.FULL:
            self.v_index_callback = self.get_index_full
        else:
            self.v_index_callback = self.get_index_column
        match self.h_mode:
            case ScrollMode.FULL:
                self.h_index_callback = self.get_index_full
            case ScrollMode.CELL:
                self.h_index_callback = self.get_index_cell
            case _:
                if self.savestate.vdp_registers.tile_height == 8:
                    self.h_index_callback = self.get_index_line
                else:
                    #double res mode
                    self.h_index_callback = self.get_index_line_double

    def get_index_full(self, index: int) -> int:
        return 0
    
    def get_index_column(self, index: int) -> int:
        return index // 16
    
    def get_index_cell(self, index: int) -> int:
        return index // self.savestate.vdp_registers.tile_height
    
    def get_index_line(self, index: int) -> int:
        return index
    
    def get_index_line_double(self, index: int) -> int:
        return index // 2
    
    '''
    TODO V Column + H Scroll
    This algo doesn't do Ver. Column scroll plus any Hor. Scroll correctly.
    Not sure if any commercial software uses such a combo, but I'm sure
    there are 1-2 corner cases to prove me wrong. I'll either come back
    to this later, or someone else can solve it. I'd need to spend more
    time reading emulator source code or doing tests and I'd rather get
    the tool released first. sin_counter++;
    '''
    def translate(self, plane: Plane, x: int, y: int) -> Tuple[int, int]:
        if plane == Plane.WINDOW:
            return x, y
        v_ndx = self.v_index_callback(x)
        h_ndx = self.h_index_callback(y)

        v_off = self.v_table[plane][v_ndx]
        h_off = self.h_table[plane][h_ndx] * -1

        #make negative offsets positive
        while v_off < 0:
            v_off += self.map_height
        while h_off < 0:
            h_off += self.map_width

        map_x = (x + h_off) % self.map_width
        map_y = (y + v_off) % self.map_height

        return map_x, map_y

    def get_vs_ram_format(self):
        return '>2h' if self.savestate.vs_ram_endian == Endian.BIG else '<2h'
    
class SpritePlane:
    """
    Renders hardware sprites in their position on the plane
    """
    class TRIM_MODE(Enum):
        NONE = 0
        SCREEN = 1
        SPRITES = 2
    PLANE_SIZE = 512
    DISPLAY_OFFSET = 128
    def __init__(self, savestate: SaveState, sprites: SpriteTable):
        self.savestate: SaveState = savestate
        self.sprites: SpriteTable = sprites

    def render(self, trim_mode: TRIM_MODE, pal: Palette, bgcolor: int, ignore: set = set(), margins: bool = False) -> Image.Image:
        pal_colors = pal.flattened_colors()
        if margins:
            img = Image.new("RGBA", (self.PLANE_SIZE, self.PLANE_SIZE), (0,0,0,0))
            self.setup_margins(img, pal.colors[bgcolor], ignore)
        else:
            img = Image.new("P", (self.PLANE_SIZE, self.PLANE_SIZE), bgcolor)
            img.putpalette(pal_colors)

        draw_list = self.sprites.get_draw_list()
        drawn = 0
        screen_w, screen_h = self.savestate.vdp_registers.get_screen_size()
        min_max_box = [self.PLANE_SIZE, self.PLANE_SIZE, 0, 0]
        for ndx in draw_list:
            if ndx in ignore:
                continue
            sprite = self.sprites.sprites[ndx]
            spr_obj = SpriteImage(self.savestate.pattern_data, sprite)
            spr_img = spr_obj.get_image()
            spr_img.putpalette(pal_colors)
            img.paste(spr_img, (sprite.x, sprite.y), spr_obj.get_mask())
            spr_img.close()
            if trim_mode == self.TRIM_MODE.SPRITES:
                self.adjust_box(min_max_box, sprite)
            drawn += 1

        if trim_mode == self.TRIM_MODE.NONE or drawn == 0:
            return img
        if trim_mode == self.TRIM_MODE.SPRITES:
            return img.crop(min_max_box)
        return img.crop((
            self.DISPLAY_OFFSET, 
            self.DISPLAY_OFFSET, 
            self.DISPLAY_OFFSET + screen_w,
            self.DISPLAY_OFFSET + screen_h
        ))

    def setup_margins(self, image: Image.Image, color: Tuple[int, int, int], ignore: set):
        draw_list = self.sprites.get_draw_list()
        draw = ImageDraw.Draw(image)
        tile_width = 8
        tile_height = self.savestate.vdp_registers.tile_height
        for ndx in draw_list:
            if ndx in ignore:
                continue
            sprite = self.sprites.sprites[ndx]
            x = sprite.x
            y = sprite.y
            x1 = sprite.x + sprite.width * tile_width - 1
            y1 = sprite.y + sprite.height * tile_height - 1
            draw.rectangle((x, y, x1, y1), fill=color)

    def adjust_box(self, box: list[int], sprite: HardwareSprite):
        x2 = sprite.x + sprite.width * 8
        y2 = sprite.y + sprite.height * self.savestate.vdp_registers.tile_height
        if sprite.x < box[0]:
            box[0] = sprite.x
        if x2 > box[2]:
            box[2] = x2
        if sprite.y < box[1]:
            box[1] = sprite.y
        if y2 > box[3]:
            box[3] = y2
        
'''
Helper functions
'''

def tile_image_and_mask(pattern: bytearray, size: Tuple[int, int]) -> Tuple[Image.Image, Image.Image]:
    image = Image.new('P', size)
    image.putdata(pattern)
    mask = Image.new('1', size)
    mask.putdata(mask_from_bytes(pattern))
    return (image, mask)