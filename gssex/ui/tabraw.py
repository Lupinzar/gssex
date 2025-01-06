from .rendertab import RenderTab
from .tileloupe import TileLoupe
from ..uibase.tabraw import Ui_TabRaw
from typing import BinaryIO
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QRegularExpressionValidator
from PySide6.QtWidgets import QFileDialog
from os.path import isfile, dirname
from os import fstat

class TabRaw(RenderTab, Ui_TabRaw):
    DEFAULT_SPIN_WIDTH = 16
    DEFAULT_SPIN_HEIGHT = 16
    OFFSET_PROCESS_DELAY = 500
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_handle: BinaryIO | None = None
        self.file_path: str | None = None
        self.file_size: int = 0
        self.offset: int = 0
        self.setupUi(self)

        #add a delay to offset line edit so we only update after X seconds of no typing
        self.offset_timer = QTimer(self)
        self.offset_timer.setSingleShot(True)
        self.offset_timer.timeout.connect(self.process_offset)

        self.offset_line.setValidator(QRegularExpressionValidator('[a-fA-F0-9]+'))
        self.width_spin.setValue(self.DEFAULT_SPIN_WIDTH)
        self.height_spin.setValue(self.DEFAULT_SPIN_HEIGHT)

        self.open_file_button.clicked.connect(self.open_file)
        self.offset_line.textEdited.connect(lambda: self.offset_timer.start(self.OFFSET_PROCESS_DELAY))

        self.clear_main_image()
        self.update_offset()

    def update_offset(self):
        self.offset_line.setText(f'{self.offset:X}')

    def process_offset(self):
        try:
            new_offset = min(int(self.offset_line.text(), 16), self.file_size)
            self.offset = new_offset
            self.update_offset()
            self.draw_main()
        except ValueError:
            pass


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
        #TODO code me
        pass

    def __del__(self):
        self.close_file()