from gssex.state import ScrollMode, PatternData, Palette, SpriteTable, load_gens_legacy_state
from gssex.render import SpriteImage, PaletteImage, VramRender, RawRender, MapRender, SpritePlane, mask_from_bytes
from gssex.rawfile import RawFile
from gssex.static import Plane, Priority
from PIL import Image
from pprint import pp
from os import fstat


state = load_gens_legacy_state("testsaves/kidscroll.gs0")

#pp(state.vdp_registers)

st = SpriteTable(state)

#pp(st.sprites[0])

pal = Palette.from_cram(state.c_ram_buffer)
#pal = Palette.make_unique()

pi = PaletteImage(pal)
pi.get_image().save("testoutput/palrender.png")

pat = state.pattern_data
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

vr = VramRender(pat, 0, 0, pivot=True)
vr_img = vr.get_image()
vr_img.putpalette(pal.flattened_colors())
vr_img.save('testoutput/vram.png')

subpat = pat.get_subset(pat.number_to_offset(561), 4)
vrs = VramRender(subpat, 0, 0, 2, pivot=True)
vrs_img = vrs.get_image()
vrs_img.putpalette(pal.flattened_colors())
vrs_img.save('testoutput/vram_sub.png')

#should produce the same output as VramRender
rawfile = RawFile('testsaves/kidscroll.gs0')
rr = RawRender(rawfile)
rr_img = rr.get_image(0x012478, 16, 128, 0, 0, pivot=True)
rr_img.putpalette(pal.flattened_colors())
rr_img.save('testoutput/raw.png')

'''
mapper = Mapper(state)
map = mapper.get_map(Plane.SCROLL_B, Mapper.PRIORITY.BOTH)
map_img = Image.new('P', (map.width, map.height))
map_img.putdata(map.get_bytes(0))
map_img.putpalette(pal.flattened_colors())
map_img.save('testoutput/mapper_test.png')
'''

map_save_path = "testsaves/langrisser_portrait.gs0"
#map_save_path = "testsaves/kidscroll.gs0"
#map_save_path = "testsaves/juju_vscrollb.gs0"
#map_save_path = "testsaves/valis3_slider.gs1"
map_state = load_gens_legacy_state(map_save_path)
map_pal = Palette.from_cram(map_state.c_ram_buffer)
map_pal.colors.append((255, 0, 255))
mapper = MapRender(map_state)
map_img = mapper.render_map(Plane.SCROLL_B, Priority.BOTH, 0)
map_img.putpalette(map_pal.flattened_colors())
map_img.save('testoutput/mapper_map_test.png')

map_scr_img = mapper.render_screen(Plane.SCROLL_B, Priority.BOTH, 0)
map_scr_img.putpalette(map_pal.flattened_colors())
map_scr_img.save('testoutput/mapper_screen_test.png')

map_wm_img = mapper.render_map(Plane.WINDOW, Priority.BOTH, 0)
map_wm_img.putpalette(map_pal.flattened_colors())
map_wm_img.save('testoutput/mapper_window_map_test.png')

map_win_img = mapper.render_screen(Plane.WINDOW, Priority.BOTH, 64)
map_win_img.putpalette(map_pal.flattened_colors())
map_win_img.save('testoutput/mapper_window_test.png')

map_mark_img = mapper.render_scoll_marks(Plane.SCROLL_B, 16)
map_mark_img.save('testoutput/mapper_mark_test.png')

spr_state = load_gens_legacy_state("testsaves/outrun2019.gs0")
spr_pal = Palette.from_cram(spr_state.c_ram_buffer)
spr_pal.colors.append((255, 0, 255))
spr_r = SpritePlane(spr_state, SpriteTable(spr_state))
spr_img = spr_r.render(SpritePlane.TRIM_MODE.NONE, spr_pal, 64, margins=False)
spr_img.save('testoutput/sprite_plane_test.png')
