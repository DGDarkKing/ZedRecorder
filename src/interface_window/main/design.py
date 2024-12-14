# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(719, 662)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Btn_OpenCamera = QPushButton(self.centralwidget)
        self.Btn_OpenCamera.setObjectName(u"Btn_OpenCamera")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_OpenCamera.sizePolicy().hasHeightForWidth())
        self.Btn_OpenCamera.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.Btn_OpenCamera)

        self.Btn_CloseCamera = QPushButton(self.centralwidget)
        self.Btn_CloseCamera.setObjectName(u"Btn_CloseCamera")
        sizePolicy.setHeightForWidth(self.Btn_CloseCamera.sizePolicy().hasHeightForWidth())
        self.Btn_CloseCamera.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.Btn_CloseCamera)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboBox_Resolution = QComboBox(self.centralwidget)
        self.comboBox_Resolution.setObjectName(u"comboBox_Resolution")
        self.comboBox_Resolution.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.comboBox_Resolution)

        self.comboBox_FPS = QComboBox(self.centralwidget)
        self.comboBox_FPS.setObjectName(u"comboBox_FPS")
        self.comboBox_FPS.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.comboBox_FPS)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.Label_VideoName = QLabel(self.centralwidget)
        self.Label_VideoName.setObjectName(u"Label_VideoName")
        sizePolicy.setHeightForWidth(self.Label_VideoName.sizePolicy().hasHeightForWidth())
        self.Label_VideoName.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.Label_VideoName.setFont(font)

        self.verticalLayout.addWidget(self.Label_VideoName)

        self.ManualVideoWidget = QWidget(self.centralwidget)
        self.ManualVideoWidget.setObjectName(u"ManualVideoWidget")
        self.ManualVideoWidget.setMinimumSize(QSize(480, 480))
        self.ManualVideoWidget.setAutoFillBackground(False)
        self.ManualVideoWidget.setStyleSheet(u"background: rgb(0, 0, 0)")

        self.verticalLayout.addWidget(self.ManualVideoWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.BTN_StartRecord = QPushButton(self.centralwidget)
        self.BTN_StartRecord.setObjectName(u"BTN_StartRecord")
        self.BTN_StartRecord.setEnabled(True)
        sizePolicy.setHeightForWidth(self.BTN_StartRecord.sizePolicy().hasHeightForWidth())
        self.BTN_StartRecord.setSizePolicy(sizePolicy)
        self.BTN_StartRecord.setMinimumSize(QSize(80, 80))
        self.BTN_StartRecord.setMaximumSize(QSize(80, 80))
        self.BTN_StartRecord.setBaseSize(QSize(80, 80))
        self.BTN_StartRecord.setAcceptDrops(False)
        self.BTN_StartRecord.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"../../../../Work/Prog/Rehabilitation/ScoreService/DesktopUi/icons/btn_play.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.BTN_StartRecord.setIcon(icon)
        self.BTN_StartRecord.setIconSize(QSize(96, 96))
        self.BTN_StartRecord.setCheckable(False)
        self.BTN_StartRecord.setAutoDefault(False)
        self.BTN_StartRecord.setFlat(True)

        self.horizontalLayout_2.addWidget(self.BTN_StartRecord)

        self.BTN_FinishRecord = QPushButton(self.centralwidget)
        self.BTN_FinishRecord.setObjectName(u"BTN_FinishRecord")
        self.BTN_FinishRecord.setEnabled(False)
        sizePolicy.setHeightForWidth(self.BTN_FinishRecord.sizePolicy().hasHeightForWidth())
        self.BTN_FinishRecord.setSizePolicy(sizePolicy)
        self.BTN_FinishRecord.setMinimumSize(QSize(80, 80))
        self.BTN_FinishRecord.setMaximumSize(QSize(80, 80))
        icon1 = QIcon()
        icon1.addFile(u"../../../../Work/Prog/Rehabilitation/ScoreService/DesktopUi/icons/btn_stop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.BTN_FinishRecord.setIcon(icon1)
        self.BTN_FinishRecord.setIconSize(QSize(96, 96))
        self.BTN_FinishRecord.setFlat(True)

        self.horizontalLayout_2.addWidget(self.BTN_FinishRecord)

        self.BTN_PauseRecord = QPushButton(self.centralwidget)
        self.BTN_PauseRecord.setObjectName(u"BTN_PauseRecord")
        self.BTN_PauseRecord.setEnabled(False)
        sizePolicy.setHeightForWidth(self.BTN_PauseRecord.sizePolicy().hasHeightForWidth())
        self.BTN_PauseRecord.setSizePolicy(sizePolicy)
        self.BTN_PauseRecord.setMinimumSize(QSize(80, 80))
        self.BTN_PauseRecord.setMaximumSize(QSize(80, 80))
        icon2 = QIcon()
        icon2.addFile(u"../../../../Work/Prog/Rehabilitation/ScoreService/DesktopUi/icons/btn_pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.BTN_PauseRecord.setIcon(icon2)
        self.BTN_PauseRecord.setIconSize(QSize(96, 96))
        self.BTN_PauseRecord.setFlat(True)

        self.horizontalLayout_2.addWidget(self.BTN_PauseRecord)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.BTN_StartRecord.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Btn_OpenCamera.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043a\u0430\u043c\u0435\u0440\u0443", None))
        self.Btn_CloseCamera.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c \u043a\u0430\u043c\u0435\u0440\u0443", None))
        self.Label_VideoName.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.BTN_StartRecord.setText("")
        self.BTN_FinishRecord.setText("")
        self.BTN_PauseRecord.setText("")
    # retranslateUi

