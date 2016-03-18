# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/pageabout.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageAbout(object):
    def setupUi(self, PageAbout):
        PageAbout.setObjectName("PageAbout")
        PageAbout.resize(960, 445)
        self.gridLayout = QtGui.QGridLayout(PageAbout)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 7, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 7, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.about_productname = QtGui.QLabel(PageAbout)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.about_productname.setFont(font)
        self.about_productname.setObjectName("about_productname")
        self.gridLayout.addWidget(self.about_productname, 1, 1, 1, 1)
        self.about_version = QtGui.QLabel(PageAbout)
        self.about_version.setObjectName("about_version")
        self.gridLayout.addWidget(self.about_version, 2, 1, 1, 1)
        self.about_copyright = QtGui.QLabel(PageAbout)
        self.about_copyright.setObjectName("about_copyright")
        self.gridLayout.addWidget(self.about_copyright, 3, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 4, 1, 1, 1)
        self.about_description = QtGui.QLabel(PageAbout)
        self.about_description.setObjectName("about_description")
        self.gridLayout.addWidget(self.about_description, 5, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem5, 6, 1, 1, 1)
        self.about_links = QtGui.QLabel(PageAbout)
        self.about_links.setOpenExternalLinks(True)
        self.about_links.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.about_links.setObjectName("about_links")
        self.gridLayout.addWidget(self.about_links, 7, 1, 1, 1)

        self.retranslateUi(PageAbout)
        QtCore.QMetaObject.connectSlotsByName(PageAbout)

    def retranslateUi(self, PageAbout):
        self.about_productname.setText(QtGui.QApplication.translate("PageAbout", "PortableApps.com Development Toolkit", None, QtGui.QApplication.UnicodeUTF8))
        self.about_version.setText(QtGui.QApplication.translate("PageAbout", "Version 1.0 Alpha 1.2", None, QtGui.QApplication.UnicodeUTF8))
        self.about_copyright.setText(QtGui.QApplication.translate("PageAbout", "© 2011 PortableApps.com (Chris Morgan)", None, QtGui.QApplication.UnicodeUTF8))
        self.about_description.setText(QtGui.QApplication.translate("PageAbout", "A utility to assist in the creation of high quality portable apps.", None, QtGui.QApplication.UnicodeUTF8))
        self.about_links.setText(QtGui.QApplication.translate("PageAbout", "<p>If you find bugs or have suggestions to make, please contact us.</p>\n"
"<p><strong>Links:</strong><br><a href=\"http://portableapps.com\">PortableApps.com</a><br>\n"
"<a href=\"http://portableapps.com/development\">PortableApps.com/Development</a></p>", None, QtGui.QApplication.UnicodeUTF8))

