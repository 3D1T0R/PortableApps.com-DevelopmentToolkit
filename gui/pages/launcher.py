from ._base import WindowPage, assert_valid_package_path
from ..ui.pagelauncher import Ui_PageLauncher
from PyQt4 import QtCore, QtGui
from utils import _


class PageLauncher(WindowPage, Ui_PageLauncher):
    @QtCore.Slot()
    @assert_valid_package_path
    def on_build_launcher_clicked(self):
        # First of all, check that it's valid.
        if self.window.package.appid is None:
            QtGui.QMessageBox.critical(self,
                    _('PortableApps.com Development Toolkit'),
                    _('The package AppID must be set before you can compile the launcher.'),
                    QtGui.QMessageBox.Ok)
            self.window.set_page('details')
            return

        if self.window.page_options.find_launcher_path():
            # No callback at present, use QThread when we need it
            self.window.package.launcher.build(block=False)
