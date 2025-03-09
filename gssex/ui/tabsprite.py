from .rendertab import RenderTab
from .tabraw import TabRaw
from .spritemodel import SpriteModel
from .app import pil_to_qimage, pil_to_clipboard
from ..uibase.tabsprite import Ui_TabSprite
from ..state import SpriteTable
from ..render import SpriteImage, SpritePlane
from PySide6.QtGui import QStandardItemModel, QPixmap, QShortcut, QKeySequence
from PIL import Image
from base64 import b32encode

class TabSprite(RenderTab, Ui_TabSprite):
    NO_SPRITE_SELECTED_MSG = "No sprite currently selected"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.sprite_table: SpriteTable
        self.sprite_view.setSelectionBehavior(self.sprite_view.SelectionBehavior.SelectRows)
        self.sprite_view.setSelectionMode(self.sprite_view.SelectionMode.SingleSelection)
        self.current_sprite: int|None
        self.hidden_sprites: set = set()

        self.clear_view()
        self.load_trim_combo()
        self.fullRefresh.connect(self.full_refresh)
        self.saveStateChanged.connect(self.state_changed)
        self.paletteSwapped.connect(self.redraw)
        self.tile_margins_check.checkStateChanged.connect(self.render_plane)
        self.trim_combo.currentIndexChanged.connect(self.render_plane)
        self.save_sprite_button.clicked.connect(self.save_sprite)
        self.copy_sprite_button.clicked.connect(self.copy_sprite_to_clipboard)
        self.save_plane_button.clicked.connect(self.save_plane)
        self.copy_plane_button.clicked.connect(self.copy_plane_to_clipboard)
        self.find_button.clicked.connect(self.find_in_raw)
        self.register_shortcuts()

    def link_raw_tab(self, tab: TabRaw):
        self.raw_tab = tab

    def load_trim_combo(self):
        for ndx in range(0, len(SpritePlane.TRIM_MODE)):
            enum = SpritePlane.TRIM_MODE(ndx)
            self.trim_combo.addItem(enum.name.title())

    def find_in_raw_allowed(self) -> bool:
        if self.raw_tab.file is None:
            return False
        if not self.app.valid_file:
            return False
        if self.current_sprite is None:
            return False
        return True
    
    def update_find_button(self):
        self.find_button.setEnabled(self.find_in_raw_allowed())

    def register_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+S"), self, lambda: self.save_sprite())
        QShortcut(QKeySequence("Ctrl+C"), self, lambda: self.copy_sprite_to_clipboard())
        QShortcut(QKeySequence("Shift+Ctrl+S"), self, lambda: self.save_plane())
        QShortcut(QKeySequence("Shift+Ctrl+C"), self, lambda: self.copy_plane_to_clipboard())

    def resize_headers(self):
        head = self.sprite_view.horizontalHeader()
        for ndx, column in enumerate(SpriteModel.COLUMNS):
            head.setSectionResizeMode(ndx, column.resize_mode)

    def clear_view(self):
        self.current_sprite = None
        self.sprite_view.setModel(QStandardItemModel())
        self.sprite_label.clear()
        self.plane_label.clear()

    def handle_selection(self):
        if not self.app.valid_file:
            return
        selection = self.sprite_view.selectedIndexes()
        if not len(selection):
            self.sprite_label.clear()
            self.current_sprite = None
            self.update_find_button()
            return
        self.current_sprite = selection[0].row()
        self.render_sprite()
        self.update_find_button()

    def redraw(self):
        if not self.app.valid_file:
            self.clear_view()
            self.update_find_button()
            return
        self.render_sprite()
        self.render_plane()
        self.update_find_button()

    def full_refresh(self):
        if not self.app.valid_file:
            self.update_find_button()
            self.clear_view()
            return
        self.load_model()
        self.resize_headers()
        self.redraw()

    def state_changed(self):
        self.hidden_sprites = set()
        self.full_refresh()

    def load_model(self):
        if not self.app.valid_file:
            self.clear_view()
            return
        self.sprite_table = SpriteTable(self.app.savestate)
        self.sprite_model = SpriteModel(self.sprite_table, self.hidden_sprites)
        self.sprite_view.setModel(self.sprite_model)
        self.sprite_view.selectionModel().selectionChanged.connect(self.handle_selection)
        self.sprite_model.dataChanged.connect(self.render_plane)
        self.resize_headers()
        if self.current_sprite is not None:
            self.sprite_view.selectRow(self.current_sprite)

    def render_sprite(self):
        if self.current_sprite is None:
            return
        img = self.get_pil_sprite()
        qimg = pil_to_qimage(img)
        self.sprite_label.setPixmap(QPixmap.fromImage(qimg))
        img.close()

    def render_plane(self):
        if not self.app.valid_file:
            return
        img = self.get_pil_plane()
        qimg = pil_to_qimage(img)
        self.plane_label.setFixedSize(img.width, img.height)
        self.scrollAreaWidgetContents.setFixedSize(img.width, img.height)
        self.plane_label.setPixmap(QPixmap.fromImage(qimg))
        img.close()

    def get_pil_sprite(self) -> Image.Image:
        render = SpriteImage(self.app.savestate.pattern_data, self.sprite_table[self.current_sprite])
        sprite_img = render.get_image()
        mask_img = render.get_mask()
        bg, pal = self.app.get_palette_and_background()
        img = Image.new('P',(sprite_img.width, sprite_img.height), bg)
        img.paste(sprite_img, (0,0), mask_img)
        img.putpalette(pal.flattened_colors())
        return img
    
    def get_pil_plane(self) -> Image.Image:
        render = SpritePlane(self.app.savestate, self.sprite_table)
        bg, pal = self.app.get_palette_and_background()
        img = render.render(
            SpritePlane.TRIM_MODE(self.trim_combo.currentIndex()),
            pal,
            bg,
            self.hidden_sprites,
            self.tile_margins_check.isChecked()
        )
        return img
    
    def save_sprite(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        if self.current_sprite is None:
            self.statusMessage.emit(self.NO_SPRITE_SELECTED_MSG)
            return
        img = self.get_pil_sprite()
        parts = [
            'hwsprite',
            f'{self.current_sprite:02d}',
            'global' if self.app.use_global_pal else 'state'
        ]
        path = self.app.build_image_output_path("_".join(parts))
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")
        img.close()

    def copy_sprite_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        if self.current_sprite is None:
            self.statusMessage.emit(self.NO_SPRITE_SELECTED_MSG)
            return
        img = self.get_pil_sprite()
        pil_to_clipboard(img)
        img.close()

    def save_plane(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        img = self.get_pil_plane()
        parts = [
            'sprite-plane',
            self.get_drawn_string(),
            SpritePlane.TRIM_MODE(self.trim_combo.currentIndex()).name.lower(),
            'global' if self.app.use_global_pal else 'state'
        ]
        if self.tile_margins_check.isChecked():
            parts.append("margins")
        path = self.app.build_image_output_path("_".join(parts))
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")
        img.close()

    def copy_plane_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        img = self.get_pil_plane()
        pil_to_clipboard(img)
        img.close()

    def find_in_raw(self):
        if self.current_sprite is None:
            return
        bytedata = bytearray()
        sprite = self.sprite_table[self.current_sprite]
        tile_start = sprite.start
        tile_end = sprite.width * sprite.height + tile_start
        for tilenum in range(tile_start, tile_end):
            offset = self.app.savestate.pattern_data.number_to_offset(tilenum)
            bytedata += self.app.savestate.pattern_data.get_raw(offset)
        tabs = self.parent().parent()
        tabs.setCurrentWidget(self.raw_tab)
        self.raw_tab.data_search(bytedata)

    def get_drawn_string(self) -> str:
        if not len(self.hidden_sprites):
            return 'all-sprites'
        drawn = [n for n in self.sprite_table.get_draw_list() if n not in self.hidden_sprites]
        if not len(drawn):
            return 'no-sprites'
        set_bits = bytearray(10) #80 sprites fits in 10 bytes
        largest = 0
        for ndx in drawn:
            bnum = len(set_bits) - 1 - (ndx // 8)
            bit = ndx % 8
            set_bits[bnum] |= 1 << bit
            if bnum > largest:
                largest = bnum
        return b32encode(set_bits).decode('ascii')
