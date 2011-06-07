import os
import hashlib
from ._base import WindowPage, assert_valid_package_path
from ..ui.pagepublish import Ui_PagePublish
from PyQt4 import QtCore, QtGui
from utils import _


class PagePublish(WindowPage, Ui_PagePublish):
    @assert_valid_package_path
    def enter(self):
        self.update_contents()
        self.filename.setText(self.installer_path)

    @QtCore.Slot()
    @assert_valid_package_path
    def on_build_installer_clicked(self):
        # First of all, check that it's valid.
        package = self.window.package
        package.validate()

        if len(package.errors):
            QtGui.QMessageBox.critical(self,
                    _('PortableApps.com Development Toolkit'),
                    _('There are errors in the package. You must fix them before making a release.'),
                    QtGui.QMessageBox.Ok)
            self.window.set_page('test')
            self.window.page_test.go_to_tab('validate')
            return
        elif len(package.warnings):
            answer = QtGui.QMessageBox.warning(self,
                    _('PortableApps.com Development Toolkit'),
                    _('There are warnings in the package validation. You should fix them before making a release.'),
                    QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ignore)
            if answer == QtGui.QMessageBox.Cancel:
                self.window.set_page('test')
                self.window.page_test.go_to_tab('validate')
                return

        installer_path = self.window.page_options.find_installer_path()

        if installer_path is None:
            return  # User told about it in find_installer_path

        package.installer.build()  # Can use returned bool if needed
        self.update_contents()
        # If it didn't build, they got an error from the Installer wizard,
        # so no need to complain. When the Installer is integrated in here,
        # we will need to handle it in here.

    @assert_valid_package_path
    def update_contents(self):
        """Enable or disable the controls which depend on the installer being built."""
        filename = self.installer_path
        state = os.path.isfile(filename)
        self.results_groupbox.setEnabled(state)
        self.upload_groupbox.setEnabled(state)

        if state:  # Got it, now update the info about it
            f = open(filename, 'rb')
            md5 = hashlib.md5()
            size = 0  # Doing it this way to save a file size stat
            while True:
                data = f.read(16384)  # Multiple of 128; somewhat arbitrary.
                size += len(data)
                if len(data) == 0:
                    break
                md5.update(data)
            self.md5.setText(md5.hexdigest())
            self.size.setText('%.1f MB' % round(size / 1048576., 1))
            self.size_installed.setText('TODO')
        else:
            self.md5.setText('')
            self.size.setText('')
            self.size_installed.setText('')

    @property
    def installer_path(self):
        """The full path to the installer when built. May or may not exist."""
        return self.window.package.path('..', self.window.package.installer.filename)
