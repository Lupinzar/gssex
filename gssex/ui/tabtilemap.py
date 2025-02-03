from .rendertab import RenderTab
from ..uibase.tabtilemap import Ui_TabTileMap
from ..static import Plane
from PySide6.QtWidgets import QButtonGroup

class TabTileMap(RenderTab, Ui_TabTileMap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.setup_plane_combo()
        self.priority_group = QButtonGroup()
        
        self.priority_group.addButton(self.priority_both_radio)
        self.priority_group.addButton(self.priority_high_radio)
        self.priority_group.addButton(self.priority_low_radio)
    
    def setup_plane_combo(self):
        print(len(Plane))
        for k in range(0, len(Plane)):
            enum = Plane(k)
            nice = enum.name.replace("_", " ").title()
            self.plane_combo.addItem(nice)
