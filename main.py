#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from qt import QtCore, QtGui
from ui.mainwindow import Ui_MainWindow
from utils import _, center_window
import paf
import paf.validate_gui
import paf.validate_cli
import config
import warnings
import warn
import appinfo
from functools import wraps
from subprocess import Popen, PIPE


def assert_valid_package_path(func):
    """Decorator to make sure that something which shouldn't ever happen
    doesn't cause a crash, and to provide a code indication of what's
    happening."""
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not paf.valid_package(unicode(self.ui.packageText.text())):
            raise Exception("The package is not valid.")

        func(self, *args, **kwargs)
    return decorate


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.packageText.setFocus()

    @QtCore.Slot(bool)
    def on_packageButton_clicked(self, checked):
        "Select a package."
        text_box = self.ui.packageText
        current_path = text_box.text()
        text_box.setText(QtGui.QFileDialog.getExistingDirectory(None,
            _("Select a portable app package"), current_path) or current_path)

    @QtCore.Slot(bool)
    def on_createButton_clicked(self, checked):
        "Create a package."
        self.ui.statusBar.showMessage(_("Creating package..."))
        text_box = self.ui.packageText
        current_path = text_box.text()
        while True:
            package = QtGui.QFileDialog.getExistingDirectory(None,
                    _("Create a directory for the package"))
            if package:
                try:
                    paf.create_package(unicode(package))
                except paf.PAFException as e:
                    QtGui.QMessageBox.critical(self,
                            _('PortableApps.com Development Toolkit'),
                            unicode(e), QtGui.QMessageBox.Ok)
                    continue

                text_box.setText(package)
                self.ui.statusBar.showMessage(
                        _("Package created successfully."), 2000)
                self.on_detailsButton_clicked(False)
            else:
                self.ui.statusBar.clearMessage()
            break

    @QtCore.Slot(bool)
    @assert_valid_package_path
    def on_detailsButton_clicked(self, checked):
        "Edit PortableApps.com Format details."
        appinfo_dialog = appinfo.AppInfoDialog(self)
        center_window(appinfo_dialog)
        appinfo_dialog.load_package(paf.Package(
            unicode(self.ui.packageText.text())))
        appinfo_dialog.setModal(True)
        appinfo_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self.dialog = appinfo_dialog

    @QtCore.Slot(bool)
    @assert_valid_package_path
    def on_validateButton_clicked(self, checked):
        "Validate the app."
        validate_dialog = paf.validate_gui.validate(self.ui.packageText.text(),
                self)
        center_window(validate_dialog)
        validate_dialog.setModal(True)
        validate_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self.dialog = validate_dialog

    @QtCore.Slot(bool)
    @assert_valid_package_path
    def on_installerButton_clicked(self, checked=None):
        "Build the installer with the PortableApps.com Installer."

        package_path = self.ui.packageText.text()

        # First of all, check that it's valid.
        self.ui.statusBar.showMessage(_("Validating package..."))
        package = paf.Package(package_path)
        package.validate()

        if len(package.errors):
            QtGui.QMessageBox.critical(self,
                    _('PortableApps.com Development Toolkit'),
                    _('There are errors in the package. You must fix them before making a release.'),
                    QtGui.QMessageBox.Ok)
            self.on_validateButton_clicked(False)
            self.ui.statusBar.clearMessage()
            return
        elif len(package.warnings):
            answer = QtGui.QMessageBox.warning(self,
                    _('PortableApps.com Development Toolkit'),
                    _('There are warnings in the package validation. You should fix them before making a release.'),
                    QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ignore)
            if answer == QtGui.QMessageBox.Cancel:
                self.on_validateButton_clicked(False)
                self.ui.statusBar.clearMessage()
                return

        installer_path = config.get('Main', 'InstallerPath')

        if not installer_path or not os.path.isfile(installer_path):
            # Try intelligently guessing if in PAF structure
            portableapps_dir = os.path.dirname(
                    config.ROOT_DIR.rpartition(
                        os.path.sep + 'App' + os.path.sep)[0])
            installer_path = os.path.join(portableapps_dir,
                    'PortableApps.comInstaller',
                    'PortableApps.comInstaller.exe')
            if not portableapps_dir or not os.path.isfile(installer_path):
                installer_path = QtGui.QFileDialog.getOpenFileName(self,
                        _('Select the path to the PortableApps.com Installer'),
                        config.ROOT_DIR,
                        'PortableApps.com Installer (PortableApps.comInstaller.exe)')

            if installer_path and os.path.isfile(installer_path):
                config.settings.Main.InstallerPath = installer_path
            else:
                QtGui.QMessageBox.critical(self,
                        _('PortableApps.com Development Toolkit'),
                        _('Unable to locate the PortableApps.com Installer.'),
                        QtGui.QMessageBox.Ok)
                self.ui.statusBar.clearMessage()
                return

        self.ui.statusBar.showMessage(_("Building installer..."))
        if package.installer.build():
            self.ui.statusBar.showMessage(_('Installer built successfully.'),
                    2000)
            # TODO: calculate MD5 checksum and installer size (also installed
            # size lazily, in a non-blocking way) and show user
        else:
            # They've already got an error from the Installer wizard, so no
            # need to complain too loudly.
            #QtGui.QMessageBox.critical(self,
            #        _('PortableApps.com Development Toolkit'),
            #        _('The installer failed to build.'),
            #        QtGui.QMessageBox.Ok)
            #self.ui.statusBar.clearMessage()
            self.ui.statusBar.showMessage(_('Installer failed to build.'),
                    2000)

    def on_packageText_textChanged(self, string):
        """
        Enable or disable the buttons below based on whether the text is a
        valid directory. This is used instead of a validator so it can do
        something without being overly hacky.
        """
        valid = paf.valid_package(unicode(string))
        self.ui.detailsButton.setEnabled(valid)
        self.ui.validateButton.setEnabled(valid)
        self.ui.installerButton.setEnabled(valid)


def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()

    window.ui.packageText.setText(config.get('Main', 'Package', ''))

    center_window(window)
    window.show()
    warn.set_warnings_qt()
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
    window = paf.validate_gui.validate(sys.argv[2])
    exit_code = app.exec_()

    return exit_code


def validate_cli():
    return paf.validate_cli.validate(sys.argv[2])


def not_implemented():
    warnings.warn('Sorry, this is not implemented yet.',
            UserWarning, stacklevel=2)


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
