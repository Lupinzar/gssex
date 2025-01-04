from .rendertab import RenderTab
from .tileloupe import TileLoupe
from ..uibase.tabraw import Ui_TabRaw
from typing import BinaryIO
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent
from PySide6.QtWidgets import QFileDialog
from os.path import isfile, dirname

class TabRaw(RenderTab, Ui_TabRaw):
    DEFAULT_SPIN_WIDTH = 16
    DEFAULT_SPIN_HEIGHT = 16
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_handle: BinaryIO | None = None
        self.file_path: str | None = None
        self.setupUi(self)

        self.width_spin.setValue(self.DEFAULT_SPIN_WIDTH)
        self.height_spin.setValue(self.DEFAULT_SPIN_HEIGHT)
        self.clear_main_image()

        self.open_file_button.clicked.connect(self.open_file)

    def clear_main_image(self):
        self.main_label.clear()
        self.main_label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.loupe_position_label.clear()

    def open_file(self):
        suggested = dirname(self.file_path) if self.file_path else None
        dialog = QFileDialog.getOpenFileName(parent=self, dir=suggested)
        if not isfile(dialog[0]):
            return
        self.close_file()
        try:
            self.file_handle = open(dialog[0], 'rb')
            self.file_path = dialog[0]
            self.opened_file_line.setText(self.file_path)
        except Exception as e:
            self.statusMessage.emit(f"Could not load {dialog[0]}: {e}")

    def close_file(self):
        try:
            if self.file_handle is not None:
                self.file_handle.close()
            self.file_path = None
        except Exception:
            pass

    def __del__(self):
        self.close_file()