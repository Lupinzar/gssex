from PySide6.QtWidgets import QPushButton, QColorDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal

'''
From an older PySide template:
https://www.pythonguis.com/widgets/qcolorbutton-a-color-selector-tool-for-pyqt/
'''

class ColorButton(QPushButton):
    colorChanged: Signal = Signal(QColor)

    def __init__(self, *args, color=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._color: QColor = QColor(0xFFFFFF)
        self._default: QColor = color
        self.pressed.connect(self.onColorPicker)
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)
        
        if self._color:
            self.setStyleSheet(f"background-color: {self._color.name()}")
        else:
            self.setStyleSheet("")

    def color(self) -> QColor:
        return self._color()
    
    def onColorPicker(self):
        dialog = QColorDialog.getColor(initial=self._color)
        if not dialog.isValid():
            return
        self.setColor(dialog)