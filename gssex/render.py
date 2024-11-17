from .state import PatternData, HardwareSprite, Palette, mask_from_bytes
from PIL import Image, ImageDraw

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
