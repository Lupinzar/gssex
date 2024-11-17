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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ..ui.paletteswatch import PaletteSwatch
from . import resource_rc

class Ui_TabPalette(object):
    def setupUi(self, TabPalette):
        if not TabPalette.objectName():
            TabPalette.setObjectName(u"TabPalette")
        TabPalette.resize(400, 395)
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

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.state_export_button = QPushButton(TabPalette)
        self.state_export_button.setObjectName(u"state_export_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.state_export_button.sizePolicy().hasHeightForWidth())
        self.state_export_button.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.state_export_button.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.state_export_button)

        self.state_clipboard_button = QPushButton(TabPalette)
        self.state_clipboard_button.setObjectName(u"state_clipboard_button")
        sizePolicy1.setHeightForWidth(self.state_clipboard_button.sizePolicy().hasHeightForWidth())
        self.state_clipboard_button.setSizePolicy(sizePolicy1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.state_clipboard_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.state_clipboard_button)

        self.copy_palette_button = QPushButton(TabPalette)
        self.copy_palette_button.setObjectName(u"copy_palette_button")
        sizePolicy1.setHeightForWidth(self.copy_palette_button.sizePolicy().hasHeightForWidth())
        self.copy_palette_button.setSizePolicy(sizePolicy1)
        icon2 = QIcon()
        icon2.addFile(u":/icons/chevron-down.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_palette_button.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.copy_palette_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.__global_pal_label = QLabel(TabPalette)
        self.__global_pal_label.setObjectName(u"__global_pal_label")
        sizePolicy.setHeightForWidth(self.__global_pal_label.sizePolicy().hasHeightForWidth())
        self.__global_pal_label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.__global_pal_label)

        self.global_swatch = PaletteSwatch(TabPalette)
        self.global_swatch.setObjectName(u"global_swatch")
        self.global_swatch.setProperty(u"editable", True)

        self.verticalLayout.addWidget(self.global_swatch)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.global_export_button = QPushButton(TabPalette)
        self.global_export_button.setObjectName(u"global_export_button")
        sizePolicy1.setHeightForWidth(self.global_export_button.sizePolicy().hasHeightForWidth())
        self.global_export_button.setSizePolicy(sizePolicy1)
        self.global_export_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.global_export_button)

        self.global_clipboard_button = QPushButton(TabPalette)
        self.global_clipboard_button.setObjectName(u"global_clipboard_button")
        sizePolicy1.setHeightForWidth(self.global_clipboard_button.sizePolicy().hasHeightForWidth())
        self.global_clipboard_button.setSizePolicy(sizePolicy1)
        self.global_clipboard_button.setIcon(icon1)

        self.horizontalLayout.addWidget(self.global_clipboard_button)

        self.global_import_button = QPushButton(TabPalette)
        self.global_import_button.setObjectName(u"global_import_button")
        sizePolicy1.setHeightForWidth(self.global_import_button.sizePolicy().hasHeightForWidth())
        self.global_import_button.setSizePolicy(sizePolicy1)
        icon3 = QIcon()
        icon3.addFile(u":/icons/folder-open.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.global_import_button.setIcon(icon3)

        self.horizontalLayout.addWidget(self.global_import_button)

        self.global_restore_button = QPushButton(TabPalette)
        self.global_restore_button.setObjectName(u"global_restore_button")
        sizePolicy1.setHeightForWidth(self.global_restore_button.sizePolicy().hasHeightForWidth())
        self.global_restore_button.setSizePolicy(sizePolicy1)
        icon4 = QIcon()
        icon4.addFile(u":/icons/restore.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.global_restore_button.setIcon(icon4)

        self.horizontalLayout.addWidget(self.global_restore_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(TabPalette)

        QMetaObject.connectSlotsByName(TabPalette)
    # setupUi

    def retranslateUi(self, TabPalette):
        TabPalette.setWindowTitle(QCoreApplication.translate("TabPalette", u"Form", None))
        self.__state_pal_label.setText(QCoreApplication.translate("TabPalette", u"State Palette - Right click to copy a single color to the Global palette", None))
        self.state_export_button.setText(QCoreApplication.translate("TabPalette", u"Export", None))
        self.state_clipboard_button.setText(QCoreApplication.translate("TabPalette", u"Clipboard", None))
        self.copy_palette_button.setText(QCoreApplication.translate("TabPalette", u"Copy All to Global", None))
        self.__global_pal_label.setText(QCoreApplication.translate("TabPalette", u"Global Palette - Left click a color to edit", None))
        self.global_export_button.setText(QCoreApplication.translate("TabPalette", u"Export", None))
        self.global_clipboard_button.setText(QCoreApplication.translate("TabPalette", u"Clipboard", None))
        self.global_import_button.setText(QCoreApplication.translate("TabPalette", u"Import", None))
        self.global_restore_button.setText(QCoreApplication.translate("TabPalette", u"Restore Default", None))
    # retranslateUi

