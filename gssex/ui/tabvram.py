from .rendertab import RenderTab
from ..uibase.tabvram import Ui_TabVram

class TabVram(RenderTab, Ui_TabVram):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)