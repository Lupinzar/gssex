from .rendertab import RenderTab
from .tileloupe import TileLoupe
from ..uibase.tabraw import Ui_TabRaw

class TabRaw(RenderTab, Ui_TabRaw):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)