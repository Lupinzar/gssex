from .rendertab import RenderTab
from ..uibase.tabvram import Ui_TabVram
from ..render import VramRender
from .app import pil_to_qimage, pil_to_clipboard
from PIL import Image
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class TabVram(RenderTab, Ui_TabVram):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.main_label.clear()
        self.saveStateChanged.connect(self.redraw)
        self.fullRefresh.connect(self.redraw)
        self.paletteSwapped.connect(self.redraw)
        self.zoom_combo.currentIndexChanged.connect(self.redraw)
        self.pal_combo.currentIndexChanged.connect(self.redraw)
        self.pivot_button.clicked.connect(self.redraw)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

    def redraw(self):
        if not self.app.valid_file:
            self.main_label.clear()
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
        pilimg.close()

    def copy_to_clipboard(self):
        if not self.app.valid_file:
            return
        img = self.get_pil_image()
        pil_to_clipboard(img)
        img.close()

    def get_pil_image(self) -> Image.Image:
        pal_data = self.app.get_palette_and_background(self.config)
        render = VramRender(self.app.savestate.pattern_data, self.pal_combo.currentIndex(), pal_data[0], pivot=self.pivot_button.isChecked())
        img = render.get_image()
        img.putpalette(pal_data[1].flattened_colors())
        return img
