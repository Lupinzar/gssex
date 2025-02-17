from ..state import SpriteTable
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHeaderView
from dataclasses import dataclass

@dataclass
class ModelColumn():
    attr: str|None
    header: str
    is_bool: bool = False
    hide_special: bool = False
    resize_mode: QHeaderView.ResizeMode = QHeaderView.ResizeMode.ResizeToContents

class SpriteModel(QAbstractTableModel):
    COLUMNS = [
        ModelColumn('start', 'Tile #', resize_mode=QHeaderView.ResizeMode.Stretch),
        ModelColumn('x', 'X', resize_mode=QHeaderView.ResizeMode.Stretch),
        ModelColumn('y', 'Y', resize_mode=QHeaderView.ResizeMode.Stretch),
        ModelColumn('width', 'Width'),
        ModelColumn('height', 'Height'),
        ModelColumn('link', 'Next'),
        ModelColumn('pal', "Pal #"),
        ModelColumn('priority', 'Priority', is_bool=True),
        ModelColumn('vflip', 'Ver Flip', is_bool=True),
        ModelColumn('hflip', 'Hor Flip', is_bool=True),
        ModelColumn(None, 'Hide', hide_special=True)
    ]
    COLUMN_COUNT = len(COLUMNS)
    def __init__(self, data: SpriteTable, hidden: set):
        super().__init__()
        self.sprite_table: SpriteTable = data.sprites
        self.drawn: list[int] = data.get_draw_list()
        self.hidden: set = hidden

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            column = self.COLUMNS[index.column()]
            if column.attr is not None:
                value = getattr(self.sprite_table[index.row()], column.attr)
                if column.is_bool:
                    return self.bool_to_yn(value)
                return value
            #if column.hide_special and index.row() in self.drawn:
                #return self.bool_to_yn(index.row() in self.hidden)
        if role == Qt.ItemDataRole.CheckStateRole:
            column = self.COLUMNS[index.column()]
            if column.hide_special and index.row() in self.drawn:
                return Qt.CheckState.Checked if index.row() in self.hidden else Qt.CheckState.Unchecked
        if role == Qt.ItemDataRole.ForegroundRole and index.row() not in self.drawn:
            return QColor('grey')
        if role == Qt.ItemDataRole.EditRole:
            column = self.COLUMNS[index.column()]
            if column.hide_special:
                return self.bool_to_yn(index.row() in self.hidden)
            
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role not in (Qt.ItemDataRole.EditRole, Qt.ItemDataRole.CheckStateRole):
            return False
        if not self.COLUMNS[index.column()].hide_special:
            return False
        if index.row() not in self.drawn:
            return False
        if value and index.row() not in self.hidden:
            self.hidden.add(index.row())
            self.dataChanged.emit(index, index)
            return True
        if not value and index.row() in self.hidden:
            self.hidden.remove(index.row())
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemNeverHasChildren
        if self.COLUMNS[index.column()].hide_special:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags
    
    def rowCount(self, parent):
        return len(self.sprite_table)
    
    def columnCount(self, parent):
        return self.COLUMN_COUNT
    
    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return
        if orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section].header
        if orientation == Qt.Orientation.Vertical:
            return section
        
    def bool_to_yn(self, value: bool) -> str:
        return 'Y' if value else 'N'