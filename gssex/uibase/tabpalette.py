# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabpalette.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from ..ui.paletteswatch import PaletteSwatch
from . import resource_rc

class Ui_TabPalette(object):
    def setupUi(self, TabPalette):
        if not TabPalette.objectName():
            TabPalette.setObjectName(u"TabPalette")
        TabPalette.resize(400, 300)
        self.verticalLayout = QVBoxLayout(TabPalette)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.__state_pal_label = QLabel(TabPalette)
        self.__state_pal_label.setObjectName(u"__state_pal_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.__state_pal_label.sizePolicy().hasHeightForWidth())
        self.__state_pal_label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.__state_pal_label)

        self.state_swatch = PaletteSwatch(TabPalette)
        self.state_swatch.setObjectName(u"state_swatch")
        self.state_swatch.setProperty(u"editable", False)

        self.verticalLayout.addWidget(self.state_swatch)

        self.copy_palette_button = QPushButton(TabPalette)
        self.copy_palette_button.setObjectName(u"copy_palette_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.copy_palette_button.sizePolicy().hasHeightForWidth())
        self.copy_palette_button.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u":/icons/chevron-down.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_palette_button.setIcon(icon)

        self.verticalLayout.addWidget(self.copy_palette_button)

        self.__global_pal_label = QLabel(TabPalette)
        self.__global_pal_label.setObjectName(u"__global_pal_label")
        sizePolicy.setHeightForWidth(self.__global_pal_label.sizePolicy().hasHeightForWidth())
        self.__global_pal_label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.__global_pal_label)

        self.global_swatch = PaletteSwatch(TabPalette)
        self.global_swatch.setObjectName(u"global_swatch")
        self.global_swatch.setProperty(u"editable", True)

        self.verticalLayout.addWidget(self.global_swatch)


        self.retranslateUi(TabPalette)

        QMetaObject.connectSlotsByName(TabPalette)
    # setupUi

    def retranslateUi(self, TabPalette):
        TabPalette.setWindowTitle(QCoreApplication.translate("TabPalette", u"Form", None))
        self.__state_pal_label.setText(QCoreApplication.translate("TabPalette", u"State Palette - Right click to copy a single color to the Global palette", None))
        self.copy_palette_button.setText(QCoreApplication.translate("TabPalette", u"Copy All to Global", None))
        self.__global_pal_label.setText(QCoreApplication.translate("TabPalette", u"Global Palette - Left click a color to edit", None))
    # retranslateUi

