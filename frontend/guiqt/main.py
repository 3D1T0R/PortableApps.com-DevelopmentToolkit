import os
from functools import wraps
from PyQt4 import QtCore, QtGui
from ui.mainwindow import Ui_MainWindow
import paf
import config
from utils import _, center_window, path_local
from validate import ValidationDialog
import appinfo


def assert_valid_package_path(func):
    """Decorator to make sure that something which shouldn't ever happen
    doesn't cause a crash, and to provide a code indication of what's
    happening."""
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not paf.valid_package(self.packageText.text()):
            raise Exception("The package is not valid.")

        func(self, *args, **kwargs)
    return decorate


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.packageText.setFocus()
        self.on_packageText_textChanged(self.packageText.text())

    @QtCore.Slot()
    def on_packageButton_clicked(self):
        "Select a package."
        text_box = self.packageText
        current_path = text_box.text()
        text_box.setText(path_local(QtGui.QFileDialog.getExistingDirectory(None,
            _("Select a portable app package"), current_path)) or current_path)

    @QtCore.Slot()
    def on_createButton_clicked(self):
        "Create a package."
        self.statusBar.showMessage(_("Creating package..."))
        while True:
            package = QtGui.QFileDialog.getExistingDirectory(None,
                    _("Create a directory for the package"))
            if package:
                package = path_local(package)
                try:
                    paf.create_package(package)
                except paf.PAFException as e:
                    QtGui.QMessageBox.critical(self,
                            _('PortableApps.com Development Toolkit'),
                            unicode(e), QtGui.QMessageBox.Ok)
                    continue

                self.packageText.setText(package)
                self.statusBar.showMessage(
                        _("Package created successfully."), 2000)
                self.on_detailsButton_clicked()
            else:
                self.statusBar.clearMessage()
            break

    @QtCore.Slot()
    @assert_valid_package_path
    def on_detailsButton_clicked(self):
        "Edit PortableApps.com Format details."
        appinfo_dialog = appinfo.AppInfoDialog(self)
        center_window(appinfo_dialog)
        appinfo_dialog.load_package(paf.Package(self.packageText.text()))
        appinfo_dialog.setModal(True)
        appinfo_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self._dialog = appinfo_dialog

    @QtCore.Slot()
    @assert_valid_package_path
    def on_validateButton_clicked(self):
        "Validate the app."
        validate_dialog = ValidationDialog(self.packageText.text(), self)
        center_window(validate_dialog)
        validate_dialog.setModal(True)
        validate_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self._dialog = validate_dialog

    @QtCore.Slot()
    @assert_valid_package_path
    def on_installerButton_clicked(self):
        "Build the installer with the PortableApps.com Installer."

        package_path = self.packageText.text()

        # First of all, check that it's valid.
        self.statusBar.showMessage(_("Validating package..."))
        package = paf.Package(package_path)
        package.validate()

        if len(package.errors):
            QtGui.QMessageBox.critical(self,
                    _('PortableApps.com Development Toolkit'),
                    _('There are errors in the package. You must fix them before making a release.'),
                    QtGui.QMessageBox.Ok)
            self.on_validateButton_clicked()
            self.statusBar.clearMessage()
            return
        elif len(package.warnings):
            answer = QtGui.QMessageBox.warning(self,
                    _('PortableApps.com Development Toolkit'),
                    _('There are warnings in the package validation. You should fix them before making a release.'),
                    QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ignore)
            if answer == QtGui.QMessageBox.Cancel:
                self.on_validateButton_clicked()
                self.statusBar.clearMessage()
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
                self.statusBar.clearMessage()
                return

        self.statusBar.showMessage(_("Building installer..."))
        if package.installer.build():
            self.statusBar.showMessage(_('Installer built successfully.'),
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
            #self.statusBar.clearMessage()
            self.statusBar.showMessage(_('Installer failed to build.'),
                    2000)

    @QtCore.Slot(unicode)
    def on_packageText_textChanged(self, string):
        """
        Enable or disable the buttons below based on whether the text is a
        valid directory. This is used instead of a validator so it can do
        something without being overly hacky.
        """
        valid = paf.valid_package(string)
        self.detailsButton.setEnabled(valid)
        self.validateButton.setEnabled(valid)
        self.installerButton.setEnabled(valid)
