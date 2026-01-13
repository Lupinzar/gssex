# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabtilemap.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_TabTileMap(object):
    def setupUi(self, TabTileMap):
        if not TabTileMap.objectName():
            TabTileMap.setObjectName(u"TabTileMap")
        TabTileMap.resize(493, 476)
        self.horizontalLayout_3 = QHBoxLayout(TabTileMap)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.plane_scroll = QScrollArea(TabTileMap)
        self.plane_scroll.setObjectName(u"plane_scroll")
        self.plane_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 329, 456))
        self.main_label = QLabel(self.scrollAreaWidgetContents)
        self.main_label.setObjectName(u"main_label")
        self.main_label.setGeometry(QRect(0, 0, 81, 16))
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

        self.label_5 = QLabel(TabTileMap)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.mode_map_radio = QRadioButton(TabTileMap)
        self.mode_map_radio.setObjectName(u"mode_map_radio")
        self.mode_map_radio.setChecked(False)

        self.verticalLayout_2.addWidget(self.mode_map_radio)

        self.mode_screen_button = QRadioButton(TabTileMap)
        self.mode_screen_button.setObjectName(u"mode_screen_button")
        self.mode_screen_button.setChecked(False)

        self.verticalLayout_2.addWidget(self.mode_screen_button)

        self.mode_marks_button = QRadioButton(TabTileMap)
        self.mode_marks_button.setObjectName(u"mode_marks_button")

        self.verticalLayout_2.addWidget(self.mode_marks_button)

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

        self.save_button = QPushButton(TabTileMap)
        self.save_button.setObjectName(u"save_button")
        icon = QIcon()
        icon.addFile(u":/icons/device-floppy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_button.setIcon(icon)

        self.verticalLayout_2.addWidget(self.save_button)

        self.copy_button = QPushButton(TabTileMap)
        self.copy_button.setObjectName(u"copy_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_button.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.copy_button)

        self._info_label = QLabel(TabTileMap)
        self._info_label.setObjectName(u"_info_label")

        self.verticalLayout_2.addWidget(self._info_label)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(TabTileMap)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.info_hscroll_label = QLabel(TabTileMap)
        self.info_hscroll_label.setObjectName(u"info_hscroll_label")
        sizePolicy.setHeightForWidth(self.info_hscroll_label.sizePolicy().hasHeightForWidth())
        self.info_hscroll_label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.info_hscroll_label, 0, 1, 1, 1)

        self.info_vscroll_label = QLabel(TabTileMap)
        self.info_vscroll_label.setObjectName(u"info_vscroll_label")
        sizePolicy.setHeightForWidth(self.info_vscroll_label.sizePolicy().hasHeightForWidth())
        self.info_vscroll_label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.info_vscroll_label, 1, 1, 1, 1)

        self.info_scroll_size_label = QLabel(TabTileMap)
        self.info_scroll_size_label.setObjectName(u"info_scroll_size_label")
        sizePolicy.setHeightForWidth(self.info_scroll_size_label.sizePolicy().hasHeightForWidth())
        self.info_scroll_size_label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.info_scroll_size_label, 2, 1, 1, 1)

        self.label_2 = QLabel(TabTileMap)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_6 = QLabel(TabTileMap)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_7 = QLabel(TabTileMap)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.info_window_size_label = QLabel(TabTileMap)
        self.info_window_size_label.setObjectName(u"info_window_size_label")
        sizePolicy.setHeightForWidth(self.info_window_size_label.sizePolicy().hasHeightForWidth())
        self.info_window_size_label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.info_window_size_label, 3, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(TabTileMap)

        QMetaObject.connectSlotsByName(TabTileMap)
    # setupUi

    def retranslateUi(self, TabTileMap):
        TabTileMap.setWindowTitle(QCoreApplication.translate("TabTileMap", u"Form", None))
        self.main_label.setText(QCoreApplication.translate("TabTileMap", u"Tile Map Image", None))
        self.label.setText(QCoreApplication.translate("TabTileMap", u"Plane", None))
        self.label_5.setText(QCoreApplication.translate("TabTileMap", u"Render Mode", None))
        self.mode_map_radio.setText(QCoreApplication.translate("TabTileMap", u"Map", None))
        self.mode_screen_button.setText(QCoreApplication.translate("TabTileMap", u"Screen", None))
        self.mode_marks_button.setText(QCoreApplication.translate("TabTileMap", u"Screen + Scroll Marks", None))
        self.label_4.setText(QCoreApplication.translate("TabTileMap", u"Priority", None))
        self.priority_both_radio.setText(QCoreApplication.translate("TabTileMap", u"Both", None))
        self.priority_high_radio.setText(QCoreApplication.translate("TabTileMap", u"High", None))
        self.priority_low_radio.setText(QCoreApplication.translate("TabTileMap", u"Low", None))
        self.save_button.setText(QCoreApplication.translate("TabTileMap", u"Save", None))
        self.copy_button.setText(QCoreApplication.translate("TabTileMap", u"Copy", None))
        self._info_label.setText(QCoreApplication.translate("TabTileMap", u"Info", None))
        self.label_3.setText(QCoreApplication.translate("TabTileMap", u"V Scroll", None))
        self.info_hscroll_label.setText(QCoreApplication.translate("TabTileMap", u"-", None))
        self.info_vscroll_label.setText(QCoreApplication.translate("TabTileMap", u"-", None))
        self.info_scroll_size_label.setText(QCoreApplication.translate("TabTileMap", u"-", None))
        self.label_2.setText(QCoreApplication.translate("TabTileMap", u"H Scroll", None))
        self.label_6.setText(QCoreApplication.translate("TabTileMap", u"Scroll Size  ", None))
        self.label_7.setText(QCoreApplication.translate("TabTileMap", u"Win. Size ", None))
        self.info_window_size_label.setText(QCoreApplication.translate("TabTileMap", u"-", None))
    # retranslateUi

