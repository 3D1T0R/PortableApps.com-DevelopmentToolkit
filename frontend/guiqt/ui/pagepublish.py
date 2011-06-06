# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/guiqt/ui/pagepublish.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PagePublish(object):
    def setupUi(self, pagepublish):
        pagepublish.setObjectName("pagepublish")
        pagepublish.setGeometry(QtCore.QRect(0, 0, 960, 445))
        self.gridLayout = QtGui.QGridLayout(pagepublish)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        self.build_installer = QtGui.QCommandLinkButton(pagepublish)
        self.build_installer.setObjectName("build_installer")
        self.gridLayout.addWidget(self.build_installer, 1, 1, 1, 1)
        self.results_groupbox = QtGui.QGroupBox(pagepublish)
        self.results_groupbox.setEnabled(False)
        self.results_groupbox.setObjectName("results_groupbox")
        self.formLayout_6 = QtGui.QFormLayout(self.results_groupbox)
        self.formLayout_6.setObjectName("formLayout_6")
        self.filename_label = QtGui.QLabel(self.results_groupbox)
        self.filename_label.setObjectName("filename_label")
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.filename_label)
        self.filename = QtGui.QLineEdit(self.results_groupbox)
        self.filename.setMinimumSize(QtCore.QSize(300, 0))
        self.filename.setReadOnly(True)
        self.filename.setObjectName("filename")
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.filename)
        self.size_label = QtGui.QLabel(self.results_groupbox)
        self.size_label.setObjectName("size_label")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.size_label)
        self.size = QtGui.QLineEdit(self.results_groupbox)
        self.size.setReadOnly(True)
        self.size.setObjectName("size")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.size)
        self.installed_size_label = QtGui.QLabel(self.results_groupbox)
        self.installed_size_label.setObjectName("installed_size_label")
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.LabelRole, self.installed_size_label)
        self.size_installed = QtGui.QLineEdit(self.results_groupbox)
        self.size_installed.setReadOnly(True)
        self.size_installed.setObjectName("size_installed")
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.FieldRole, self.size_installed)
        self.md5_label = QtGui.QLabel(self.results_groupbox)
        self.md5_label.setObjectName("md5_label")
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.LabelRole, self.md5_label)
        self.md5 = QtGui.QLineEdit(self.results_groupbox)
        self.md5.setReadOnly(True)
        self.md5.setObjectName("md5")
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.FieldRole, self.md5)
        self.gridLayout.addWidget(self.results_groupbox, 2, 1, 1, 1)
        self.upload_groupbox = QtGui.QGroupBox(pagepublish)
        self.upload_groupbox.setEnabled(False)
        self.upload_groupbox.setObjectName("upload_groupbox")
        self.gridLayout_3 = QtGui.QGridLayout(self.upload_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.upload_to_label = QtGui.QLabel(self.upload_groupbox)
        self.upload_to_label.setObjectName("upload_to_label")
        self.gridLayout_3.addWidget(self.upload_to_label, 0, 0, 1, 1)
        self.upload_to = QtGui.QComboBox(self.upload_groupbox)
        self.upload_to.setObjectName("upload_to")
        self.upload_to.addItem("")
        self.upload_to.addItem("")
        self.gridLayout_3.addWidget(self.upload_to, 0, 1, 1, 2)
        self.configure_upload_targets = QtGui.QPushButton(self.upload_groupbox)
        self.configure_upload_targets.setObjectName("configure_upload_targets")
        self.gridLayout_3.addWidget(self.configure_upload_targets, 1, 2, 1, 1)
        self.upload_button = QtGui.QPushButton(self.upload_groupbox)
        self.upload_button.setObjectName("upload_button")
        self.gridLayout_3.addWidget(self.upload_button, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.upload_groupbox, 3, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 3, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 3, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)

        self.retranslateUi(pagepublish)
        QtCore.QMetaObject.connectSlotsByName(pagepublish)

    def retranslateUi(self, pagepublish):
        self.build_installer.setText(QtGui.QApplication.translate("PagePublish", "Build installer", None, QtGui.QApplication.UnicodeUTF8))
        self.results_groupbox.setTitle(QtGui.QApplication.translate("PagePublish", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.filename_label.setText(QtGui.QApplication.translate("PagePublish", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.size_label.setText(QtGui.QApplication.translate("PagePublish", "File size:", None, QtGui.QApplication.UnicodeUTF8))
        self.installed_size_label.setText(QtGui.QApplication.translate("PagePublish", "Installed size:", None, QtGui.QApplication.UnicodeUTF8))
        self.md5_label.setText(QtGui.QApplication.translate("PagePublish", "MD5 checksum:", None, QtGui.QApplication.UnicodeUTF8))
        self.upload_groupbox.setTitle(QtGui.QApplication.translate("PagePublish", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.upload_to_label.setText(QtGui.QApplication.translate("PagePublish", "Upload to:", None, QtGui.QApplication.UnicodeUTF8))
        self.upload_to.setItemText(0, QtGui.QApplication.translate("PagePublish", "SourceForge (portableapps)", None, QtGui.QApplication.UnicodeUTF8))
        self.upload_to.setItemText(1, QtGui.QApplication.translate("PagePublish", "portableapps.chrismorgan.info", None, QtGui.QApplication.UnicodeUTF8))
        self.configure_upload_targets.setText(QtGui.QApplication.translate("PagePublish", "Configure targets", None, QtGui.QApplication.UnicodeUTF8))
        self.upload_button.setText(QtGui.QApplication.translate("PagePublish", "Upload it", None, QtGui.QApplication.UnicodeUTF8))

