# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabraw.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from ..ui.tileloupe import TileLoupe
from . import resource_rc

class Ui_TabRaw(object):
    def setupUi(self, TabRaw):
        if not TabRaw.objectName():
            TabRaw.setObjectName(u"TabRaw")
        TabRaw.resize(400, 400)
        self.horizontalLayout_2 = QHBoxLayout(TabRaw)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scroll_area = QScrollArea(TabRaw)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 186, 380))
        self.main_label = QLabel(self.scrollAreaWidgetContents)
        self.main_label.setObjectName(u"main_label")
        self.main_label.setGeometry(QRect(0, 0, 71, 16))
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.scroll_area)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self._opened_file = QLabel(TabRaw)
        self._opened_file.setObjectName(u"_opened_file")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self._opened_file)

        self._offset_label = QLabel(TabRaw)
        self._offset_label.setObjectName(u"_offset_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self._offset_label)

        self.offset_line = QLineEdit(TabRaw)
        self.offset_line.setObjectName(u"offset_line")
        self.offset_line.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.offset_line.sizePolicy().hasHeightForWidth())
        self.offset_line.setSizePolicy(sizePolicy)
        self.offset_line.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.offset_line)

        self._tile_height_label = QLabel(TabRaw)
        self._tile_height_label.setObjectName(u"_tile_height_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self._tile_height_label)

        self.tile_height_combo = QComboBox(TabRaw)
        self.tile_height_combo.addItem("")
        self.tile_height_combo.addItem("")
        self.tile_height_combo.setObjectName(u"tile_height_combo")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.tile_height_combo)

        self._size_label = QLabel(TabRaw)
        self._size_label.setObjectName(u"_size_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self._size_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.width_spin = QSpinBox(TabRaw)
        self.width_spin.setObjectName(u"width_spin")
        self.width_spin.setMinimum(1)

        self.horizontalLayout.addWidget(self.width_spin)

        self._cross_label = QLabel(TabRaw)
        self._cross_label.setObjectName(u"_cross_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self._cross_label.sizePolicy().hasHeightForWidth())
        self._cross_label.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self._cross_label)

        self.height_spin = QSpinBox(TabRaw)
        self.height_spin.setObjectName(u"height_spin")
        self.height_spin.setMinimum(1)

        self.horizontalLayout.addWidget(self.height_spin)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout)

        self._zoom_label = QLabel(TabRaw)
        self._zoom_label.setObjectName(u"_zoom_label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self._zoom_label)

        self.zoom_combo = QComboBox(TabRaw)
        self.zoom_combo.addItem("")
        self.zoom_combo.addItem("")
        self.zoom_combo.addItem("")
        self.zoom_combo.addItem("")
        self.zoom_combo.setObjectName(u"zoom_combo")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.zoom_combo)

        self._pal_label = QLabel(TabRaw)
        self._pal_label.setObjectName(u"_pal_label")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self._pal_label)

        self.pal_combo = QComboBox(TabRaw)
        self.pal_combo.addItem("")
        self.pal_combo.addItem("")
        self.pal_combo.addItem("")
        self.pal_combo.addItem("")
        self.pal_combo.setObjectName(u"pal_combo")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.pal_combo)

        self.open_file_button = QPushButton(TabRaw)
        self.open_file_button.setObjectName(u"open_file_button")
        icon = QIcon()
        icon.addFile(u":/icons/file.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_file_button.setIcon(icon)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.open_file_button)

        self.opened_file_line = QLineEdit(TabRaw)
        self.opened_file_line.setObjectName(u"opened_file_line")
        self.opened_file_line.setEnabled(False)
        sizePolicy.setHeightForWidth(self.opened_file_line.sizePolicy().hasHeightForWidth())
        self.opened_file_line.setSizePolicy(sizePolicy)
        self.opened_file_line.setReadOnly(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.opened_file_line)


        self.verticalLayout.addLayout(self.formLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.copy_button = QPushButton(TabRaw)
        self.copy_button.setObjectName(u"copy_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_button.setIcon(icon1)

        self.gridLayout.addWidget(self.copy_button, 2, 1, 1, 1)

        self.find_previous_button = QPushButton(TabRaw)
        self.find_previous_button.setObjectName(u"find_previous_button")
        self.find_previous_button.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/icons/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.find_previous_button.setIcon(icon2)

        self.gridLayout.addWidget(self.find_previous_button, 1, 0, 1, 1)

        self.save_button = QPushButton(TabRaw)
        self.save_button.setObjectName(u"save_button")
        icon3 = QIcon()
        icon3.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_button.setIcon(icon3)

        self.gridLayout.addWidget(self.save_button, 2, 0, 1, 1)

        self.find_next_button = QPushButton(TabRaw)
        self.find_next_button.setObjectName(u"find_next_button")
        self.find_next_button.setEnabled(False)
        self.find_next_button.setIcon(icon2)

        self.gridLayout.addWidget(self.find_next_button, 1, 1, 1, 1)

        self.pivot_button = QPushButton(TabRaw)
        self.pivot_button.setObjectName(u"pivot_button")
        self.pivot_button.setCheckable(True)
        self.pivot_button.setChecked(True)
        self.pivot_button.setFlat(False)

        self.gridLayout.addWidget(self.pivot_button, 0, 0, 1, 1)

        self.keyboard_button = QPushButton(TabRaw)
        self.keyboard_button.setObjectName(u"keyboard_button")
        self.keyboard_button.setCheckable(True)

        self.gridLayout.addWidget(self.keyboard_button, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.line = QFrame(TabRaw)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self._loupe_label = QLabel(TabRaw)
        self._loupe_label.setObjectName(u"_loupe_label")
        sizePolicy1.setHeightForWidth(self._loupe_label.sizePolicy().hasHeightForWidth())
        self._loupe_label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self._loupe_label)

        self.loupe_position_label = QLabel(TabRaw)
        self.loupe_position_label.setObjectName(u"loupe_position_label")
        self.loupe_position_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.loupe_position_label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.tile_loupe = TileLoupe(TabRaw)
        self.tile_loupe.setObjectName(u"tile_loupe")

        self.verticalLayout.addWidget(self.tile_loupe)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(TabRaw)

        QMetaObject.connectSlotsByName(TabRaw)
    # setupUi

    def retranslateUi(self, TabRaw):
        TabRaw.setWindowTitle(QCoreApplication.translate("TabRaw", u"Form", None))
        self.main_label.setText(QCoreApplication.translate("TabRaw", u"RAW Image", None))
        self._opened_file.setText(QCoreApplication.translate("TabRaw", u"File", None))
        self._offset_label.setText(QCoreApplication.translate("TabRaw", u"Offset (Hex)", None))
        self._tile_height_label.setText(QCoreApplication.translate("TabRaw", u"Tile Height", None))
        self.tile_height_combo.setItemText(0, QCoreApplication.translate("TabRaw", u"8", None))
        self.tile_height_combo.setItemText(1, QCoreApplication.translate("TabRaw", u"16", None))

        self._size_label.setText(QCoreApplication.translate("TabRaw", u"Size", None))
        self._cross_label.setText(QCoreApplication.translate("TabRaw", u"x", None))
        self._zoom_label.setText(QCoreApplication.translate("TabRaw", u"Zoom", None))
        self.zoom_combo.setItemText(0, QCoreApplication.translate("TabRaw", u"1", None))
        self.zoom_combo.setItemText(1, QCoreApplication.translate("TabRaw", u"2", None))
        self.zoom_combo.setItemText(2, QCoreApplication.translate("TabRaw", u"4", None))
        self.zoom_combo.setItemText(3, QCoreApplication.translate("TabRaw", u"8", None))

        self._pal_label.setText(QCoreApplication.translate("TabRaw", u"Palette", None))
        self.pal_combo.setItemText(0, QCoreApplication.translate("TabRaw", u"0", None))
        self.pal_combo.setItemText(1, QCoreApplication.translate("TabRaw", u"1", None))
        self.pal_combo.setItemText(2, QCoreApplication.translate("TabRaw", u"2", None))
        self.pal_combo.setItemText(3, QCoreApplication.translate("TabRaw", u"3", None))

        self.open_file_button.setText(QCoreApplication.translate("TabRaw", u"Open File", None))
        self.opened_file_line.setText("")
        self.opened_file_line.setPlaceholderText(QCoreApplication.translate("TabRaw", u"No File Selected", None))
        self.copy_button.setText(QCoreApplication.translate("TabRaw", u"Copy", None))
        self.find_previous_button.setText(QCoreApplication.translate("TabRaw", u"Previous", None))
        self.save_button.setText(QCoreApplication.translate("TabRaw", u"Save", None))
        self.find_next_button.setText(QCoreApplication.translate("TabRaw", u"Next", None))
        self.pivot_button.setText(QCoreApplication.translate("TabRaw", u"Pivot", None))
        self.keyboard_button.setText(QCoreApplication.translate("TabRaw", u"Keyboard", None))
        self._loupe_label.setText(QCoreApplication.translate("TabRaw", u"Tile Loupe", None))
        self.loupe_position_label.setText(QCoreApplication.translate("TabRaw", u"Position", None))
    # retranslateUi

