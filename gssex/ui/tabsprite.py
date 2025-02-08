from .rendertab import RenderTab
from .spritemodel import SpriteModel
from ..uibase.tabsprite import Ui_TabSprite
from ..state import SpriteTable
from ..render import SpriteImage
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel

class TabSprite(RenderTab, Ui_TabSprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.sprite_table: SpriteTable|None = None
        self.hidden_sprites: list[int] = []

        self.fullRefresh.connect(self.test_update)
        self.saveStateChanged.connect(self.test_update)
        #self.sprite_view.activated.connect(lambda index: print(f'act {index.row()}'))
        #self.sprite_view.doubleClicked.connect(lambda index: print(f'dbl clicked {index.row()}'))


    def resize_headers(self):
        head = self.sprite_view.horizontalHeader()
        for ndx, column in enumerate(SpriteModel.COLUMNS):
            head.setSectionResizeMode(ndx, column.resize_mode)

    def clear_view(self):
        self.sprite_view.setModel(QStandardItemModel())

    def test_update(self):
        if not self.app.valid_file:
            self.clear_view()
            return
        self.sprite_table = SpriteTable(self.app.savestate)
        self.sprite_model = SpriteModel(self.sprite_table)
        self.sprite_view.setModel(self.sprite_model)
        self.resize_headers()

