# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#

#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from qt import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 336)
        MainWindow.setMinimumSize(QtCore.QSize(550, 336))
        MainWindow.setMaximumSize(QtCore.QSize(550, 336))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sidebarLogo = QtGui.QLabel(self.centralWidget)
        self.sidebarLogo.setPixmap(QtGui.QPixmap(":/sidebar.png"))
        self.sidebarLogo.setObjectName("sidebarLogo")
        self.horizontalLayout.addWidget(self.sidebarLogo)
        self.pageLayout = QtGui.QVBoxLayout()
        self.pageLayout.setMargin(9)
        self.pageLayout.setObjectName("pageLayout")
        self.createButton = QtGui.QCommandLinkButton(self.centralWidget)
        self.createButton.setObjectName("createButton")
        self.pageLayout.addWidget(self.createButton)
        self.line = QtGui.QFrame(self.centralWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pageLayout.addWidget(self.line)
        self.packageLayout = QtGui.QHBoxLayout()
        self.packageLayout.setObjectName("packageLayout")
        self.packageLabel = QtGui.QLabel(self.centralWidget)
        self.packageLabel.setObjectName("packageLabel")
        self.packageLayout.addWidget(self.packageLabel)
        self.packageText = QtGui.QLineEdit(self.centralWidget)
        self.packageText.setObjectName("packageText")
        self.packageLayout.addWidget(self.packageText)
        self.packageButton = QtGui.QPushButton(self.centralWidget)
        self.packageButton.setObjectName("packageButton")
        self.packageLayout.addWidget(self.packageButton)
        self.pageLayout.addLayout(self.packageLayout)
        self.detailsButton = QtGui.QCommandLinkButton(self.centralWidget)
        self.detailsButton.setObjectName("detailsButton")
        self.pageLayout.addWidget(self.detailsButton)
        self.validateButton = QtGui.QCommandLinkButton(self.centralWidget)
        self.validateButton.setObjectName("validateButton")
        self.pageLayout.addWidget(self.validateButton)
        self.installerButton = QtGui.QCommandLinkButton(self.centralWidget)
        self.installerButton.setObjectName("installerButton")
        self.pageLayout.addWidget(self.installerButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.pageLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.pageLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.packageLabel.setBuddy(self.packageText)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PortableApps.com Development Toolkit", None, QtGui.QApplication.UnicodeUTF8))
        self.createButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Start a new portable app package", None, QtGui.QApplication.UnicodeUTF8))
        self.createButton.setText(QtGui.QApplication.translate("MainWindow", "&Create a new portable app...", None, QtGui.QApplication.UnicodeUTF8))
        self.createButton.setDescription(QtGui.QApplication.translate("MainWindow", "Start a new portable app package here", None, QtGui.QApplication.UnicodeUTF8))
        self.packageLabel.setText(QtGui.QApplication.translate("MainWindow", "&Package:", None, QtGui.QApplication.UnicodeUTF8))
        self.packageButton.setText(QtGui.QApplication.translate("MainWindow", "&Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.detailsButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Edit the basic app details", None, QtGui.QApplication.UnicodeUTF8))
        self.detailsButton.setText(QtGui.QApplication.translate("MainWindow", "Edit &details", None, QtGui.QApplication.UnicodeUTF8))
        self.detailsButton.setDescription(QtGui.QApplication.translate("MainWindow", "Edit the basic app details", None, QtGui.QApplication.UnicodeUTF8))
        self.validateButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Validate PortableApps.com Format compliance", None, QtGui.QApplication.UnicodeUTF8))
        self.validateButton.setText(QtGui.QApplication.translate("MainWindow", "&Validate", None, QtGui.QApplication.UnicodeUTF8))
        self.validateButton.setDescription(QtGui.QApplication.translate("MainWindow", "Validate the app", None, QtGui.QApplication.UnicodeUTF8))
        self.installerButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Generate your installer", None, QtGui.QApplication.UnicodeUTF8))
        self.installerButton.setText(QtGui.QApplication.translate("MainWindow", "PortableApps.com &Installer", None, QtGui.QApplication.UnicodeUTF8))
        self.installerButton.setDescription(QtGui.QApplication.translate("MainWindow", "Generate your installer", None, QtGui.QApplication.UnicodeUTF8))

import graphics_rc
