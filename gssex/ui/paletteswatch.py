#Hand-made widget that does not have a Qt Creator file
from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QColorDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPalette
from gssex.state import Palette

#we should only need this here...
class SwatchColor(QWidget):
    TILE_SIZE = 24
    def __init__(self, color: QColor, index: int, **kwargs):
        super().__init__(**kwargs)
        self._index: int = index
        self._color: QColor = color
        self.setAutoFillBackground(True)
        self.drawColor(color)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.setMinimumWidth(self.TILE_SIZE)
        self.setMinimumHeight(self.TILE_SIZE)

    def drawColor(self, color: QColor):
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(pal)

    def selectColor(self):
        color = QColorDialog.getColor(self._color)
        if not color.isValid():
            return
        self.drawColor(color)
        self.parentWidget().colorChanged.emit(self._index, QColor(color))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if(event.button() == Qt.MouseButton.LeftButton and self.parentWidget().property("editable")):
            self.selectColor()
            return
        if(event.button() == Qt.MouseButton.RightButton):
            self.parentWidget().colorCopy.emit(self._index, QColor(self._color))
            return

class PaletteSwatch(QWidget):
    colorChanged: Signal = Signal(int, QColor)
    colorCopy: Signal = Signal(int, QColor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elements: list[SwatchColor] = []
        self.swatch_size = 64
        self.setProperty(u"editable", False)
        self.setupUi()
    
    def setupUi(self):
        width = 16
        layout = QGridLayout()
        layout.setHorizontalSpacing(1)
        layout.setVerticalSpacing(1)
        for k in range(0, self.swatch_size):
            element = SwatchColor(QColor(0), k, parent=self)
            self.elements.append(element)
            layout.addWidget(element, k // width, k % width)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

    def empty(self):
        black = QColor(0)
        for k in range(0, self.swatch_size):
            self.elements[k].drawColor(black)

    def show_gssex_pal(self, palette: Palette):
        for k in range(0, self.swatch_size):
            self.elements[k].drawColor(QColor(palette.get_color_as_rgb(k)))
