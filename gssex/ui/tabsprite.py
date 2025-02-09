from .rendertab import RenderTab
from .spritemodel import SpriteModel
from .app import pil_to_qimage, pil_to_clipboard
from ..uibase.tabsprite import Ui_TabSprite
from ..state import SpriteTable
from ..render import SpriteImage, SpritePlane
from PySide6.QtCore import Qt, QModelIndex, QItemSelection
from PySide6.QtGui import QStandardItemModel, QPixmap
from PIL import Image

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
        self.save_sprite_button.clicked.connect(self.save_sprite)
        self.copy_sprite_button.clicked.connect(self.copy_sprite_to_clipboard)

    def load_trim_combo(self):
        for ndx in range(0, len(SpritePlane.TRIM_MODE)):
            enum = SpritePlane.TRIM_MODE(ndx)
            self.trim_combo.addItem(enum.name.title())

    def resize_headers(self):
        head = self.sprite_view.horizontalHeader()
        for ndx, column in enumerate(SpriteModel.COLUMNS):
            head.setSectionResizeMode(ndx, column.resize_mode)

    def clear_view(self):
        self.current_sprite = None
        self.sprite_view.setModel(QStandardItemModel())
        self.sprite_label.clear()
        self.plane_label.clear()

    def handle_table_click(self, index: QModelIndex):
        if not self.app.valid_file:
            return
        self.render_sprite(index.row())

    def handle_selection(self):
        if not self.app.valid_file:
            return
        selection = self.sprite_view.selectedIndexes()
        if not len(selection):
            self.sprite_label.clear()
            self.current_sprite = None
            return
        self.current_sprite = selection[0].row()
        self.render_sprite()

    def redraw(self):
        if not self.app.valid_file:
            self.clear_view()
            return
        self.render_sprite()
        self.render_plane()

    def full_refresh(self):
        if not self.app.valid_file:
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
        self.resize_headers()

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

    def get_pil_sprite(self):
        render = SpriteImage(self.app.savestate.pattern_data, self.sprite_table[self.current_sprite])
        sprite_img = render.get_image()
        mask_img = render.get_mask()
        bg, pal = self.app.get_palette_and_background()
        img = Image.new('P',(sprite_img.width, sprite_img.height), bg)
        img.paste(sprite_img, (0,0), mask_img)
        img.putpalette(pal.flattened_colors())
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
