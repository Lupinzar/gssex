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
    
    #need to find a better way to do this
    def bind_states(self, app: App):
        self.app = app
