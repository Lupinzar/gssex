from .rendertab import RenderTab
from .tileloupe import TileLoupe
from ..uibase.tabraw import Ui_TabRaw
from ..render import RawRender
from .app import pil_to_qimage, pil_to_clipboard
from typing import BinaryIO
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QRegularExpressionValidator, QShortcut, QKeySequence
from PySide6.QtWidgets import QFileDialog
from os.path import isfile, dirname, basename
from os import fstat
from PIL import Image
from enum import Enum, auto

class TabRaw(RenderTab, Ui_TabRaw):
    class POSITION_DIRECTION(Enum):
        INCREMENT = auto()
        DECREMENT = auto()
    class POSITION_SIZE(Enum):
        SINGLE = auto()
        TILE = auto()
        LINE = auto()
        WINDOW = auto()
    DEFAULT_SPIN_WIDTH = 16
    DEFAULT_SPIN_HEIGHT = 16
    OFFSET_PROCESS_DELAY = 500
    NO_FILE_LOADED_MSG = "No file is currently opened"
    NO_LOUPE_SELECTED_MSG = 'No tile selected in loupe'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_handle: BinaryIO | None = None
        self.file_path: str | None = None
        self.file_size: int = 0
        self.offset: int = 0
        self.renderer: RawRender | None = None
        self.shortcuts: list[QShortcut] = []
        self.setupUi(self)

        #add a delay to offset line edit so we only update after X seconds of no typing
        self.offset_timer = QTimer(self)
        self.offset_timer.setSingleShot(True)
        self.offset_timer.timeout.connect(self.process_offset)

        self.offset_line.setValidator(QRegularExpressionValidator('[a-fA-F0-9]+'))
        self.width_spin.setValue(self.DEFAULT_SPIN_WIDTH)
        self.height_spin.setValue(self.DEFAULT_SPIN_HEIGHT)

        self.main_label.installEventFilter(self)

        self.open_file_button.clicked.connect(self.open_file)
        self.offset_line.textEdited.connect(lambda: self.offset_timer.start(self.OFFSET_PROCESS_DELAY))
        self.saveStateChanged.connect(self.draw_main)
        self.fullRefresh.connect(self.draw_main)
        self.paletteSwapped.connect(self.draw_main)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.save_button.clicked.connect(self.save_image)
        self.keyboard_button.toggled.connect(self.toggle_shortcuts)
        #input changes, redraw
        self.tile_height_combo.currentIndexChanged.connect(self.draw_main)
        self.width_spin.valueChanged.connect(self.draw_main)
        self.height_spin.valueChanged.connect(self.draw_main)
        self.zoom_combo.currentIndexChanged.connect(self.draw_main)
        self.pal_combo.currentIndexChanged.connect(self.draw_main)
        self.pivot_button.clicked.connect(self.draw_main)
        
        self.register_shortcuts()
        self.clear_main_image()
        self.update_offset()

    def eventFilter(self, obj, event):
        if obj == self.main_label and event.type() == QEvent.Type.MouseButtonRelease:
            self.handle_main_label_click(event)
        return super().eventFilter(obj, event)
    
    def handle_main_label_click(self, event: QMouseEvent):
        if self.file_handle is None:
            return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        zoom = int(self.zoom_combo.currentText())
        tw = 8
        th = int(self.tile_height_combo.currentText())
        x = event.x() // zoom
        y = event.y() // zoom
        if self.pivot_button.isChecked():
            tile_num = (x // tw) * self.width_spin.value() + (y // th)
        else:
            tile_num = (y // th) * self.height_spin.value() + (x // tw)
        offset = tile_num * self.get_tile_bytes() + self.offset
        #sanity check
        if offset > self.file_size:
            return
        self.tile_loupe.reference = offset
        self.draw_loupe()
    
    def register_shortcuts(self):
        self.new_shortcut(QKeySequence("Right"), 
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.INCREMENT))
        self.new_shortcut(QKeySequence("Left"), 
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.DECREMENT))
        self.new_shortcut(QKeySequence("Down"), 
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.LINE))
        self.new_shortcut(QKeySequence("Up"),
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.LINE))
        self.new_shortcut(QKeySequence("Shift+Right"),
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.TILE))
        self.new_shortcut(QKeySequence("Shift+Left"),
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.TILE))
        self.new_shortcut(QKeySequence("Shift+Down"),
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.WINDOW))
        self.new_shortcut(QKeySequence("Shift+Up"),
                          lambda: self.adjust_offset(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.WINDOW))
        
    def new_shortcut(self, sequence: QKeySequence, callback: callable):
        shortcut = QShortcut(sequence, self)
        shortcut.activated.connect(callback)
        shortcut.setEnabled(self.keyboard_button.isChecked())
        self.shortcuts.append(shortcut)

    def toggle_shortcuts(self, checked):
        for shortcut in self.shortcuts:
            shortcut.setEnabled(checked)
        #get focus off the form elements
        if checked:
            self.scroll_area.setFocus()

    def adjust_offset(self, dir: POSITION_DIRECTION, size: POSITION_SIZE = POSITION_SIZE.SINGLE):
        if self.file_handle is None:
            return
        adjustment: int = 1 if dir == self.POSITION_DIRECTION.INCREMENT else -1
        multiple: int
        match size:
            case self.POSITION_SIZE.TILE:
                multiple = self.get_tile_bytes()
            case self.POSITION_SIZE.LINE:
                multiple = self.get_tile_bytes() * self.width_spin.value()
            case self.POSITION_SIZE.WINDOW:
                multiple = self.get_tile_bytes() * self.width_spin.value() * self.height_spin.value()
            case _:
                multiple = 1
        
        new = self.clamp_offset(self.offset + adjustment * multiple)
        #skip redraw if we clamped and went nowhere
        if new == self.offset:
            return
        self.offset = new
        self.update_offset()
        self.draw_main()

    def update_offset(self):
        self.offset_line.setText(f'{self.offset:X}')

    def update_loupe_position(self):
        offset_from = self.tile_loupe.reference
        offset_to = self.tile_loupe.reference + self.tile_loupe.tiles_drawn * self.get_tile_bytes() - 1
        self.loupe_position_label.setText(f'{offset_from:X}h - {offset_to:X}h')

    def process_offset(self):
        try:
            new_offset = self.clamp_offset(int(self.offset_line.text(), 16))
            self.offset = new_offset
            self.update_offset()
            self.draw_main()
        except ValueError:
            pass

    def clamp_offset(self, offset: int) -> int:
        return max(0, min(offset, self.file_size))

    def clear_main_image(self):
        self.main_label.clear()
        self.main_label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.loupe_position_label.clear()

    def open_file(self):
        suggested = dirname(self.file_path) if self.file_path else None
        dialog = QFileDialog.getOpenFileName(parent=self, dir=suggested)
        if not isfile(dialog[0]):
            return
        self.offset = 0
        self.update_offset()
        self.close_file()
        try:
            self.file_handle = open(dialog[0], 'rb')
            self.file_path = dialog[0]
            self.opened_file_line.setText(self.file_path)
            self.file_size = fstat(self.file_handle.fileno()).st_size
            self.offset_line.setEnabled(True)
            self.renderer = RawRender(self.file_handle, self.file_size)
            self.draw_main()
        except Exception as e:
            self.statusMessage.emit(f"Could not load {dialog[0]}: {e}")

    def close_file(self):
        try:
            if self.file_handle is not None:
                self.file_handle.close()
            self.file_path = None
        except Exception:
            pass

    def draw_main(self):
        if self.file_handle is None:
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
        if self.tile_loupe.reference is None or self.file_handle is None:
            return
        img = self.get_pil_loupe()
        self.tile_loupe.set_image(QPixmap.fromImage(pil_to_qimage(img)), img.width, img.height)
        img.close()
        self.update_loupe_position()

    def copy_to_clipboard(self):
        if self.file_handle is None:
            self.statusMessage.emit(self.NO_FILE_LOADED_MSG)
            return
        img = self.get_pil_image()
        pil_to_clipboard(img)
        img.close()

    def save_image(self):
        if self.file_handle is None:
            self.statusMessage.emit(self.NO_FILE_LOADED_MSG)
            return
        img = self.get_pil_image()
        path = self.build_image_path()
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")

    def build_image_path(self):
        parts = [
            f'{self.offset:08X}',
            self.tile_height_combo.currentText(),
            str(self.width_spin.value()),
            str(self.width_spin.value()),
            'global' if self.app.use_global_pal else 'state',
            self.pal_combo.currentText(),
        ]
        if self.pivot_button.isChecked():
            parts.append('pivot')
        key = "_".join(parts)
        return f'{self.app.config.output_path}/{basename(self.file_path)}_{key}.png'

    def get_pil_image(self) -> Image.Image:
        pal_data = self.app.get_palette_and_background()
        img = self.renderer.get_image(
            self.offset,
            self.width_spin.value(),
            self.height_spin.value(),
            self.pal_combo.currentIndex(),
            pal_data[0],
            int(self.tile_height_combo.currentText()),
            self.pivot_button.isChecked()
        )
        img.putpalette(pal_data[1].flattened_colors())
        return img
    
    def get_pil_loupe(self) -> Image.Image:
        pal_data = self.app.get_palette_and_background()
        img = self.renderer.get_image(
            self.tile_loupe.reference,
            self.tile_loupe.get_width(),
            self.tile_loupe.get_height(),
            self.pal_combo.currentIndex(),
            pal_data[0],
            int(self.tile_height_combo.currentText()),
            self.pivot_button.isChecked()
        )
        self.tile_loupe.tiles_drawn = self.renderer.get_tiles_drawn()
        img.putpalette(pal_data[1].flattened_colors())
        return img
    
    def get_tile_bytes(self) -> int:
        return 8 * int(self.tile_height_combo.currentText()) // 2

    def __del__(self):
        self.close_file()