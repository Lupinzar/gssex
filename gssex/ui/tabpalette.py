from .rendertab import RenderTab
from ..uibase.tabpalette import Ui_TabPalette
from .app import App, pil_to_clipboard
from ..state import Palette
from ..render import PaletteImage
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QColor
from typing import Tuple
from os.path import isfile, dirname
import json

class TabPalette(RenderTab, Ui_TabPalette):
    STATE_NOT_VALID_MSG = 'No valid save state currently loaded'
    globalPalChanged: Signal = Signal()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.app: App
        self.last_save_path = ''
        self.last_open_path = ''
        self.fullRefresh.connect(self.refresh_tab)
        self.global_swatch.colorChanged.connect(self.update_global_palette)
        self.copy_palette_button.pressed.connect(self.copy_all_to_global)
        self.state_swatch.colorCopy.connect(self.copy_single_to_global)
        self.global_restore_button.pressed.connect(self.restore_global)
        self.global_export_button.pressed.connect(lambda: self.export_to_file(self.app.global_pal))
        self.global_import_button.pressed.connect(self.import_file)
        self.global_clipboard_button.pressed.connect(lambda: self.copy_to_clipboard(self.app.global_pal))
        self.state_export_button.pressed.connect(self.state_export_to_file)
        self.state_clipboard_button.pressed.connect(self.state_copy_to_clipboard)

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

    def restore_global(self):
        self.app.global_pal = Palette.make_unique()
        self.update_global_swatch()

    def import_file(self):
        suggested = self.last_open_path or self.config.output_path
        dialog = QFileDialog.getOpenFileName(parent=self, dir=suggested, filter='JSON (*.json)')
        if not isfile(dialog[0]):
            return
        try:
            self.last_open_path = dirname(dialog[0])
            with open(dialog[0]) as fp:
                data = json.load(fp)
            if not isinstance(data, list):
                raise Exception("Top level JSON element is not an array")
            colors = []
            for k, color in enumerate(data):
                if not isinstance(color, list):
                    raise Exception(f"Color {k} is not an array")
                if len(color) < 3:
                    raise Exception(f"Not enough values for index {k}")
                clamped = [max(0, min(b, 255)) for b in color]
                colors.append((int(clamped[0]), int(clamped[1]), int(clamped[2])))
            if len(colors) < Palette.GROUP_SIZE * Palette.SIZE:
                raise Exception("Not enough colors")
            self.app.global_pal = Palette(colors)
            self.update_global_swatch()
        except Exception as e:
            self.statusMessage.emit(f"Could not load {dialog[0]}: {e}")

    def export_to_file(self, palette: Palette):
        suggested = self.last_save_path or f'{self.config.output_path}'
        suggested += '/global'
        dialog = QFileDialog.getSaveFileName(parent=self, dir=suggested, filter='JSON (*.json);;Image (*.png)')
        if not dialog[1]:
            return
        try:
            if dialog[1] == 'JSON (*.json)':
                self.save_json(palette, dialog[0])
            elif dialog[1] == 'Image (*.png)':
                self.save_png(palette, dialog[0])
            else:
                raise Exception(f"Unhandled type {dialog[1]}")
            self.last_save_path = dirname(dialog[0])
            self.statusMessage.emit(f"Saved {dialog[0]}")
        except Exception as e:
            self.statusMessage.emit(f"Could not save {dialog[0]}: {e}")

    def state_export_to_file(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        #TODO: state handling
        #self.export_to_file(yada yada)

    def state_copy_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        #TODO: state handling
        #self.copy_to_clipboard(yada yada)

    def save_json(self, palette: Palette, path: str):
        with open(path, 'w') as fp:
            json.dump(palette.colors, fp)

    def save_png(self, palette: Palette, path: str):
        render = PaletteImage(palette)
        img = render.get_image()
        img.save(path)
        img.close()

    def copy_to_clipboard(self, palette: Palette):
        render = PaletteImage(palette)
        img = render.get_image()
        pil_to_clipboard(img)
        img.close()

    @staticmethod
    def qcolor_to_tuple(color: QColor) -> Tuple[int, int, int]:
        return (color.red(), color.green(), color.blue())