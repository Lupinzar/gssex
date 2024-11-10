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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QSizePolicy,
    QStatusBar, QTabWidget, QToolBar, QVBoxLayout,
    QWidget)
from . import resource_rc

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
        icon3.addFile(u":/icons/lock-open-2.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/lock.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.action_lock_palette.setIcon(icon3)
        self.action_lock_palette.setMenuRole(QAction.MenuRole.NoRole)
        self.action_open_file = QAction(MainWindow)
        self.action_open_file.setObjectName(u"action_open_file")
        icon4 = QIcon()
        icon4.addFile(u":/icons/file.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_open_file.setIcon(icon4)
        self.action_open_file.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_opened_file = QLabel(self.centralwidget)
        self.label_opened_file.setObjectName(u"label_opened_file")
        self.label_opened_file.setTextFormat(Qt.TextFormat.PlainText)

        self.verticalLayout.addWidget(self.label_opened_file)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_settings = QWidget()
        self.tab_settings.setObjectName(u"tab_settings")
        self.tabWidget.addTab(self.tab_settings, "")
        self.tab_palette = QWidget()
        self.tab_palette.setObjectName(u"tab_palette")
        self.tabWidget.addTab(self.tab_palette, "")
        self.tab_layers = QWidget()
        self.tab_layers.setObjectName(u"tab_layers")
        self.tabWidget.addTab(self.tab_layers, "")
        self.tab_hw_sprites = QWidget()
        self.tab_hw_sprites.setObjectName(u"tab_hw_sprites")
        self.tabWidget.addTab(self.tab_hw_sprites, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setFloatable(True)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_open_folder)
        self.toolBar.addAction(self.action_open_file)
        self.toolBar.addAction(self.action_previous_file)
        self.toolBar.addAction(self.action_next_file)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_lock_palette)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


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
        self.action_lock_palette.setText(QCoreApplication.translate("MainWindow", u"Lock Palette", None))
#if QT_CONFIG(tooltip)
        self.action_lock_palette.setToolTip(QCoreApplication.translate("MainWindow", u"Lock Palette", None))
#endif // QT_CONFIG(tooltip)
        self.action_open_file.setText(QCoreApplication.translate("MainWindow", u"Select File", None))
#if QT_CONFIG(tooltip)
        self.action_open_file.setToolTip(QCoreApplication.translate("MainWindow", u"Select Save State File", None))
#endif // QT_CONFIG(tooltip)
        self.label_opened_file.setText(QCoreApplication.translate("MainWindow", u"opened file label", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_palette), QCoreApplication.translate("MainWindow", u"Palette", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_layers), QCoreApplication.translate("MainWindow", u"Layers", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_hw_sprites), QCoreApplication.translate("MainWindow", u"Hardware Sprites", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

