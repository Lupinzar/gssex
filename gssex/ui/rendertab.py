from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from .app import App, Config

class RenderTab(QWidget):
    fullRefresh: Signal = Signal()
    saveStateChanged: Signal = Signal()
    statusMessage: Signal = Signal(str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app: App
        self.config: Config
    
    #need to find a better way to do this
    def bind_states(self, app: App, config: Config):
        self.app = app
        self.config = config
