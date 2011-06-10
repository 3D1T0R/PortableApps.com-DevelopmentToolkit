# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/pagecompact.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageCompact(object):
    def setupUi(self, PageCompact):
        PageCompact.setObjectName("PageCompact")
        PageCompact.resize(960, 445)
        self.verticalLayout = QtGui.QVBoxLayout(PageCompact)
        self.verticalLayout.setObjectName("verticalLayout")
        self.start_button = QtGui.QCommandLinkButton(PageCompact)
        self.start_button.setObjectName("start_button")
        self.verticalLayout.addWidget(self.start_button)
        self.output = QtGui.QTextBrowser(PageCompact)
        self.output.setObjectName("output")
        self.verticalLayout.addWidget(self.output)
        self.advanced_groupbox = QtGui.QGroupBox(PageCompact)
        self.advanced_groupbox.setObjectName("advanced_groupbox")
        self.advanced_layout = QtGui.QGridLayout(self.advanced_groupbox)
        self.advanced_layout.setObjectName("advanced_layout")
        self.files_excluded_label = QtGui.QLabel(self.advanced_groupbox)
        self.files_excluded_label.setObjectName("files_excluded_label")
        self.advanced_layout.addWidget(self.files_excluded_label, 0, 0, 1, 1)
        self.files_excluded = QtGui.QLineEdit(self.advanced_groupbox)
        self.files_excluded.setObjectName("files_excluded")
        self.advanced_layout.addWidget(self.files_excluded, 0, 1, 1, 2)
        self.compression_file_size_cut_off_label = QtGui.QLabel(self.advanced_groupbox)
        self.compression_file_size_cut_off_label.setObjectName("compression_file_size_cut_off_label")
        self.advanced_layout.addWidget(self.compression_file_size_cut_off_label, 1, 0, 1, 1)
        self.compression_file_size_cut_off = QtGui.QSpinBox(self.advanced_groupbox)
        self.compression_file_size_cut_off.setMaximum(1073741824)
        self.compression_file_size_cut_off.setProperty("value", 4096)
        self.compression_file_size_cut_off.setObjectName("compression_file_size_cut_off")
        self.advanced_layout.addWidget(self.compression_file_size_cut_off, 1, 1, 1, 1)
        self.compression_file_size_cut_off_unit_label = QtGui.QLabel(self.advanced_groupbox)
        self.compression_file_size_cut_off_unit_label.setObjectName("compression_file_size_cut_off_unit_label")
        self.advanced_layout.addWidget(self.compression_file_size_cut_off_unit_label, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.advanced_layout.addItem(spacerItem, 0, 3, 2, 1)
        self.additional_extensions_excluded_label = QtGui.QLabel(self.advanced_groupbox)
        self.additional_extensions_excluded_label.setObjectName("additional_extensions_excluded_label")
        self.advanced_layout.addWidget(self.additional_extensions_excluded_label, 0, 4, 1, 1)
        self.additional_extensions_excluded = QtGui.QLineEdit(self.advanced_groupbox)
        self.additional_extensions_excluded.setObjectName("additional_extensions_excluded")
        self.advanced_layout.addWidget(self.additional_extensions_excluded, 0, 5, 1, 1)
        self.additional_extensions_included_label = QtGui.QLabel(self.advanced_groupbox)
        self.additional_extensions_included_label.setObjectName("additional_extensions_included_label")
        self.advanced_layout.addWidget(self.additional_extensions_included_label, 1, 4, 1, 1)
        self.additional_extensions_included = QtGui.QLineEdit(self.advanced_groupbox)
        self.additional_extensions_included.setObjectName("additional_extensions_included")
        self.advanced_layout.addWidget(self.additional_extensions_included, 1, 5, 1, 1)
        self.advanced_layout.setColumnStretch(1, 1)
        self.advanced_layout.setColumnStretch(2, 1)
        self.advanced_layout.setColumnStretch(5, 2)
        self.verticalLayout.addWidget(self.advanced_groupbox)
        self.files_excluded_label.setBuddy(self.files_excluded)
        self.compression_file_size_cut_off_label.setBuddy(self.compression_file_size_cut_off)
        self.additional_extensions_excluded_label.setBuddy(self.additional_extensions_excluded)
        self.additional_extensions_included_label.setBuddy(self.additional_extensions_included)

        self.retranslateUi(PageCompact)
        QtCore.QMetaObject.connectSlotsByName(PageCompact)

    def retranslateUi(self, PageCompact):
        self.start_button.setText(QtGui.QApplication.translate("PageCompact", "Start &compacting app", None, QtGui.QApplication.UnicodeUTF8))
        self.advanced_groupbox.setTitle(QtGui.QApplication.translate("PageCompact", "Advanced configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.files_excluded_label.setText(QtGui.QApplication.translate("PageCompact", "&Files to exclude:", None, QtGui.QApplication.UnicodeUTF8))
        self.files_excluded.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter a pipe-separated list of filenames to exclude from compression.  Wildcards are not accepted.</p><p><strong>Example:</strong> <code>msvcm90.dll|msvcp90.dll|mscvr90.dll</code></p>", None, QtGui.QApplication.UnicodeUTF8))
        self.compression_file_size_cut_off_label.setText(QtGui.QApplication.translate("PageCompact", "&Size cutoff:", None, QtGui.QApplication.UnicodeUTF8))
        self.compression_file_size_cut_off.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter the minimum file size in bytes for files which will be compressed.</p><p><strong>Default:</strong> 4096 (files 4 KB and under will be ignored.)</p>", None, QtGui.QApplication.UnicodeUTF8))
        self.compression_file_size_cut_off_unit_label.setText(QtGui.QApplication.translate("PageCompact", "bytes", None, QtGui.QApplication.UnicodeUTF8))
        self.additional_extensions_excluded_label.setText(QtGui.QApplication.translate("PageCompact", "Additional extensions &excluded:", None, QtGui.QApplication.UnicodeUTF8))
        self.additional_extensions_excluded.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter a pipe-separated list of file extensions to exclude from compression.  Wildcards are not accepted.</p><p><strong>Example:</strong> <code>pyd|irc</code></p>", None, QtGui.QApplication.UnicodeUTF8))
        self.additional_extensions_included_label.setText(QtGui.QApplication.translate("PageCompact", "Additional extensions &included:", None, QtGui.QApplication.UnicodeUTF8))
        self.additional_extensions_included.setToolTip(QtGui.QApplication.translate("PageCompact", "<p>Enter a pipe-separated list of additional file extensions to compress.  Wildcards are not accepted.</p><p><strong>Example:</strong> <code>example|beta</code></p>", None, QtGui.QApplication.UnicodeUTF8))

