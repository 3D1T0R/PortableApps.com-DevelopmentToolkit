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
        self.ui.statusBar.showMessage(_("Creating package..."))
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
                self.ui.statusBar.showMessage(_("Package created successfully."), 2000)
                # TODO: go straight on to the Format window for AppInfo filling-in
                #self.on_launcherButton_clicked(False)
            else:
                self.ui.statusBar.clearMessage()
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

    prepare_quit(window)

    return exit_code

def prepare_quit(window):
    config.settings.Main.Package = window.ui.packageText.text()
    config.save()

def cli_help():
    print "PortableApps.com Development Toolkit"
    print "Launch without command line arguments to run normally."
    print
    print 'Validate a package (GUI):'
    print '  %s validate <package>' % sys.argv[0]
    print
    print 'Validate a package (command line):'
    print '  %s validate-cli <package>' % sys.argv[0]
    return 0

def validate_gui():
    app = QtGui.QApplication(sys.argv)
    not_implemented()
    # No app.exec_() as there's no window
    return 0

def validate_cli():
    import paf.validate_cli
    return paf.validate_cli.validate(sys.argv[2])

def not_implemented():
    warnings.warn('Sorry, this is not implemented yet.', UserWarning, stacklevel=2)

if len(sys.argv) > 1:
    if sys.argv[1] == 'help':
        action = cli_help
    elif sys.argv[1] == 'validate':
        action = len(sys.argv) == 3 and validate_gui or cli_help
    elif sys.argv[1] == 'validate-cli':
        action = len(sys.argv) == 3 and validate_cli or cli_help
    else:
        action = main
else:
    action = main

if __name__ == "__main__":
    sys.exit(action())
