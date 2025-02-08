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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableView,
    QWidget)

class Ui_TabSprite(object):
    def setupUi(self, TabSprite):
        if not TabSprite.objectName():
            TabSprite.setObjectName(u"TabSprite")
        TabSprite.resize(610, 484)
        self.sprite_view = QTableView(TabSprite)
        self.sprite_view.setObjectName(u"sprite_view")
        self.sprite_view.setGeometry(QRect(10, 10, 581, 411))

        self.retranslateUi(TabSprite)

        QMetaObject.connectSlotsByName(TabSprite)
    # setupUi

    def retranslateUi(self, TabSprite):
        TabSprite.setWindowTitle(QCoreApplication.translate("TabSprite", u"Form", None))
    # retranslateUi

