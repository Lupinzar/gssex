from PySide6.QtGui import QShortcut
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from gssex.ui.app import App

class RenderTab(QWidget):
    STATE_NOT_VALID_MSG = 'No valid save state currently loaded'
    fullRefresh: Signal = Signal()
    saveStateChanged: Signal = Signal()
    statusMessage: Signal = Signal(str)
    paletteSwapped: Signal = Signal()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app: App
        self.shortcuts: dict[str, QShortcut] = {}
    
    #need to find a better way to do this
    def bind_states(self, app: App):
        self.app = app

    def register_shortcuts(self):
        pass

    def update_shortcuts(self):
        for key in self.shortcuts.keys():
            self.shortcuts[key].setKey(self.app.shortcuts.get_sequence(key))
