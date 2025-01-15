from .rendertab import RenderTab
from .tabraw import TabRaw
from .tileloupe import TileLoupe
from ..uibase.tabvram import Ui_TabVram
from ..render import VramRender
from .app import pil_to_qimage, pil_to_clipboard
from PIL import Image
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent
from PySide6.QtCore import Qt, QEvent
from enum import Enum

class TabVram(RenderTab, Ui_TabVram):
    TILES_WIDE = 16
    NO_LOUPE_SELECTED_MSG = 'No tile selected in loupe'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.clear_main_image()
        self.saveStateChanged.connect(self.state_changed)
        self.fullRefresh.connect(self.full_refresh)
        self.paletteSwapped.connect(self.redraw)
        self.zoom_combo.currentIndexChanged.connect(self.redraw)
        self.pal_combo.currentIndexChanged.connect(self.redraw)
        self.pivot_button.clicked.connect(self.redraw)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.save_button.clicked.connect(self.save_image)
        self.find_button.clicked.connect(self.find_in_raw)
        self.tile_loupe.sizeChanged.connect(self.draw_loupe)
        self.tile_loupe.copyInitiated.connect(self.loupe_copy_to_clipboard)
        self.tile_loupe.saveInitiated.connect(self.loupe_save_image)
        self.tile_loupe.positionInitiated.connect(self.handle_loupe_position)
        self.main_label.installEventFilter(self)
    
    def link_raw_tab(self, tab: TabRaw):
        self.raw_tab = tab

    def eventFilter(self, obj, event):
        if obj == self.main_label and event.type() == QEvent.Type.MouseButtonRelease:
            self.handle_main_label_click(event)
        return super().eventFilter(obj, event)

    def state_changed(self):
        self.tile_loupe.reset()
        self.update_find_button()
        self.redraw()

    def clear_main_image(self):
        self.main_label.clear()
        self.main_label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.loupe_position_label.clear()

    def full_refresh(self):
        self.update_find_button()
        self.redraw()

    def find_in_raw_allowed(self) -> bool:
        if self.raw_tab.file is None:
            return False
        if not self.app.valid_file:
            return False
        if self.tile_loupe.reference is None:
            return False
        return True
    
    def update_find_button(self):
        self.find_button.setEnabled(self.find_in_raw_allowed())

    def redraw(self):
        if not self.app.valid_file:
            self.clear_main_image()
            return
        pilimg = self.get_pil_image()
        qimg = pil_to_qimage(pilimg)
        zoom = int(self.zoom_combo.currentText())
        width = pilimg.width * zoom
        height = pilimg.height * zoom
        self.main_label.setFixedSize(width, height)
        self.scrollAreaWidgetContents.setFixedSize(width, height)
        self.main_label.setPixmap(QPixmap.fromImage(qimg).scaled(
            width, 
            height, 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation)
        )
        self.main_label.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        pilimg.close()
        self.draw_loupe()

    def draw_loupe(self):
        self.update_find_button()
        if self.tile_loupe.reference is None or not self.app.valid_file:
            return
        img = self.get_pil_loupe()
        self.tile_loupe.set_image(QPixmap.fromImage(pil_to_qimage(img)), img.width, img.height)
        img.close()
        self.update_loupe_position()

    def handle_main_label_click(self, event: QMouseEvent):
        if not self.app.valid_file:
            return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        zoom = int(self.zoom_combo.currentText())
        tw = self.app.savestate.pattern_data.tile_width
        th = self.app.savestate.pattern_data.tile_height
        x = event.x() // zoom
        y = event.y() // zoom
        if self.pivot_button.isChecked():
            tile_num = (x // tw) * self.TILES_WIDE + (y // th)
        else:
            tile_num = (y // th) * self.TILES_WIDE + (x // tw)
        self.tile_loupe.reference = tile_num
        self.draw_loupe()
    
    def handle_loupe_position(self, direction: Enum, size: Enum):
        if not self.app.valid_file:
            return
        #if they haven't chosen a tile yet, just start at 0
        start = 0 if self.tile_loupe.reference is None else self.tile_loupe.reference
        amount = 1 if size == TileLoupe.POSITION_SIZE.SINGLE else self.tile_loupe.get_tile_area()
        if direction == TileLoupe.POSITION_DIRECTION.DECREMENT:
            amount = -amount
        new = start + amount
        if new < 0 or new >= self.app.savestate.pattern_data.get_tile_count():
            return
        self.tile_loupe.reference = new
        self.draw_loupe()

    def update_loupe_position(self):
        tile_from = self.tile_loupe.reference
        tile_to = self.tile_loupe.reference + self.tile_loupe.tiles_drawn - 1
        self.loupe_position_label.setText(f'#{tile_from} - #{tile_to}')

    def find_in_raw(self):
        bytedata = bytearray()
        tile_start = self.tile_loupe.reference
        tile_end = self.tile_loupe.tiles_drawn + tile_start
        for tilenum in range(tile_start, tile_end):
            offset = self.app.savestate.pattern_data.number_to_offset(tilenum)
            bytedata += self.app.savestate.pattern_data.get_raw(offset)
        tabs = self.parent().parent()
        tabs.setCurrentWidget(self.raw_tab)
        self.raw_tab.data_search(bytedata)

    def copy_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        img = self.get_pil_image()
        pil_to_clipboard(img)
        img.close()

    def save_image(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        img = self.get_pil_image()
        pal_type = 'global' if self.app.use_global_pal else 'local'
        pivot = '_pivot' if self.pivot_button.isChecked() else ''
        path = self.app.build_image_output_path(f'vram_{pal_type}_{self.pal_combo.currentText()}{pivot}')
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")

    def loupe_copy_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        if self.tile_loupe.reference is None:
            self.statusMessage.emit(self.NO_LOUPE_SELECTED_MSG)
            return
        img = self.get_pil_loupe()
        pil_to_clipboard(img)
        img.close()

    def loupe_save_image(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        if self.tile_loupe.reference is None:
            self.statusMessage.emit(self.NO_LOUPE_SELECTED_MSG)
            return
        img = self.get_pil_loupe()
        name_parts = [
            'vram',
            'loupe',
            'global' if self.app.use_global_pal else 'local',
            self.pal_combo.currentText(),
            str(self.tile_loupe.get_width()),
            str(self.tile_loupe.get_height()),
            str(self.tile_loupe.reference)
        ]
        if self.pivot_button.isChecked():
            name_parts.append('pivot')
        path = self.app.build_image_output_path("_".join(name_parts))
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")

    def get_pil_image(self) -> Image.Image:
        pal_data = self.app.get_palette_and_background()
        render = VramRender(self.app.savestate.pattern_data, self.pal_combo.currentIndex(), pal_data[0], self.TILES_WIDE, self.pivot_button.isChecked())
        img = render.get_image()
        img.putpalette(pal_data[1].flattened_colors())
        return img
    
    def get_pil_loupe(self) -> Image.Image:
        subpatterns = self.app.savestate.pattern_data.get_subset(
            self.app.savestate.pattern_data.number_to_offset(self.tile_loupe.reference),
            self.tile_loupe.get_tile_area()
        )
        tiles_to_draw = subpatterns.get_tile_count()
        self.tile_loupe.tiles_drawn = tiles_to_draw
        pal_data = self.app.get_palette_and_background()
        tile_width = self.tile_loupe.get_height() if self.pivot_button.isChecked() else self.tile_loupe.get_width()
        render = VramRender(
            subpatterns, 
            self.pal_combo.currentIndex(), 
            pal_data[0], 
            min(tiles_to_draw, tile_width),  #e.g. if tile area is 1x2 but we only have 1 tile left to draw
            self.pivot_button.isChecked()
        )
        img = render.get_image()
        img.putpalette(pal_data[1].flattened_colors())
        return img
