#Hand-made widget that does not have a Qt Creator file
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSpinBox, QSizePolicy, QPushButton
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from ..uibase import resource_rc

class TileLoupe(QWidget):
    sizeChanged: Signal = Signal(int, int)
    saveInitiated: Signal = Signal()
    copyInitiated: Signal = Signal()

    def __init__(self, parent, zoom: int = 2):
        super().__init__(parent)
        self.zoom = zoom
        self.width_spin = QSpinBox()
        self.height_spin = QSpinBox()
        self.image_label = QLabel()
        self.save_button = QPushButton("Save")
        self.copy_button = QPushButton("Copy")
        self.setupUi()

        self.width_spin.valueChanged.connect(self.emit_size_change)
        self.save_button.clicked.connect(lambda: self.saveInitiated.emit())
        self.copy_button.clicked.connect(lambda: self.copyInitiated.emit())

    def emit_size_change(self):
        self.sizeChanged.emit(self.width_spin.value(), self.height_spin.value())

    def set_image(self, image: QPixmap, width: int, height: int):
        width *= self.zoom
        height *= self.zoom
        self.image_label.setPixmap(image.scaled(
            width, 
            height, 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation)
        )
        self.image_label.setFixedSize(width, height)

    def reset(self):
        self.image_label.clear()

    def setupUi(self):
        by_label = QLabel('x')
        by_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        save_icon = QIcon()
        save_icon.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_button.setIcon(save_icon)
        copy_icon = QIcon()
        copy_icon.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_button.setIcon(copy_icon)
        self.width_spin.setMinimum(1)
        self.width_spin.setMaximum(4)
        self.height_spin.setMinimum(1)
        self.height_spin.setMaximum(4)
        main_layout = QVBoxLayout(self)
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(self.width_spin)
        spin_layout.addWidget(by_label)
        spin_layout.addWidget(self.height_spin)
        main_layout.addLayout(spin_layout)
        main_layout.addWidget(self.image_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.copy_button)
        main_layout.addLayout(button_layout)