# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(590, 692)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 210, 121, 16))
        self.geschwindigkeit = QLineEdit(self.centralwidget)
        self.geschwindigkeit.setObjectName(u"geschwindigkeit")
        self.geschwindigkeit.setGeometry(QRect(150, 210, 61, 21))
        self.geschwindigkeit.setReadOnly(True)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 240, 101, 16))
        self.druckhll = QLineEdit(self.centralwidget)
        self.druckhll.setObjectName(u"druckhll")
        self.druckhll.setGeometry(QRect(150, 240, 201, 21))
        self.druckhll.setReadOnly(True)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 300, 171, 121))
        self.lm_u = QLabel(self.groupBox)
        self.lm_u.setObjectName(u"lm_u")
        self.lm_u.setGeometry(QRect(10, 10, 51, 51))
        self.lm_u.setAutoFillBackground(False)
        self.lm_u.setStyleSheet(u"background-color: blue;")
        self.lm_u.setAlignment(Qt.AlignCenter)
        self.lm_m = QLabel(self.groupBox)
        self.lm_m.setObjectName(u"lm_m")
        self.lm_m.setGeometry(QRect(60, 10, 51, 51))
        self.lm_m.setAutoFillBackground(False)
        self.lm_m.setStyleSheet(u"background-color: blue;")
        self.lm_m.setAlignment(Qt.AlignCenter)
        self.lm_o = QLabel(self.groupBox)
        self.lm_o.setObjectName(u"lm_o")
        self.lm_o.setGeometry(QRect(110, 10, 51, 51))
        self.lm_o.setAutoFillBackground(False)
        self.lm_o.setStyleSheet(u"background-color: blue;")
        self.lm_o.setAlignment(Qt.AlignCenter)
        self.lm_40 = QLabel(self.groupBox)
        self.lm_40.setObjectName(u"lm_40")
        self.lm_40.setGeometry(QRect(10, 60, 51, 51))
        self.lm_40.setAutoFillBackground(False)
        self.lm_40.setStyleSheet(u"background-color: black")
        self.lm_40.setAlignment(Qt.AlignCenter)
        self.lm_500 = QLabel(self.groupBox)
        self.lm_500.setObjectName(u"lm_500")
        self.lm_500.setGeometry(QRect(60, 60, 51, 51))
        self.lm_500.setAutoFillBackground(False)
        self.lm_500.setStyleSheet(u"background-color: red;")
        self.lm_500.setAlignment(Qt.AlignCenter)
        self.lm_1000 = QLabel(self.groupBox)
        self.lm_1000.setObjectName(u"lm_1000")
        self.lm_1000.setGeometry(QRect(110, 60, 51, 51))
        self.lm_1000.setAutoFillBackground(False)
        self.lm_1000.setStyleSheet(u"background-color: yellow;")
        self.lm_1000.setAlignment(Qt.AlignCenter)
        self.lm_sifa = QLabel(self.centralwidget)
        self.lm_sifa.setObjectName(u"lm_sifa")
        self.lm_sifa.setGeometry(QRect(230, 310, 51, 51))
        self.lm_sifa.setAutoFillBackground(False)
        self.lm_sifa.setStyleSheet(u"background-color: gray;")
        self.lm_sifa.setAlignment(Qt.AlignCenter)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(30, 440, 91, 16))
        self.indusistatus = QLineEdit(self.centralwidget)
        self.indusistatus.setObjectName(u"indusistatus")
        self.indusistatus.setGeometry(QRect(150, 440, 201, 21))
        self.indusistatus.setAlignment(Qt.AlignCenter)
        self.indusistatus.setReadOnly(True)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(30, 510, 111, 16))
        self.sifastatus = QLineEdit(self.centralwidget)
        self.sifastatus.setObjectName(u"sifastatus")
        self.sifastatus.setGeometry(QRect(150, 510, 201, 21))
        self.sifastatus.setAlignment(Qt.AlignCenter)
        self.sifastatus.setReadOnly(True)
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(30, 180, 121, 16))
        self.uhrzeit = QLineEdit(self.centralwidget)
        self.uhrzeit.setObjectName(u"uhrzeit")
        self.uhrzeit.setGeometry(QRect(150, 180, 201, 21))
        self.uhrzeit.setReadOnly(True)
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(30, 540, 111, 16))
        self.nbuestatus = QLineEdit(self.centralwidget)
        self.nbuestatus.setObjectName(u"nbuestatus")
        self.nbuestatus.setGeometry(QRect(150, 540, 201, 21))
        self.nbuestatus.setAlignment(Qt.AlignCenter)
        self.nbuestatus.setReadOnly(True)
        self.sifabauart = QLineEdit(self.centralwidget)
        self.sifabauart.setObjectName(u"sifabauart")
        self.sifabauart.setGeometry(QRect(360, 510, 211, 21))
        self.sifabauart.setAlignment(Qt.AlignCenter)
        self.sifabauart.setReadOnly(True)
        self.indusibauart = QLineEdit(self.centralwidget)
        self.indusibauart.setObjectName(u"indusibauart")
        self.indusibauart.setGeometry(QRect(360, 440, 211, 21))
        self.indusibauart.setAlignment(Qt.AlignCenter)
        self.indusibauart.setReadOnly(True)
        self.nbuebauart = QLineEdit(self.centralwidget)
        self.nbuebauart.setObjectName(u"nbuebauart")
        self.nbuebauart.setGeometry(QRect(360, 540, 211, 21))
        self.nbuebauart.setAlignment(Qt.AlignCenter)
        self.nbuebauart.setReadOnly(True)
        self.indusizwangsbremsung = QLineEdit(self.centralwidget)
        self.indusizwangsbremsung.setObjectName(u"indusizwangsbremsung")
        self.indusizwangsbremsung.setGeometry(QRect(150, 470, 201, 21))
        self.indusizwangsbremsung.setAlignment(Qt.AlignCenter)
        self.indusizwangsbremsung.setReadOnly(True)
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(30, 470, 111, 16))
        self.indusizusatzinfo = QLineEdit(self.centralwidget)
        self.indusizusatzinfo.setObjectName(u"indusizusatzinfo")
        self.indusizusatzinfo.setGeometry(QRect(360, 470, 211, 21))
        self.indusizusatzinfo.setAlignment(Qt.AlignCenter)
        self.indusizusatzinfo.setReadOnly(True)
        self.sollgeschwindigkeit = QLineEdit(self.centralwidget)
        self.sollgeschwindigkeit.setObjectName(u"sollgeschwindigkeit")
        self.sollgeschwindigkeit.setGeometry(QRect(270, 210, 81, 21))
        self.sollgeschwindigkeit.setReadOnly(True)
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(30, 590, 111, 16))
        self.tuerenlinks = QLineEdit(self.centralwidget)
        self.tuerenlinks.setObjectName(u"tuerenlinks")
        self.tuerenlinks.setGeometry(QRect(150, 590, 201, 21))
        self.tuerenlinks.setAlignment(Qt.AlignCenter)
        self.tuerenlinks.setReadOnly(True)
        self.tuerenrechts = QLineEdit(self.centralwidget)
        self.tuerenrechts.setObjectName(u"tuerenrechts")
        self.tuerenrechts.setGeometry(QRect(360, 590, 211, 21))
        self.tuerenrechts.setAlignment(Qt.AlignCenter)
        self.tuerenrechts.setReadOnly(True)
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(30, 20, 121, 16))
        self.zusi_ip = QLineEdit(self.centralwidget)
        self.zusi_ip.setObjectName(u"zusi_ip")
        self.zusi_ip.setGeometry(QRect(150, 20, 151, 21))
        self.connectButton = QPushButton(self.centralwidget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(330, 10, 100, 41))
        self.zugnummer = QLineEdit(self.centralwidget)
        self.zugnummer.setObjectName(u"zugnummer")
        self.zugnummer.setGeometry(QRect(150, 100, 201, 21))
        self.zugnummer.setReadOnly(True)
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(30, 100, 121, 16))
        self.fahrplan = QLineEdit(self.centralwidget)
        self.fahrplan.setObjectName(u"fahrplan")
        self.fahrplan.setGeometry(QRect(30, 70, 531, 21))
        self.fahrplan.setReadOnly(True)
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(30, 50, 121, 16))
        self.ladezustand = QLineEdit(self.centralwidget)
        self.ladezustand.setObjectName(u"ladezustand")
        self.ladezustand.setGeometry(QRect(150, 130, 201, 21))
        self.ladezustand.setReadOnly(True)
        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(30, 130, 121, 16))
        self.bremsdruck = QLineEdit(self.centralwidget)
        self.bremsdruck.setObjectName(u"bremsdruck")
        self.bremsdruck.setGeometry(QRect(150, 270, 201, 21))
        self.bremsdruck.setReadOnly(True)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 270, 101, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(230, 210, 51, 16))
        self.sollgeschwindigkeit_check = QCheckBox(self.centralwidget)
        self.sollgeschwindigkeit_check.setObjectName(u"sollgeschwindigkeit_check")
        self.sollgeschwindigkeit_check.setGeometry(QRect(360, 210, 85, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 590, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ZusiData", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Geschwindigkeit:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Druck HLL:", None))
        self.groupBox.setTitle("")
        self.lm_u.setText(QCoreApplication.translate("MainWindow", u"55", None))
        self.lm_m.setText(QCoreApplication.translate("MainWindow", u"70", None))
        self.lm_o.setText(QCoreApplication.translate("MainWindow", u"85", None))
        self.lm_40.setText(QCoreApplication.translate("MainWindow", u"Befehl\n"
"40", None))
        self.lm_500.setText(QCoreApplication.translate("MainWindow", u"500Hz", None))
        self.lm_1000.setText(QCoreApplication.translate("MainWindow", u"1000Hz", None))
        self.lm_sifa.setText(QCoreApplication.translate("MainWindow", u"Sifa", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Indusi Status:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Sifa Status:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Uhrzeit:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Notbremsstatus:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Zwangsbremsung:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"T\u00fcrstatus:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Zusi IP", None))
        self.zusi_ip.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Zugnummer:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Fahrplan:", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Ladezustand:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Bremsdruck:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Max:", None))
        self.sollgeschwindigkeit_check.setText(QCoreApplication.translate("MainWindow", u"zeigen", None))
    # retranslateUi

