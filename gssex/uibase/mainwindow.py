# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QToolBar, QVBoxLayout,
    QWidget)

from gssex.ui.colorbutton import ColorButton
from gssex.ui.tabpalette import TabPalette
from gssex.ui.tabraw import TabRaw
from gssex.ui.tabsprite import TabSprite
from gssex.ui.tabtilemap import TabTileMap
from gssex.ui.tabvram import TabVram
from gssex.uibase import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QSize(640, 0))
        self.action_open_folder = QAction(MainWindow)
        self.action_open_folder.setObjectName(u"action_open_folder")
        icon = QIcon()
        icon.addFile(u":/icons/folder-open.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_open_folder.setIcon(icon)
        self.action_open_folder.setMenuRole(QAction.MenuRole.NoRole)
        self.action_previous_file = QAction(MainWindow)
        self.action_previous_file.setObjectName(u"action_previous_file")
        icon1 = QIcon()
        icon1.addFile(u":/icons/chevron-left.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_previous_file.setIcon(icon1)
        self.action_previous_file.setMenuRole(QAction.MenuRole.NoRole)
        self.action_next_file = QAction(MainWindow)
        self.action_next_file.setObjectName(u"action_next_file")
        icon2 = QIcon()
        icon2.addFile(u":/icons/chevron-right.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_next_file.setIcon(icon2)
        self.action_next_file.setMenuRole(QAction.MenuRole.NoRole)
        self.action_lock_palette = QAction(MainWindow)
        self.action_lock_palette.setObjectName(u"action_lock_palette")
        self.action_lock_palette.setCheckable(True)
        icon3 = QIcon()
        icon3.addFile(u":/icons/palette.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/world.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.action_lock_palette.setIcon(icon3)
        self.action_lock_palette.setMenuRole(QAction.MenuRole.NoRole)
        self.action_open_file = QAction(MainWindow)
        self.action_open_file.setObjectName(u"action_open_file")
        icon4 = QIcon()
        icon4.addFile(u":/icons/file.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_open_file.setIcon(icon4)
        self.action_open_file.setMenuRole(QAction.MenuRole.NoRole)
        self.action_refresh = QAction(MainWindow)
        self.action_refresh.setObjectName(u"action_refresh")
        icon5 = QIcon()
        icon5.addFile(u":/icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_refresh.setIcon(icon5)
        self.action_refresh.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_opened_file = QLabel(self.centralwidget)
        self.label_opened_file.setObjectName(u"label_opened_file")
        self.label_opened_file.setTextFormat(Qt.TextFormat.PlainText)

        self.verticalLayout.addWidget(self.label_opened_file)

        self.main_tabs = QTabWidget(self.centralwidget)
        self.main_tabs.setObjectName(u"main_tabs")
        self.tab_settings = QWidget()
        self.tab_settings.setObjectName(u"tab_settings")
        self.gridLayoutWidget = QWidget(self.tab_settings)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 421, 140))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.__img_output_dir_label = QLabel(self.gridLayoutWidget)
        self.__img_output_dir_label.setObjectName(u"__img_output_dir_label")

        self.gridLayout.addWidget(self.__img_output_dir_label, 2, 0, 1, 1)

        self.state_format_combo = QComboBox(self.gridLayoutWidget)
        self.state_format_combo.setObjectName(u"state_format_combo")

        self.gridLayout.addWidget(self.state_format_combo, 3, 1, 1, 1)

        self.__bg_color_override_label = QLabel(self.gridLayoutWidget)
        self.__bg_color_override_label.setObjectName(u"__bg_color_override_label")

        self.gridLayout.addWidget(self.__bg_color_override_label, 1, 0, 1, 1)

        self.bg_color_toggle = QCheckBox(self.gridLayoutWidget)
        self.bg_color_toggle.setObjectName(u"bg_color_toggle")

        self.gridLayout.addWidget(self.bg_color_toggle, 0, 1, 1, 1)

        self.bg_color_button = ColorButton(self.gridLayoutWidget)
        self.bg_color_button.setObjectName(u"bg_color_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_color_button.sizePolicy().hasHeightForWidth())
        self.bg_color_button.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.bg_color_button, 1, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.output_directory_line = QLineEdit(self.gridLayoutWidget)
        self.output_directory_line.setObjectName(u"output_directory_line")
        self.output_directory_line.setEnabled(False)

        self.horizontalLayout.addWidget(self.output_directory_line)

        self.output_select_button = QPushButton(self.gridLayoutWidget)
        self.output_select_button.setObjectName(u"output_select_button")
        self.output_select_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.output_select_button)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.__bg_color_toggle_label = QLabel(self.gridLayoutWidget)
        self.__bg_color_toggle_label.setObjectName(u"__bg_color_toggle_label")

        self.gridLayout.addWidget(self.__bg_color_toggle_label, 0, 0, 1, 1)

        self.__state_format = QLabel(self.gridLayoutWidget)
        self.__state_format.setObjectName(u"__state_format")

        self.gridLayout.addWidget(self.__state_format, 3, 0, 1, 1)

        self.default_config_button = QPushButton(self.gridLayoutWidget)
        self.default_config_button.setObjectName(u"default_config_button")
        self.default_config_button.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.default_config_button.sizePolicy().hasHeightForWidth())
        self.default_config_button.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.default_config_button, 4, 0, 1, 1)

        self.about_label = QLabel(self.tab_settings)
        self.about_label.setObjectName(u"about_label")
        self.about_label.setGeometry(QRect(10, 180, 421, 141))
        self.about_label.setFrameShape(QFrame.Shape.NoFrame)
        self.about_label.setFrameShadow(QFrame.Shadow.Plain)
        self.about_label.setTextFormat(Qt.TextFormat.PlainText)
        self.about_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.main_tabs.addTab(self.tab_settings, "")
        self.tab_palette = TabPalette()
        self.tab_palette.setObjectName(u"tab_palette")
        self.main_tabs.addTab(self.tab_palette, "")
        self.tab_vram = TabVram()
        self.tab_vram.setObjectName(u"tab_vram")
        self.main_tabs.addTab(self.tab_vram, "")
        self.tab_raw = TabRaw()
        self.tab_raw.setObjectName(u"tab_raw")
        self.main_tabs.addTab(self.tab_raw, "")
        self.tab_tilemap = TabTileMap()
        self.tab_tilemap.setObjectName(u"tab_tilemap")
        self.main_tabs.addTab(self.tab_tilemap, "")
        self.tab_hw_sprites = TabSprite()
        self.tab_hw_sprites.setObjectName(u"tab_hw_sprites")
        self.main_tabs.addTab(self.tab_hw_sprites, "")

        self.verticalLayout.addWidget(self.main_tabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setFloatable(True)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        QWidget.setTabOrder(self.main_tabs, self.bg_color_toggle)
        QWidget.setTabOrder(self.bg_color_toggle, self.bg_color_button)
        QWidget.setTabOrder(self.bg_color_button, self.output_directory_line)
        QWidget.setTabOrder(self.output_directory_line, self.output_select_button)
        QWidget.setTabOrder(self.output_select_button, self.state_format_combo)
        QWidget.setTabOrder(self.state_format_combo, self.default_config_button)

        self.toolBar.addAction(self.action_open_folder)
        self.toolBar.addAction(self.action_open_file)
        self.toolBar.addAction(self.action_previous_file)
        self.toolBar.addAction(self.action_next_file)
        self.toolBar.addAction(self.action_refresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_lock_palette)

        self.retranslateUi(MainWindow)

        self.main_tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_open_folder.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
#if QT_CONFIG(tooltip)
        self.action_open_folder.setToolTip(QCoreApplication.translate("MainWindow", u"Select save state folder", None))
#endif // QT_CONFIG(tooltip)
        self.action_previous_file.setText(QCoreApplication.translate("MainWindow", u"Previous File", None))
        self.action_next_file.setText(QCoreApplication.translate("MainWindow", u"Next File", None))
#if QT_CONFIG(tooltip)
        self.action_next_file.setToolTip(QCoreApplication.translate("MainWindow", u"Next File", None))
#endif // QT_CONFIG(tooltip)
        self.action_lock_palette.setText(QCoreApplication.translate("MainWindow", u"Swap Palette", None))
#if QT_CONFIG(tooltip)
        self.action_lock_palette.setToolTip(QCoreApplication.translate("MainWindow", u"Swap Palette", None))
#endif // QT_CONFIG(tooltip)
        self.action_open_file.setText(QCoreApplication.translate("MainWindow", u"Select File", None))
#if QT_CONFIG(tooltip)
        self.action_open_file.setToolTip(QCoreApplication.translate("MainWindow", u"Select Save State File", None))
#endif // QT_CONFIG(tooltip)
        self.action_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.label_opened_file.setText(QCoreApplication.translate("MainWindow", u"opened file label", None))
        self.__img_output_dir_label.setText(QCoreApplication.translate("MainWindow", u"Image Output Directory", None))
        self.__bg_color_override_label.setText(QCoreApplication.translate("MainWindow", u"Override Color", None))
        self.bg_color_toggle.setText("")
        self.bg_color_button.setText("")
        self.output_directory_line.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.output_select_button.setToolTip(QCoreApplication.translate("MainWindow", u"Select Directory", None))
#endif // QT_CONFIG(tooltip)
        self.output_select_button.setText("")
        self.__bg_color_toggle_label.setText(QCoreApplication.translate("MainWindow", u"Override Background Color", None))
        self.__state_format.setText(QCoreApplication.translate("MainWindow", u"Save State Format", None))
        self.default_config_button.setText(QCoreApplication.translate("MainWindow", u"Restore Defaults", None))
        self.about_label.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_settings), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_palette), QCoreApplication.translate("MainWindow", u"Palette", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_vram), QCoreApplication.translate("MainWindow", u"VRAM", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_raw), QCoreApplication.translate("MainWindow", u"RAW Tiles", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_tilemap), QCoreApplication.translate("MainWindow", u"Tile Maps", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_hw_sprites), QCoreApplication.translate("MainWindow", u"Sprites", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

