# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabvram.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFormLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from . import resource_rc

class Ui_TabVram(object):
    def setupUi(self, TabVram):
        if not TabVram.objectName():
            TabVram.setObjectName(u"TabVram")
        TabVram.resize(400, 300)
        self.horizontalLayout_2 = QHBoxLayout(TabVram)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scroll_area = QScrollArea(TabVram)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 186, 280))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.main_label = QLabel(self.scrollAreaWidgetContents)
        self.main_label.setObjectName(u"main_label")
        self.main_label.setGeometry(QRect(0, 0, 69, 16))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy1)
        self.main_label.setScaledContents(False)
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.scroll_area)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self._zoom_label = QLabel(TabVram)
        self._zoom_label.setObjectName(u"_zoom_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self._zoom_label)

        self.zoom_combo = QComboBox(TabVram)
        self.zoom_combo.addItem("")
        self.zoom_combo.addItem("")
        self.zoom_combo.addItem("")
        self.zoom_combo.addItem("")
        self.zoom_combo.setObjectName(u"zoom_combo")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.zoom_combo)

        self._pal_label = QLabel(TabVram)
        self._pal_label.setObjectName(u"_pal_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self._pal_label)

        self.pal_combo = QComboBox(TabVram)
        self.pal_combo.addItem("")
        self.pal_combo.addItem("")
        self.pal_combo.addItem("")
        self.pal_combo.addItem("")
        self.pal_combo.setObjectName(u"pal_combo")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pal_combo)

        self.pivot_button = QPushButton(TabVram)
        self.pivot_button.setObjectName(u"pivot_button")
        self.pivot_button.setCheckable(True)
        self.pivot_button.setChecked(True)
        self.pivot_button.setFlat(False)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pivot_button)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.save_button = QPushButton(TabVram)
        self.save_button.setObjectName(u"save_button")

        self.horizontalLayout.addWidget(self.save_button)

        self.copy_button = QPushButton(TabVram)
        self.copy_button.setObjectName(u"copy_button")
        icon = QIcon()
        icon.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.copy_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(TabVram)

        QMetaObject.connectSlotsByName(TabVram)
    # setupUi

    def retranslateUi(self, TabVram):
        TabVram.setWindowTitle(QCoreApplication.translate("TabVram", u"Form", None))
        self.main_label.setText(QCoreApplication.translate("TabVram", u"VRAM Image", None))
        self._zoom_label.setText(QCoreApplication.translate("TabVram", u"Zoom", None))
        self.zoom_combo.setItemText(0, QCoreApplication.translate("TabVram", u"1", None))
        self.zoom_combo.setItemText(1, QCoreApplication.translate("TabVram", u"2", None))
        self.zoom_combo.setItemText(2, QCoreApplication.translate("TabVram", u"4", None))
        self.zoom_combo.setItemText(3, QCoreApplication.translate("TabVram", u"8", None))

        self._pal_label.setText(QCoreApplication.translate("TabVram", u"Palette", None))
        self.pal_combo.setItemText(0, QCoreApplication.translate("TabVram", u"0", None))
        self.pal_combo.setItemText(1, QCoreApplication.translate("TabVram", u"1", None))
        self.pal_combo.setItemText(2, QCoreApplication.translate("TabVram", u"2", None))
        self.pal_combo.setItemText(3, QCoreApplication.translate("TabVram", u"3", None))

        self.pivot_button.setText(QCoreApplication.translate("TabVram", u"Pivot", None))
        self.save_button.setText(QCoreApplication.translate("TabVram", u"Save", None))
        self.copy_button.setText(QCoreApplication.translate("TabVram", u"Copy", None))
    # retranslateUi

