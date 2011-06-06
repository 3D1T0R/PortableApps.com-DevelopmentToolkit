# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/guiqt/ui/pagecompact.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageCompact(object):
    def setupUi(self, pagecompact):
        pagecompact.setObjectName("pagecompact")
        pagecompact.setGeometry(QtCore.QRect(0, 0, 960, 445))
        self.verticalLayout = QtGui.QVBoxLayout(pagecompact)
        self.verticalLayout.setObjectName("verticalLayout")
        self.start_button = QtGui.QCommandLinkButton(pagecompact)
        self.start_button.setObjectName("start_button")
        self.verticalLayout.addWidget(self.start_button)
        self.output = QtGui.QTextBrowser(pagecompact)
        self.output.setObjectName("output")
        self.verticalLayout.addWidget(self.output)
        self.advanced_groupbox = QtGui.QGroupBox(pagecompact)
        self.advanced_groupbox.setObjectName("advanced_groupbox")
        self.formLayout_3 = QtGui.QFormLayout(self.advanced_groupbox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.filesexcluded_label = QtGui.QLabel(self.advanced_groupbox)
        self.filesexcluded_label.setObjectName("filesexcluded_label")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.filesexcluded_label)
        self.filesexcluded = QtGui.QLineEdit(self.advanced_groupbox)
        self.filesexcluded.setObjectName("filesexcluded")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.filesexcluded)
        self.additionalextensionsexcluded_label = QtGui.QLabel(self.advanced_groupbox)
        self.additionalextensionsexcluded_label.setObjectName("additionalextensionsexcluded_label")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.additionalextensionsexcluded_label)
        self.additionalextensionsexcluded = QtGui.QLineEdit(self.advanced_groupbox)
        self.additionalextensionsexcluded.setObjectName("additionalextensionsexcluded")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.additionalextensionsexcluded)
        self.additionalextensionsincluded_label = QtGui.QLabel(self.advanced_groupbox)
        self.additionalextensionsincluded_label.setObjectName("additionalextensionsincluded_label")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.additionalextensionsincluded_label)
        self.additionalextensionsincluded = QtGui.QLineEdit(self.advanced_groupbox)
        self.additionalextensionsincluded.setObjectName("additionalextensionsincluded")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.additionalextensionsincluded)
        self.verticalLayout.addWidget(self.advanced_groupbox)
        self.filesexcluded_label.setBuddy(self.filesexcluded)
        self.additionalextensionsexcluded_label.setBuddy(self.additionalextensionsexcluded)
        self.additionalextensionsincluded_label.setBuddy(self.additionalextensionsincluded)

        self.retranslateUi(pagecompact)
        QtCore.QMetaObject.connectSlotsByName(pagecompact)

    def retranslateUi(self, pagecompact):
        self.start_button.setText(QtGui.QApplication.translate("PageCompact", "Start compacting app", None, QtGui.QApplication.UnicodeUTF8))
        self.advanced_groupbox.setTitle(QtGui.QApplication.translate("PageCompact", "Advanced configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.filesexcluded_label.setText(QtGui.QApplication.translate("PageCompact", "&Files to exclude:", None, QtGui.QApplication.UnicodeUTF8))
        self.filesexcluded.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter a pipe-separated list of filenames to exclude from compression.  Wildcards are not accepted.</p><p><strong>Example:</strong> <code>msvcm90.dll|msvcp90.dll|mscvr90.dll</code></p>", None, QtGui.QApplication.UnicodeUTF8))
        self.additionalextensionsexcluded_label.setText(QtGui.QApplication.translate("PageCompact", "Additional extensions &excluded:", None, QtGui.QApplication.UnicodeUTF8))
        self.additionalextensionsexcluded.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter a pipe-separated list of file extensions to exclude from compression.  Wildcards are not accepted.</p><p><strong>Example:</strong> <code>pyd|irc</code></p>", None, QtGui.QApplication.UnicodeUTF8))
        self.additionalextensionsincluded_label.setText(QtGui.QApplication.translate("PageCompact", "Additional extensions &included:", None, QtGui.QApplication.UnicodeUTF8))
        self.additionalextensionsincluded.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter a pipe-separated list of additional file extensions to compress.  Wildcards are not accepted.</p><p><strong>Example:</strong> <code>example|beta</code></p>", None, QtGui.QApplication.UnicodeUTF8))

