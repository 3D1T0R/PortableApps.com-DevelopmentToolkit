#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui.mainwindow import Ui_MainWindow
from utils import _
import paf
import config
import warnings
import warn

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.packageText.setFocus()

        # Currently all slots are auto-connected which is a Good Thing.
        # QtCore.QMetaObject.connectSlotsByName(self)

    def on_packageButton_clicked(self, checked=None):
        if checked == None: return
        text_box = self.ui.packageText
        current_path = text_box.text()
        text_box.setText(QtGui.QFileDialog.getExistingDirectory(None, _("Select a portable app package"), current_path) or current_path)

    def on_createButton_clicked(self, checked=None):
        if checked == None: return
        text_box = self.ui.packageText
        current_path = text_box.text()
        while True:
            package = QtGui.QFileDialog.getExistingDirectory(None, _("Create a directory for the package"))
            if package:
                try:
                    paf.create_package(unicode(package))
                except paf.PAFException as e:
                    QtGui.QMessageBox.critical(self, _('PortableApps.com Development Toolkit'), unicode(e), QtGui.QMessageBox.Ok)
                    continue

                text_box.setText(package)
                # TODO: go straight on to the Format window for AppInfo filling-in
                #self.on_launcherButton_clicked(False)
            break

    def on_formatButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented()

    def on_launcherButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented()

    def on_installerButton_clicked(self, checked=None):
        if checked == None: return
        not_implemented()

    def on_packageText_textChanged(self, string):
        """
        Enable or disable the buttons below based on whether the text is a
        valid directory. This is used instead of a validator so it can do
        something without being overly hacky.
        """
        valid = paf.valid_package(unicode(string))
        self.ui.formatButton.setEnabled(valid)
        self.ui.launcherButton.setEnabled(valid)
        self.ui.installerButton.setEnabled(valid)

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

def quit(window, exit_code):
    config.settings.Main.Package = window.ui.packageText.text()
    config.save()

    sys.exit(exit_code)

def not_implemented():
    warnings.warn('Sorry, this is not implemented yet.', UserWarning, stacklevel=2)

if __name__ == "__main__":
    main()
