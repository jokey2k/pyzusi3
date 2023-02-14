# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)
import form_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(364, 195)
        icon = QIcon()
        icon.addFile(u":/icons/appicon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lm_sifa = QLabel(self.centralwidget)
        self.lm_sifa.setObjectName(u"lm_sifa")
        self.lm_sifa.setGeometry(QRect(300, 40, 51, 51))
        self.lm_sifa.setAutoFillBackground(False)
        self.lm_sifa.setStyleSheet(u"background-color: gray;")
        self.lm_sifa.setAlignment(Qt.AlignCenter)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 70, 111, 16))
        self.sifastatus = QLineEdit(self.centralwidget)
        self.sifastatus.setObjectName(u"sifastatus")
        self.sifastatus.setGeometry(QRect(80, 70, 211, 21))
        self.sifastatus.setAlignment(Qt.AlignCenter)
        self.sifastatus.setReadOnly(True)
        self.sifabauart = QLineEdit(self.centralwidget)
        self.sifabauart.setObjectName(u"sifabauart")
        self.sifabauart.setGeometry(QRect(80, 40, 211, 21))
        self.sifabauart.setAlignment(Qt.AlignCenter)
        self.sifabauart.setReadOnly(True)
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(10, 10, 121, 16))
        self.zusi_ip = QLineEdit(self.centralwidget)
        self.zusi_ip.setObjectName(u"zusi_ip")
        self.zusi_ip.setGeometry(QRect(80, 10, 171, 21))
        self.connectButton = QPushButton(self.centralwidget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(270, 10, 81, 21))
        self.autosifa_check = QCheckBox(self.centralwidget)
        self.autosifa_check.setObjectName(u"autosifa_check")
        self.autosifa_check.setGeometry(QRect(10, 100, 151, 20))
        self.autosifastatus = QLineEdit(self.centralwidget)
        self.autosifastatus.setObjectName(u"autosifastatus")
        self.autosifastatus.setGeometry(QRect(10, 130, 341, 21))
        self.autosifastatus.setAlignment(Qt.AlignCenter)
        self.autosifastatus.setReadOnly(True)
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 40, 111, 16))
        self.autosifa_invers = QCheckBox(self.centralwidget)
        self.autosifa_invers.setObjectName(u"autosifa_invers")
        self.autosifa_invers.setGeometry(QRect(170, 100, 151, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 364, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Zusi 3 AutoSifa", None))
        self.lm_sifa.setText(QCoreApplication.translate("MainWindow", u"Sifa", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Sifa Status:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Zusi IP", None))
        self.zusi_ip.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Verbinden", None))
        self.autosifa_check.setText(QCoreApplication.translate("MainWindow", u"Auto-Sifa", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Sifa Bauart:", None))
        self.autosifa_invers.setText(QCoreApplication.translate("MainWindow", u"Pedal invertiert", None))
    # retranslateUi

