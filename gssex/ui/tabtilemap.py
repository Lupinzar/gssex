from .rendertab import RenderTab
from ..uibase.tabtilemap import Ui_TabTileMap
from ..static import Plane
from PySide6.QtWidgets import QButtonGroup

class TabTileMap(RenderTab, Ui_TabTileMap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.setup_plane_combo()
        self.mode_group = QButtonGroup()
        self.priority_group = QButtonGroup()
        
        self.mode_group.addButton(self.mode_map_radio)
        self.mode_group.addButton(self.mode_screen_button)
        self.mode_map_radio.setChecked(True)

        self.priority_group.addButton(self.priority_both_radio)
        self.priority_group.addButton(self.priority_high_radio)
        self.priority_group.addButton(self.priority_low_radio)
        self.priority_both_radio.setChecked(True)
    
    def setup_plane_combo(self):
        for k in range(0, len(Plane)):
            enum = Plane(k)
            self.plane_combo.addItem(enum.name.replace("_", " ").title())
