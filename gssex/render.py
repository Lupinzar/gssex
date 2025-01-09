from .state import PatternData, HardwareSprite, Palette, mask_from_bytes
from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import Tuple, BinaryIO

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
    def __init__(self, file_handle: BinaryIO, file_size: int):
        self.handle = file_handle
        self.file_size = file_size

    def get_image(self, offset: int, tiles_wide: int, tiles_tall: int, palette: int, bgcolor: int = 0, tile_height: int = 8, pivot: bool = False) -> Image.Image:
        tile_width = 8
        tile_bytes = tile_width * tile_height // 2
        data_to_read = tile_bytes * tiles_wide * tiles_tall

        #adjust tiles to read if we need to
        if offset + data_to_read >= self.file_size:
            data_to_read = self.file_size - offset
            tile_count = data_to_read // tile_bytes
        else:
            tile_count = tiles_wide * tiles_tall
        tile_size = (tiles_wide, tiles_tall)

        image = Image.new('P', (tile_width * tile_size[0], tile_height * tile_size[1]), bgcolor)
        self.handle.seek(offset)
        for ndx in range(0, tile_count):
            if pivot:
                pos = (ndx // tiles_tall, ndx % tiles_tall)
            else:
                pos = (ndx % tiles_wide, ndx // tiles_wide)
            image_data = tile_image_and_mask(self.expand_tile(self.handle.read(tile_bytes), palette), (tile_width, tile_height))
            image.paste(image_data[0], (pos[0] * tile_width, pos[1] * tile_height), mask=image_data[1])
            for img in image_data:
                img.close()
        return image
    
    def expand_tile(self, bytes: bytearray, palette: int) -> bytearray:
        data = bytearray()
        for b in bytes:
            data.append(((b & 0xF0) >> 4) | (palette << 4))
            data.append((b & 0x0F) | (palette << 4))
        return data


    
'''
Helper functions
'''

def tile_image_and_mask(pattern: bytearray, size: Tuple[int, int]) -> Tuple[Image.Image, Image.Image]:
    image = Image.new('P', size)
    image.putdata(pattern)
    mask = Image.new('1', size)
    mask.putdata(mask_from_bytes(pattern))
    return (image, mask)