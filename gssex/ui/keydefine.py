from PySide6.QtWidgets import (QWidget, QMainWindow,  QVBoxLayout, QKeySequenceEdit, QLabel, 
    QPushButton, QHBoxLayout, QGridLayout, QScrollArea, QMessageBox)
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import QSize
from gssex.ui.app import Shortcuts

class KeyDefine(QMainWindow):
    def __init__(self, parent, shortcuts: Shortcuts):
        super().__init__(parent)
        self.shortcuts = shortcuts
        self.key_widgets: dict[str, QKeySequenceEdit] = {}
        self.ok_button: QPushButton
        self.cancel_button: QPushButton
        self.setup_ui()
        
        self.ok_button.pressed.connect(self.ok)
        self.cancel_button.pressed.connect(self.cancel)
        self.cancel_button.setFocus()

    def setup_ui(self):
        self.setWindowTitle('Redefine Keyboard Shortcuts')
        self.resize(QSize(320, 420))

        cw = QWidget(self)
        main_layout = QVBoxLayout(cw)
        btn_layout = QHBoxLayout()
        
        scroll = QScrollArea()
        scroll.setObjectName('scroll')
        scroll.setWidgetResizable(True)
        key_widget = QWidget()
        key_widget.setObjectName('key parent')
        key_grid = QGridLayout(key_widget)
        key_grid.setObjectName('key grid')
        scroll.setWidget(key_widget)

        self.ok_button = QPushButton('Ok')
        self.cancel_button = QPushButton('Cancel')
        btn_layout.addWidget(self.ok_button)
        btn_layout.addWidget(self.cancel_button)

        row = 0
        for key, data in Shortcuts.KEY_MAP.items():
            widget = QKeySequenceEdit(key_widget)
            widget.setMaximumSequenceLength(1)
            #widget.setClearButtonEnabled(True)
            widget.setKeySequence(self.shortcuts.get_sequence(key))
            widget.editingFinished.connect(self.sequence_done)
            key_grid.addWidget(QLabel(data[Shortcuts.FIELD_DESC], cw), row, 0)
            key_grid.addWidget(widget, row, 1)
            self.key_widgets[key] = widget
            row += 1

        main_layout.addWidget(QLabel('Click box to set key combination'))
        main_layout.addWidget(scroll)
        main_layout.addLayout(btn_layout)
        
        self.setCentralWidget(cw)

    def sequence_done(self):
        sender = self.sender()
        if hasattr(sender, 'clearFocus'):
            sender.clearFocus() #type: ignore

    def cancel(self):
        self.close()

    def ok(self):
        self.save()
        self.parent().shortcut_change.emit() #type: ignore
        self.close()

    def save(self):
        success: bool = False
        try:
            for name, widget in self.key_widgets.items():
                self.shortcuts.set_sequence(name, widget.keySequence().toString())
            success = self.shortcuts.save()
        except Exception as e:
            pass #TODO add logging
        if not success:
            self.shortcuts.load_defaults()
            QMessageBox.warning(None, 'Error', 'Error saving key binds to disk, using defaults for this session.')

    def print_seq(self):
        for key in Shortcuts.KEY_MAP.keys():
            print(key, self.key_widgets[key].keySequence().toString())