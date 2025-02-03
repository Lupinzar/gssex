# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabtilemap.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from . import resource_rc

class Ui_TabTileMap(object):
    def setupUi(self, TabTileMap):
        if not TabTileMap.objectName():
            TabTileMap.setObjectName(u"TabTileMap")
        TabTileMap.resize(493, 436)
        self.horizontalLayout_3 = QHBoxLayout(TabTileMap)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.plane_scroll = QScrollArea(TabTileMap)
        self.plane_scroll.setObjectName(u"plane_scroll")
        self.plane_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 297, 416))
        self.plane_scroll.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.plane_scroll)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(TabTileMap)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label)

        self.plane_combo = QComboBox(TabTileMap)
        self.plane_combo.setObjectName(u"plane_combo")

        self.verticalLayout_2.addWidget(self.plane_combo)

        self.label_4 = QLabel(TabTileMap)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.priority_both_radio = QRadioButton(TabTileMap)
        self.priority_both_radio.setObjectName(u"priority_both_radio")
        self.priority_both_radio.setChecked(True)

        self.verticalLayout_2.addWidget(self.priority_both_radio)

        self.priority_high_radio = QRadioButton(TabTileMap)
        self.priority_high_radio.setObjectName(u"priority_high_radio")

        self.verticalLayout_2.addWidget(self.priority_high_radio)

        self.priority_low_radio = QRadioButton(TabTileMap)
        self.priority_low_radio.setObjectName(u"priority_low_radio")

        self.verticalLayout_2.addWidget(self.priority_low_radio)

        self.line = QFrame(TabTileMap)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label_2 = QLabel(TabTileMap)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tile_map_save_button = QPushButton(TabTileMap)
        self.tile_map_save_button.setObjectName(u"tile_map_save_button")
        icon = QIcon()
        icon.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tile_map_save_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.tile_map_save_button)

        self.tile_map_copy_button = QPushButton(TabTileMap)
        self.tile_map_copy_button.setObjectName(u"tile_map_copy_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tile_map_copy_button.setIcon(icon1)

        self.horizontalLayout.addWidget(self.tile_map_copy_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(TabTileMap)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.label_3 = QLabel(TabTileMap)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.screen_save_button = QPushButton(TabTileMap)
        self.screen_save_button.setObjectName(u"screen_save_button")
        self.screen_save_button.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.screen_save_button)

        self.screen_copy_button = QPushButton(TabTileMap)
        self.screen_copy_button.setObjectName(u"screen_copy_button")
        self.screen_copy_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.screen_copy_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(TabTileMap)

        QMetaObject.connectSlotsByName(TabTileMap)
    # setupUi

    def retranslateUi(self, TabTileMap):
        TabTileMap.setWindowTitle(QCoreApplication.translate("TabTileMap", u"Form", None))
        self.label.setText(QCoreApplication.translate("TabTileMap", u"Plane", None))
        self.label_4.setText(QCoreApplication.translate("TabTileMap", u"Priority", None))
        self.priority_both_radio.setText(QCoreApplication.translate("TabTileMap", u"Both", None))
        self.priority_high_radio.setText(QCoreApplication.translate("TabTileMap", u"High", None))
        self.priority_low_radio.setText(QCoreApplication.translate("TabTileMap", u"Low", None))
        self.label_2.setText(QCoreApplication.translate("TabTileMap", u"Tile Map", None))
        self.tile_map_save_button.setText(QCoreApplication.translate("TabTileMap", u"Save", None))
        self.tile_map_copy_button.setText(QCoreApplication.translate("TabTileMap", u"Copy", None))
        self.label_3.setText(QCoreApplication.translate("TabTileMap", u"Screen", None))
        self.screen_save_button.setText(QCoreApplication.translate("TabTileMap", u"Save", None))
        self.screen_copy_button.setText(QCoreApplication.translate("TabTileMap", u"Copy", None))
    # retranslateUi

