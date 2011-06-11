# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/pagelauncher.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageLauncher(object):
    def setupUi(self, PageLauncher):
        PageLauncher.setObjectName("PageLauncher")
        PageLauncher.resize(960, 445)
        self.verticalLayout = QtGui.QVBoxLayout(PageLauncher)
        self.verticalLayout.setObjectName("verticalLayout")
        self.build_launcher = QtGui.QCommandLinkButton(PageLauncher)
        self.build_launcher.setObjectName("build_launcher")
        self.verticalLayout.addWidget(self.build_launcher)
        self.label_6 = QtGui.QLabel(PageLauncher)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setOpenExternalLinks(True)
        self.label_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(PageLauncher)
        QtCore.QMetaObject.connectSlotsByName(PageLauncher)

    def retranslateUi(self, PageLauncher):
        self.build_launcher.setText(QtGui.QApplication.translate("PageLauncher", "&Build launcher", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PageLauncher", "<p>A really advanced sort of editor and manager for PortableApps.com Launcher configuration will go here.</p><p>Unfortunately, it\'s going to be <em>so</em> powerful that it\'s not ready yet.</p><p>In the mean time, refer to the <a href=\"http://portableapps.com/manuals/PortableApps.comLauncher/\">PortableApps.com Launcher manual</a> for information on what to do.</p>", None, QtGui.QApplication.UnicodeUTF8))

