# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/pageoptions.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageOptions(object):
    def setupUi(self, PageOptions):
        PageOptions.setObjectName("PageOptions")
        PageOptions.resize(960, 445)
        self.gridLayout = QtGui.QGridLayout(PageOptions)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 2, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 4, 2, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 3)
        self.installer_label = QtGui.QLabel(PageOptions)
        self.installer_label.setObjectName("installer_label")
        self.gridLayout.addWidget(self.installer_label, 1, 1, 1, 1)
        self.launcher_label = QtGui.QLabel(PageOptions)
        self.launcher_label.setObjectName("launcher_label")
        self.gridLayout.addWidget(self.launcher_label, 2, 1, 1, 1)
        self.appcompactor_label = QtGui.QLabel(PageOptions)
        self.appcompactor_label.setObjectName("appcompactor_label")
        self.gridLayout.addWidget(self.appcompactor_label, 3, 1, 1, 1)
        self.installer = QtGui.QLineEdit(PageOptions)
        self.installer.setMinimumSize(QtCore.QSize(400, 0))
        self.installer.setObjectName("installer")
        self.gridLayout.addWidget(self.installer, 1, 2, 1, 1)
        self.launcher = QtGui.QLineEdit(PageOptions)
        self.launcher.setMinimumSize(QtCore.QSize(400, 0))
        self.launcher.setObjectName("launcher")
        self.gridLayout.addWidget(self.launcher, 2, 2, 1, 1)
        self.appcompactor = QtGui.QLineEdit(PageOptions)
        self.appcompactor.setMinimumSize(QtCore.QSize(400, 0))
        self.appcompactor.setObjectName("appcompactor")
        self.gridLayout.addWidget(self.appcompactor, 3, 2, 1, 1)
        self.installer_browse = QtGui.QPushButton(PageOptions)
        self.installer_browse.setObjectName("installer_browse")
        self.gridLayout.addWidget(self.installer_browse, 1, 3, 1, 1)
        self.launcher_browse = QtGui.QPushButton(PageOptions)
        self.launcher_browse.setObjectName("launcher_browse")
        self.gridLayout.addWidget(self.launcher_browse, 2, 3, 1, 1)
        self.appcompactor_browse = QtGui.QPushButton(PageOptions)
        self.appcompactor_browse.setObjectName("appcompactor_browse")
        self.gridLayout.addWidget(self.appcompactor_browse, 3, 3, 1, 1)
        self.installer_label.setBuddy(self.installer)
        self.launcher_label.setBuddy(self.launcher)
        self.appcompactor_label.setBuddy(self.appcompactor)

        self.retranslateUi(PageOptions)
        QtCore.QMetaObject.connectSlotsByName(PageOptions)

    def retranslateUi(self, PageOptions):
        self.installer_label.setText(QtGui.QApplication.translate("PageOptions", "PortableApps.com &Installer path:", None, QtGui.QApplication.UnicodeUTF8))
        self.launcher_label.setText(QtGui.QApplication.translate("PageOptions", "PortableApps.com &Launcher path:", None, QtGui.QApplication.UnicodeUTF8))
        self.appcompactor_label.setText(QtGui.QApplication.translate("PageOptions", "PortableApps.com &AppCompactor path:", None, QtGui.QApplication.UnicodeUTF8))
        self.installer_browse.setText(QtGui.QApplication.translate("PageOptions", "&Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.launcher_browse.setText(QtGui.QApplication.translate("PageOptions", "B&rowse...", None, QtGui.QApplication.UnicodeUTF8))
        self.appcompactor_browse.setText(QtGui.QApplication.translate("PageOptions", "Br&owse...", None, QtGui.QApplication.UnicodeUTF8))

