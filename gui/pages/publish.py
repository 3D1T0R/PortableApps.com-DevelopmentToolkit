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

    @assert_valid_package_path
    def update_contents_async(self):
        calc_str = _('Calculating...')
        self.update_stats({'md5': calc_str, 'size': calc_str, 'size_installed': calc_str})
        self._stats_updater = StatUpdaterThread(self)
        self._stats_updater.update_stats.connect(self.update_stats)
        self._stats_updater.start()

    def update_stats(self, stats):
        for key, value in stats.iteritems():
            if key in ('md5', 'size', 'size_installed'):
                getattr(self, key).setText(value)
            else:
                raise ValueError('update_stats only accepts keys md5, size, size_installed')

    @property
    def installer_path(self):
        """The full path to the installer when built. May or may not exist."""
        return self.window.package.path('..', self.window.package.installer.filename)


class StatUpdaterThread(QtCore.QThread):
    update_stats = QtCore.Signal(dict)

    def __init__(self, page, *args, **kwargs):
        self.page = page
        super(StatUpdaterThread, self).__init__(*args, **kwargs)

    def run(self):
        filename = self.page.installer_path
        f = open(filename, 'rb')
        md5 = hashlib.md5()
        size = 0  # Doing it this way to save a file size stat
        while True:
            data = f.read(16384)  # Multiple of 128; somewhat arbitrary.
            size += len(data)
            if len(data) == 0:
                break
            md5.update(data)
        self.update_stats.emit({'md5': md5.hexdigest(), 'size': size_string_megabytes(size)})
        minsize, maxsize = [size_string_megabytes(s) for s in self.page.window.package.installed_size()]
        if minsize == maxsize:
            size_installed = minsize
        else:
            size_installed = '%s-%s' % (minsize, maxsize)
        self.update_stats.emit({'size_installed': size_installed})
