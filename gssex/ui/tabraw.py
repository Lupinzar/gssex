from .rendertab import RenderTab
from .tileloupe import TileLoupe
from ..uibase.tabraw import Ui_TabRaw
from ..render import RawRender
from ..rawfile import RawFile, BinarySearch
from .app import pil_to_qimage, pil_to_clipboard
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QRegularExpressionValidator, QShortcut, QKeySequence
from PySide6.QtWidgets import QFileDialog
from os.path import isfile
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
        self.file: RawFile | None = None
        self.offset: int = 0
        self.renderer: RawRender | None = None
        self.shortcuts: list[QShortcut] = []
        self.setupUi(self)
        self.search: BinarySearch | None = None

        #add a delay to offset line edit so we only update after X seconds of no typing
        self.offset_timer = QTimer(self)
        self.offset_timer.setSingleShot(True)
        self.offset_timer.timeout.connect(self.process_offset)

        self.offset_line.setValidator(QRegularExpressionValidator('[a-fA-F0-9]+'))
        self.width_spin.setValue(self.DEFAULT_SPIN_WIDTH)
        self.height_spin.setValue(self.DEFAULT_SPIN_HEIGHT)

        self.main_label.installEventFilter(self)
        self.scroll_area.installEventFilter(self)

        self.open_file_button.clicked.connect(self.open_file)
        self.offset_line.textEdited.connect(lambda: self.offset_timer.start(self.OFFSET_PROCESS_DELAY))
        self.saveStateChanged.connect(self.draw_main)
        self.fullRefresh.connect(self.draw_main)
        self.paletteSwapped.connect(self.draw_main)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.save_button.clicked.connect(self.save_image)
        self.find_next_button.clicked.connect(self.data_search_next)
        self.find_previous_button.clicked.connect(self.data_serach_prev)
        #input changes, redraw
        self.tile_height_combo.currentIndexChanged.connect(self.draw_main)
        self.width_spin.valueChanged.connect(self.draw_main)
        self.height_spin.valueChanged.connect(self.draw_main)
        self.zoom_combo.currentIndexChanged.connect(self.draw_main)
        self.pal_combo.currentIndexChanged.connect(self.draw_main)
        self.pivot_button.clicked.connect(self.draw_main)

        self.tile_loupe.sizeChanged.connect(self.draw_loupe)
        self.tile_loupe.copyInitiated.connect(self.loupe_copy_to_clipboard)
        self.tile_loupe.saveInitiated.connect(self.loupe_save_image)
        self.tile_loupe.positionInitiated.connect(self.handle_loupe_position)
        
        self.register_shortcuts()
        self.clear_main_image()
        self.update_offset()

    def eventFilter(self, obj, event):
        if obj == self.main_label and event.type() == QEvent.Type.MouseButtonRelease:
            self.handle_main_label_click(event)
        if obj == self.scroll_area:
            if event.type() == QEvent.Type.Enter:
                self.toggle_shortcuts(True)
            if event.type() == QEvent.Type.Leave:
                self.toggle_shortcuts(False)
        return super().eventFilter(obj, event)
    
    def handle_main_label_click(self, event: QMouseEvent):
        if self.file is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_loupe_from_click(event)
            return
        if event.button() == Qt.MouseButton.RightButton:
            self.set_offset_from_click(event)
            return
        
    def set_loupe_from_click(self, event: QMouseEvent):
        offset = self.click_to_offset(event)
        if offset > self.file.size:
            return
        self.tile_loupe.reference = offset
        self.draw_loupe()

    def set_offset_from_click(self, event: QMouseEvent):
        offset = self.click_to_offset(event, tile_mode=False)
        if offset > self.file.size or offset == self.offset:
            return
        self.set_offset(offset)

    def click_to_offset(self, event: QMouseEvent, tile_mode: bool = True) -> int:
        zoom = int(self.zoom_combo.currentText())
        tw = 8
        th = int(self.tile_height_combo.currentText())
        x = event.x() // zoom
        y = event.y() // zoom

        if self.pivot_button.isChecked():
            tile_num = (x // tw) * self.height_spin.value() + (y // th)
        else:
            tile_num = (y // th) * self.width_spin.value() + (x // tw)
        offset = tile_num * self.get_tile_bytes() + self.offset
        if tile_mode:
            return offset
        return offset + x % tw // 2 + y % th * (tw // 2)
    
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
        self.new_shortcut(QKeySequence("Ctrl+Right"),
                          lambda: self.width_spin.setValue(self.width_spin.value() + 1))
        self.new_shortcut(QKeySequence("Ctrl+Left"),
                          lambda: self.width_spin.setValue(self.width_spin.value() - 1))
        self.new_shortcut(QKeySequence("Ctrl+Down"),
                          lambda: self.height_spin.setValue(self.height_spin.value() + 1))
        self.new_shortcut(QKeySequence("Ctrl+Up"),
                          lambda: self.height_spin.setValue(self.height_spin.value() - 1))
        
    def new_shortcut(self, sequence: QKeySequence, callback: callable):
        shortcut = QShortcut(sequence, self)
        shortcut.activated.connect(callback)
        shortcut.setEnabled(False)
        self.shortcuts.append(shortcut)

    def toggle_shortcuts(self, checked: bool):
        for shortcut in self.shortcuts:
            shortcut.setEnabled(checked)

    def adjust_offset(self, dir: POSITION_DIRECTION, size: POSITION_SIZE = POSITION_SIZE.SINGLE):
        if self.file is None:
            return
        adjustment: int = 1 if dir == self.POSITION_DIRECTION.INCREMENT else -1
        multiple: int
        match size:
            case self.POSITION_SIZE.TILE:
                multiple = self.get_tile_bytes()
            case self.POSITION_SIZE.LINE:
                multiple = self.get_tile_bytes() * (self.height_spin.value() if self.pivot_button.isChecked() else self.width_spin.value())
            case self.POSITION_SIZE.WINDOW:
                multiple = self.get_tile_bytes() * self.width_spin.value() * self.height_spin.value()
            case _:
                multiple = 1
        
        new = self.clamp_offset(self.offset + adjustment * multiple)
        #skip redraw if we clamped and went nowhere
        if new == self.offset:
            return
        self.set_offset(new)

    def update_offset(self):
        self.offset_line.setText(f'{self.offset:X}')

    def update_find_buttons(self):
        enabled = self.search is not None and self.search.found
        self.find_next_button.setEnabled(enabled)
        self.find_previous_button.setEnabled(enabled)

    def update_loupe_position(self):
        offset_from = self.tile_loupe.reference
        offset_to = self.tile_loupe.reference + self.tile_loupe.tiles_drawn * self.get_tile_bytes() - 1
        self.loupe_position_label.setText(f'{offset_from:X}h - {offset_to:X}h')

    def process_offset(self):
        try:
            new_offset = self.clamp_offset(int(self.offset_line.text(), 16))
            self.set_offset(new_offset)
        except ValueError:
            pass

    def set_offset(self, offset: int):
        self.offset = offset
        self.update_offset()
        self.draw_main()

    def clamp_offset(self, offset: int) -> int:
        return max(0, min(offset, self.file.size))

    def clear_main_image(self):
        self.main_label.clear()
        self.main_label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.loupe_position_label.clear()

    def open_file(self):
        suggested = self.file.dirname() if self.file else None
        dialog = QFileDialog.getOpenFileName(parent=self, dir=suggested)
        if not isfile(dialog[0]):
            return
        self.offset = 0
        self.update_offset()
        self.search = None
        self.update_find_buttons()
        if self.file:
            self.file.close()
        try:
            self.file = RawFile(dialog[0])
            if self.file.size == 0:
                raise Exception("File is empty")
            self.opened_file_line.setText(self.file.path)
            self.offset_line.setEnabled(True)
            self.renderer = RawRender(self.file)
            self.draw_main()
        except Exception as e:
            self.statusMessage.emit(f"Could not load {dialog[0]}: {e}")

    def draw_main(self):
        if self.file is None:
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
        if self.tile_loupe.reference is None or self.file is None:
            return
        img = self.get_pil_loupe()
        self.tile_loupe.set_image(QPixmap.fromImage(pil_to_qimage(img)), img.width, img.height)
        img.close()
        self.update_loupe_position()

    def copy_to_clipboard(self):
        if self.file is None:
            self.statusMessage.emit(self.NO_FILE_LOADED_MSG)
            return
        img = self.get_pil_image()
        pil_to_clipboard(img)
        img.close()

    def save_image(self):
        if self.file is None:
            self.statusMessage.emit(self.NO_FILE_LOADED_MSG)
            return
        img = self.get_pil_image()
        path = self.build_image_path()
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")

    def loupe_copy_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.NO_FILE_LOADED_MSG)
            return
        if self.tile_loupe.reference is None:
            self.statusMessage.emit(self.NO_LOUPE_SELECTED_MSG)
            return
        img = self.get_pil_loupe()
        pil_to_clipboard(img)
        img.close()

    def loupe_save_image(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.NO_FILE_LOADED_MSG)
            return
        if self.tile_loupe.reference is None:
            self.statusMessage.emit(self.NO_LOUPE_SELECTED_MSG)
            return
        img = self.get_pil_loupe()
        path = self.build_loupe_image_path()
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")

    def handle_loupe_position(self, direction: Enum, size: Enum):
        if self.file is None:
            return
        #if they haven't chosen a tile yet, just start at current offset
        start = self.offset if self.tile_loupe.reference is None else self.tile_loupe.reference
        amount = self.get_tile_bytes() if size == TileLoupe.POSITION_SIZE.SINGLE else self.tile_loupe.get_tile_area() * self.get_tile_bytes()
        if direction == TileLoupe.POSITION_DIRECTION.DECREMENT:
            amount = -amount
        new = start + amount
        if new < 0 or new >= self.file.size:
            return
        self.tile_loupe.reference = new
        self.draw_loupe()

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
        return f'{self.app.config.output_path}/{self.file.basename()}_{key}.png'
    
    def build_loupe_image_path(self):
        parts = [
            f'{self.tile_loupe.reference:08X}',
            self.tile_height_combo.currentText(),
            str(self.tile_loupe.get_width()),
            str(self.tile_loupe.get_height()),
            'global' if self.app.use_global_pal else 'state',
            self.pal_combo.currentText()
        ]
        if self.pivot_button.isChecked():
            parts.append('pivot')
        key = "_".join(parts)
        return f'{self.app.config.output_path}/{self.file.basename()}_{key}.png'

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
    
    def data_search(self, term: bytearray):
        self.search = BinarySearch(self.file, term)
        self.search.first()
        if not self.search.found:
            self.statusMessage.emit("Data not found in file")
            return False
        self.set_offset(self.search.last)
        self.update_find_buttons()

    def data_search_next(self):
        self.search.next()
        if self.search.looped:
            self.statusMessage.emit("Search looped from start of file")
        if self.search.last != self.offset:
            self.set_offset(self.search.last)

    def data_serach_prev(self):
        self.search.prev()
        if self.search.looped:
            self.statusMessage.emit("Search looped from end of file")
        if self.search.last != self.offset:
            self.set_offset(self.search.last)
