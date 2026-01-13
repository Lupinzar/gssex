#Hand-made widget that does not have a Qt Creator file
from enum import Enum, auto
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSpinBox, QSizePolicy, QPushButton, QScrollArea
from PySide6.QtCore import Signal, Qt, QSize, QEvent
from PySide6.QtGui import QPixmap, QIcon, QKeySequence, QShortcut
from gssex.uibase import resource_rc
from typing import Callable

class TileLoupe(QWidget):
    class POSITION_DIRECTION(Enum):
        INCREMENT = auto()
        DECREMENT = auto()
    class POSITION_SIZE(Enum):
        SINGLE = auto()
        WHOLE = auto()
    MIN_SIZE = 1
    MAX_SIZE = 4
    sizeChanged: Signal = Signal(int, int)
    saveInitiated: Signal = Signal()
    copyInitiated: Signal = Signal()
    positionInitiated: Signal = Signal(Enum, Enum)

    def __init__(self, parent, zoom: int = 2):
        super().__init__(parent)
        self.zoom = zoom
        self.width_spin = QSpinBox()
        self.height_spin = QSpinBox()
        self.image_label = QLabel()
        self.save_button = QPushButton("Save")
        self.copy_button = QPushButton("Copy")
        self.inc_small_button = QPushButton()
        self.inc_large_button = QPushButton()
        self.dec_small_button = QPushButton()
        self.dec_large_button = QPushButton()
        self.image_scroll = QScrollArea()
        self.reference: None|int = None
        self.tiles_drawn: int = 0
        self.context_shortcuts: list[QShortcut] = []
        self.image_scroll.installEventFilter(self)
        self.setupUi()

        self.width_spin.valueChanged.connect(self.emit_size_change)
        self.height_spin.valueChanged.connect(self.emit_size_change)
        self.save_button.clicked.connect(lambda: self.saveInitiated.emit())
        self.copy_button.clicked.connect(lambda: self.copyInitiated.emit())
        self.inc_small_button.clicked.connect(lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.SINGLE))
        self.inc_large_button.clicked.connect(lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.WHOLE))
        self.dec_small_button.clicked.connect(lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.SINGLE))
        self.dec_large_button.clicked.connect(lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.WHOLE))

        self.register_shortcuts()

    def eventFilter(self, obj, event):
        if obj == self.image_scroll:
            if event.type() == QEvent.Type.Enter:
                self.toggle_context_shortcuts(True)
            if event.type() == QEvent.Type.Leave:
                self.toggle_context_shortcuts(False)
        return super().eventFilter(obj, event)

    def emit_size_change(self):
        self.sizeChanged.emit(self.width_spin.value(), self.height_spin.value())

    def register_shortcuts(self):
        self.new_context_shortcut(QKeySequence("Right"), 
                          lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.SINGLE))
        self.new_context_shortcut(QKeySequence("Left"), 
                          lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.SINGLE))
        self.new_context_shortcut(QKeySequence("Down"), 
                          lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.INCREMENT, self.POSITION_SIZE.WHOLE))
        self.new_context_shortcut(QKeySequence("Up"),
                          lambda: self.positionInitiated.emit(self.POSITION_DIRECTION.DECREMENT, self.POSITION_SIZE.WHOLE))
        self.new_context_shortcut(QKeySequence("Ctrl+Right"),
                          lambda: self.width_spin.setValue(self.width_spin.value() + 1))
        self.new_context_shortcut(QKeySequence("Ctrl+Left"),
                          lambda: self.width_spin.setValue(self.width_spin.value() - 1))
        self.new_context_shortcut(QKeySequence("Ctrl+Down"),
                          lambda: self.height_spin.setValue(self.height_spin.value() + 1))
        self.new_context_shortcut(QKeySequence("Ctrl+Up"),
                          lambda: self.height_spin.setValue(self.height_spin.value() - 1))
        
    def new_context_shortcut(self, sequence: QKeySequence, callback: Callable):
        shortcut = QShortcut(sequence, self)
        shortcut.activated.connect(callback)
        shortcut.setEnabled(False)
        self.context_shortcuts.append(shortcut)

    def toggle_context_shortcuts(self, checked: bool):
        for shortcut in self.context_shortcuts:
            shortcut.setEnabled(checked)

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

    def get_tile_area(self) -> int:
        return self.width_spin.value() * self.height_spin.value()
    
    def get_width(self) -> int:
        return self.width_spin.value()
    
    def get_height(self) -> int:
        return self.height_spin.value()

    def setupUi(self):
        by_label = QLabel('x')
        by_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        save_icon = QIcon()
        save_icon.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_button.setIcon(save_icon)
        copy_icon = QIcon()
        copy_icon.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_button.setIcon(copy_icon)
        
        self.width_spin.setMinimum(self.MIN_SIZE)
        self.width_spin.setMaximum(self.MAX_SIZE)
        self.height_spin.setMinimum(self.MIN_SIZE)
        self.height_spin.setMaximum(self.MAX_SIZE)

        #make sure widget can show at least a 4x4 sprite with 8x8 tiles
        minsize = self.MAX_SIZE * self.zoom * 8 + self.image_scroll.frameWidth() * 2
        self.image_scroll.setWidget(self.image_label)
        self.image_scroll.setMinimumSize(minsize, minsize)
        self.image_scroll.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(self.width_spin)
        spin_layout.addWidget(by_label)
        spin_layout.addWidget(self.height_spin)
        main_layout.addLayout(spin_layout)
        main_layout.addWidget(self.image_scroll)

        pos_buttons = [self.dec_large_button, self.dec_small_button, self.inc_small_button, self.inc_large_button]
        pos_icons = ['chevrons-left.svg', 'chevron-left.svg', 'chevron-right.svg', 'chevrons-right']
        pos_layout = QHBoxLayout()
        for ndx, btn in enumerate(pos_buttons):
            icon = QIcon()
            icon.addFile(f":/icons/{pos_icons[ndx]}", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            btn.setIcon(icon)
            pos_layout.addWidget(btn)

        main_layout.addLayout(pos_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.copy_button)

        main_layout.addLayout(button_layout)