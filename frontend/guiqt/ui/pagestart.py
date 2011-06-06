# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/guiqt/ui/pagestart.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageStart(object):
    def setupUi(self, pagestart):
        pagestart.setObjectName("pagestart")
        pagestart.setGeometry(QtCore.QRect(0, 0, 960, 445))
        self.gridLayout = QtGui.QGridLayout(pagestart)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.content_box = QtGui.QVBoxLayout()
        self.content_box.setSpacing(40)
        self.content_box.setObjectName("content_box")
        self.label = QtGui.QLabel(pagestart)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.content_box.addWidget(self.label)
        self.open_groupbox = QtGui.QGroupBox(pagestart)
        self.open_groupbox.setObjectName("open_groupbox")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.open_groupbox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.open_label = QtGui.QLabel(self.open_groupbox)
        self.open_label.setObjectName("open_label")
        self.horizontalLayout_2.addWidget(self.open_label)
        self.open = QtGui.QLineEdit(self.open_groupbox)
        self.open.setMinimumSize(QtCore.QSize(400, 0))
        self.open.setObjectName("open")
        self.horizontalLayout_2.addWidget(self.open)
        self.open_browse = QtGui.QPushButton(self.open_groupbox)
        self.open_browse.setObjectName("open_browse")
        self.horizontalLayout_2.addWidget(self.open_browse)
        self.content_box.addWidget(self.open_groupbox)
        self.create_groupbox = QtGui.QGroupBox(pagestart)
        self.create_groupbox.setObjectName("create_groupbox")
        self.hboxlayout = QtGui.QHBoxLayout(self.create_groupbox)
        self.hboxlayout.setObjectName("hboxlayout")
        self.create_label = QtGui.QLabel(self.create_groupbox)
        self.create_label.setObjectName("create_label")
        self.hboxlayout.addWidget(self.create_label)
        self.create = QtGui.QLineEdit(self.create_groupbox)
        self.create.setMinimumSize(QtCore.QSize(400, 0))
        self.create.setObjectName("create")
        self.hboxlayout.addWidget(self.create)
        self.create_browse = QtGui.QPushButton(self.create_groupbox)
        self.create_browse.setObjectName("create_browse")
        self.hboxlayout.addWidget(self.create_browse)
        self.create_button = QtGui.QPushButton(self.create_groupbox)
        self.create_button.setAutoDefault(True)
        self.create_button.setDefault(True)
        self.create_button.setObjectName("create_button")
        self.hboxlayout.addWidget(self.create_button)
        self.content_box.addWidget(self.create_groupbox)
        self.gridLayout.addLayout(self.content_box, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        self.open_label.setBuddy(self.open)
        self.create_label.setBuddy(self.create)

        self.retranslateUi(pagestart)
        QtCore.QMetaObject.connectSlotsByName(pagestart)

    def retranslateUi(self, pagestart):
        self.label.setText(QtGui.QApplication.translate("PageStart", "I want to...", None, QtGui.QApplication.UnicodeUTF8))
        self.open_groupbox.setTitle(QtGui.QApplication.translate("PageStart", "Open an existing package", None, QtGui.QApplication.UnicodeUTF8))
        self.open_label.setText(QtGui.QApplication.translate("PageStart", "&Path:", None, QtGui.QApplication.UnicodeUTF8))
        self.open_browse.setText(QtGui.QApplication.translate("PageStart", "&Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.create_groupbox.setTitle(QtGui.QApplication.translate("PageStart", "Create a new portable app", None, QtGui.QApplication.UnicodeUTF8))
        self.create_label.setText(QtGui.QApplication.translate("PageStart", "P&ath:", None, QtGui.QApplication.UnicodeUTF8))
        self.create_browse.setText(QtGui.QApplication.translate("PageStart", "B&rowse...", None, QtGui.QApplication.UnicodeUTF8))
        self.create_button.setText(QtGui.QApplication.translate("PageStart", "Create", None, QtGui.QApplication.UnicodeUTF8))

