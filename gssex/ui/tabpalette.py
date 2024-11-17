from .rendertab import RenderTab
from ..uibase.tabpalette import Ui_TabPalette
from .app import App
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from typing import Tuple

class TabPalette(RenderTab, Ui_TabPalette):
    STATE_NOT_VALID_MSG = 'No valid save state currently loaded'
    globalPalChanged: Signal = Signal()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.app: App
        self.fullRefresh.connect(self.refresh_tab)
        self.global_swatch.colorChanged.connect(self.update_global_palette)
        self.copy_palette_button.pressed.connect(self.copy_all_to_global)
        self.state_swatch.colorCopy.connect(self.copy_single_to_global)

    def bind_app(self, app: App):
        self.app = app

    def refresh_tab(self):
        if not self.app:
            raise Exception("Application state not bound")
        if(self.app.valid_file):
            pass #TODO: add code for save state refresh
        else:
            self.state_swatch.empty()
        self.update_global_swatch()

    def update_global_swatch(self):
        self.global_swatch.show_gssex_pal(self.app.global_pal)

    def update_global_palette(self, index, color):
        self.app.global_pal.colors[index] = self.qcolor_to_tuple(color)

    def copy_single_to_global(self, index, color):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        #TODO: code save state copy

    def copy_all_to_global(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        #TODO: code save state copy

    @staticmethod
    def qcolor_to_tuple(color: QColor) -> Tuple[int, int, int]:
        return (color.red(), color.green(), color.blue())