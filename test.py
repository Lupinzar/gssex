from gssex.state import ScrollMode, PatternData, Palette, SpriteTable, load_gens_legacy_state
from gssex.render import SpriteImage, PaletteImage
from PIL import Image
from pprint import pp


state = load_gens_legacy_state("testsaves/kidscroll.gs0")

#pp(state.vdp_registers)

st = SpriteTable(state)

#pp(st.sprites[0])

pal = Palette.from_cram(state.c_ram_buffer)
#pal = Palette.make_unique()

pi = PaletteImage(pal)
pi.get_image().save("testoutput/palrender.png")

pat = PatternData(state.v_ram_buffer, use_cache=False)
pattern = pat.get_pattern_by_number(561,0)
#pattern = pat.get_pattern_by_number(561,1)

patimg = Image.new('P',(8,8))
patimg.putdata(pattern)
patimg.putpalette(pal.flattened_colors())

patimg.save('testoutput/patterntest.png')

patmask = Image.new('1', (8, 8))
patmask.putdata(pat.to_mask(pattern))
patmask.save('testoutput/patternmask.png')

final = Image.new('P', (8, 8), 64)
final.putpalette(pal.flattened_colors() + [0xFF,0x00,0xFF])
final.paste(patimg, patmask)
final.save('testoutput/patternfinal.png')

si = SpriteImage(pat, st.sprites[0])
sprite = si.get_image()
sprite.putpalette(pal.flattened_colors())
sprite.save('testoutput/spritetest.png')
si.get_mask().save('testoutput/spritemask.png')