#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui.mainwindow import Ui_MainWindow
from utils import _
import config

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.packageText.setFocus();

        # Currently all slots are auto-connected which is a Good Thing.
        # QtCore.QMetaObject.connectSlotsByName(self)

    def on_packageButton_clicked(self, checked=None):
        if checked == None: return
        text_box = self.ui.packageText
        current_path = text_box.text()
        text_box.setText(QtGui.QFileDialog.getExistingDirectory(None, _("Select a portable app package"), current_path) or current_path)

    def on_createButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented(self)

    def on_formatButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented(self)

    def on_launcherButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented(self)

    def on_installerButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented(self)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()

    window.ui.packageText.setText(config.get('Main', 'Package', ''))

    window.center()
    window.show()
    exit_code = app.exec_()

    quit(window, exit_code)
    sys.exit(exit_code)

def quit(window, exit_code):
    config.settings.Main.Package = window.ui.packageText.text()
    config.save()

    sys.exit(exit_code)

def not_implemented(window):
    QtGui.QMessageBox.information(window, _('PortableApps.com Development Toolkit'), _('Sorry, this is not implemented yet.'), QtGui.QMessageBox.Ok)

if __name__ == "__main__":
    main()
