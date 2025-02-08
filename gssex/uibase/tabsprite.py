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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTableView, QVBoxLayout, QWidget)
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
        self.label = QLabel(TabSprite)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label)

        self.sprite_label = QLabel(TabSprite)
        self.sprite_label.setObjectName(u"sprite_label")
        sizePolicy.setHeightForWidth(self.sprite_label.sizePolicy().hasHeightForWidth())
        self.sprite_label.setSizePolicy(sizePolicy)
        self.sprite_label.setMinimumSize(QSize(32, 64))

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
        self.plane_scroll.setMinimumSize(QSize(320, 224))
        self.plane_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 601, 228))
        self.plane_label = QLabel(self.scrollAreaWidgetContents)
        self.plane_label.setObjectName(u"plane_label")
        self.plane_label.setGeometry(QRect(0, 0, 71, 16))
        self.plane_scroll.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.plane_scroll, 1, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(TabSprite)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.label_2)

        self.hide_button = QPushButton(TabSprite)
        self.hide_button.setObjectName(u"hide_button")
        icon2 = QIcon()
        icon2.addFile(u":/icons/eye-off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.hide_button.setIcon(icon2)

        self.verticalLayout_3.addWidget(self.hide_button)

        self.show_button = QPushButton(TabSprite)
        self.show_button.setObjectName(u"show_button")
        icon3 = QIcon()
        icon3.addFile(u":/icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.show_button.setIcon(icon3)

        self.verticalLayout_3.addWidget(self.show_button)

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
        self.label.setText(QCoreApplication.translate("TabSprite", u"Sprite", None))
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
        self.label_2.setText(QCoreApplication.translate("TabSprite", u"Plane", None))
        self.hide_button.setText(QCoreApplication.translate("TabSprite", u"Hide Selected", None))
        self.show_button.setText(QCoreApplication.translate("TabSprite", u"Show Selected", None))
#if QT_CONFIG(tooltip)
        self.save_plane_button.setToolTip(QCoreApplication.translate("TabSprite", u"Save Sprite", None))
#endif // QT_CONFIG(tooltip)
        self.save_plane_button.setText(QCoreApplication.translate("TabSprite", u"Save", None))
#if QT_CONFIG(tooltip)
        self.copy_plane_button.setToolTip(QCoreApplication.translate("TabSprite", u"Copy Sprite", None))
#endif // QT_CONFIG(tooltip)
        self.copy_plane_button.setText(QCoreApplication.translate("TabSprite", u"Copy", None))
    # retranslateUi

