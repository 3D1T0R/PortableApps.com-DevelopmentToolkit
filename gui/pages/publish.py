import os
import hashlib
from ._base import WindowPage, assert_valid_package_path
from ..ui.pagepublish import Ui_PagePublish
from PyQt4 import QtCore, QtGui
from utils import _, size_string_megabytes


class PagePublish(WindowPage, Ui_PagePublish):
    def __init__(self, *args, **kwargs):
        super(PagePublish, self).__init__(*args, **kwargs)
        # No automatic uploads yet, kill the QGroupBox
        self.upload_groupbox.deleteLater()
        del self.upload_groupbox

    @assert_valid_package_path
    def enter(self):
        self.filename.setText(self.window.package.installer.filename)
        self.update_contents_async()

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
        self.update_contents_async()
        # If it didn't build, they got an error from the Installer wizard,
        # so no need to complain. When the Installer is integrated in here,
        # we will need to handle it in here.

    def update_contents_async(self):
        self.update_contents()
        # TODO: use QThread to make it non-blocking while still being safe.
        # (threading.Thread causes deadlock fairly often this way.)
        #threading.Thread(target=self.update_contents).start()

    @assert_valid_package_path
    def update_contents(self):
        """Enable or disable the controls which depend on the installer being built."""
        state = os.path.isfile(self.window.package.installer.filename)
        self.results_groupbox.setEnabled(state)
        #self.upload_groupbox.setEnabled(state)

        if state:  # Got it, now update the info about it
            self.md5.setText('Calculating...')
            self.size.setText('Calculating...')
            self.size_installed.setText('Calculating...')
            filename = self.installer_path
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
            # + 0.05 is to round up
            self.size.setText(size_string_megabytes(size))
            minsize, maxsize = [size_string_megabytes(s) for s in self.window.package.installed_size()]
            if minsize == maxsize:
                self.size_installed.setText(minsize)
            else:
                self.size_installed.setText('%s-%s' % (minsize, maxsize))
        else:
            self.md5.setText('')
            self.size.setText('')
            self.size_installed.setText('')

    @property
    def installer_path(self):
        """The full path to the installer when built. May or may not exist."""
        return self.window.package.path('..', self.window.package.installer.filename)
