# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabsprite.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHeaderView, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget)
from . import resource_rc

class Ui_TabSprite(object):
    def setupUi(self, TabSprite):
        if not TabSprite.objectName():
            TabSprite.setObjectName(u"TabSprite")
        TabSprite.resize(733, 484)
        self.gridLayout = QGridLayout(TabSprite)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sprite_view = QTableView(TabSprite)
        self.sprite_view.setObjectName(u"sprite_view")

        self.gridLayout.addWidget(self.sprite_view, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.sprite_label = QLabel(TabSprite)
        self.sprite_label.setObjectName(u"sprite_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sprite_label.sizePolicy().hasHeightForWidth())
        self.sprite_label.setSizePolicy(sizePolicy)
        self.sprite_label.setMinimumSize(QSize(34, 68))
        self.sprite_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.sprite_label.setFrameShadow(QFrame.Shadow.Sunken)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_2.addWidget(self.sprite_label)

        self.save_sprite_button = QPushButton(TabSprite)
        self.save_sprite_button.setObjectName(u"save_sprite_button")
        icon = QIcon()
        icon.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_sprite_button.setIcon(icon)

        self.verticalLayout_2.addWidget(self.save_sprite_button)

        self.copy_sprite_button = QPushButton(TabSprite)
        self.copy_sprite_button.setObjectName(u"copy_sprite_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_sprite_button.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.copy_sprite_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.plane_scroll = QScrollArea(TabSprite)
        self.plane_scroll.setObjectName(u"plane_scroll")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.plane_scroll.sizePolicy().hasHeightForWidth())
        self.plane_scroll.setSizePolicy(sizePolicy1)
        self.plane_scroll.setMinimumSize(QSize(320, 224))
        self.plane_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 616, 266))
        self.plane_label = QLabel(self.scrollAreaWidgetContents)
        self.plane_label.setObjectName(u"plane_label")
        self.plane_label.setGeometry(QRect(0, 0, 71, 16))
        self.plane_scroll.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.plane_scroll, 1, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tile_margins_check = QCheckBox(TabSprite)
        self.tile_margins_check.setObjectName(u"tile_margins_check")

        self.verticalLayout_3.addWidget(self.tile_margins_check)

        self.label_3 = QLabel(TabSprite)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.trim_combo = QComboBox(TabSprite)
        self.trim_combo.setObjectName(u"trim_combo")

        self.verticalLayout_3.addWidget(self.trim_combo)

        self.save_plane_button = QPushButton(TabSprite)
        self.save_plane_button.setObjectName(u"save_plane_button")
        self.save_plane_button.setIcon(icon)

        self.verticalLayout_3.addWidget(self.save_plane_button)

        self.copy_plane_button = QPushButton(TabSprite)
        self.copy_plane_button.setObjectName(u"copy_plane_button")
        self.copy_plane_button.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.copy_plane_button)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.gridLayout.addLayout(self.verticalLayout_3, 1, 1, 1, 1)


        self.retranslateUi(TabSprite)

        QMetaObject.connectSlotsByName(TabSprite)
    # setupUi

    def retranslateUi(self, TabSprite):
        TabSprite.setWindowTitle(QCoreApplication.translate("TabSprite", u"Form", None))
        self.sprite_label.setText(QCoreApplication.translate("TabSprite", u"Img", None))
#if QT_CONFIG(tooltip)
        self.save_sprite_button.setToolTip(QCoreApplication.translate("TabSprite", u"Save Sprite", None))
#endif // QT_CONFIG(tooltip)
        self.save_sprite_button.setText(QCoreApplication.translate("TabSprite", u"Save", None))
#if QT_CONFIG(tooltip)
        self.copy_sprite_button.setToolTip(QCoreApplication.translate("TabSprite", u"Copy Sprite", None))
#endif // QT_CONFIG(tooltip)
        self.copy_sprite_button.setText(QCoreApplication.translate("TabSprite", u"Copy", None))
        self.plane_label.setText(QCoreApplication.translate("TabSprite", u"Sprite Plane", None))
        self.tile_margins_check.setText(QCoreApplication.translate("TabSprite", u"Tile Margins", None))
        self.label_3.setText(QCoreApplication.translate("TabSprite", u"Trim", None))
#if QT_CONFIG(tooltip)
        self.save_plane_button.setToolTip(QCoreApplication.translate("TabSprite", u"Save Sprite", None))
#endif // QT_CONFIG(tooltip)
        self.save_plane_button.setText(QCoreApplication.translate("TabSprite", u"Save", None))
#if QT_CONFIG(tooltip)
        self.copy_plane_button.setToolTip(QCoreApplication.translate("TabSprite", u"Copy Sprite", None))
#endif // QT_CONFIG(tooltip)
        self.copy_plane_button.setText(QCoreApplication.translate("TabSprite", u"Copy", None))
    # retranslateUi

