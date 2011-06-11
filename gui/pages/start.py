from ._base import WindowPage
from ..ui.pagestart import Ui_PageStart
import paf
from PyQt4 import QtCore, QtGui
from utils import _, path_local


class PageStart(WindowPage, Ui_PageStart):
    def leave(self, closing=False):
        """Set MainWindow.package when leaving the page."""
        path = self.open.text()
        if paf.valid_package(path) and not closing:
            try:
                self.window.package = paf.Package(path)
            except paf.PAFException as e:
                QtGui.QMessageBox.critical(self,
                        _('Unable to load package'),
                        unicode(e), QtGui.QMessageBox.Ok)
                return False  # don't go to a different page, please.
        else:
            self.window.package = None

    @QtCore.Slot(unicode)
    def on_open_textChanged(self, string):
        """
        Enable or disable the buttons below based on whether the text is a
        valid directory. This is used instead of a validator so it can do
        something without being overly hacky.
        """

        from . import pages
        valid = paf.valid_package(string)
        for p in pages:
            if p not in ('start', 'options', 'about'):
                getattr(self.window, 'nav_%s' % p).setEnabled(valid)

    @QtCore.Slot()
    def on_open_browse_clicked(self):
        """Select a package."""
        text_box = self.open
        current_path = text_box.text()
        text_box.setText(path_local(QtGui.QFileDialog.getExistingDirectory(None,
            _("Select a portable app package"), current_path)) or current_path)

    @QtCore.Slot()
    def on_create_browse_clicked(self):
        """Select a directory to create a new package in."""
        text_box = self.create
        current_path = text_box.text()
        text_box.setText(path_local(QtGui.QFileDialog.getExistingDirectory(None,
            _("Create a directory for the package"))) or current_path)

    @QtCore.Slot()
    def on_create_button_clicked(self):
        """Create a package."""
        package = self.create.text()
        if not package:
            # Nothing in the field, get a path from the user first
            self.on_create_browse_clicked()
            package = self.create.text()

        if package:
            package = path_local(package)
            try:
                paf.create_package(package)
            except paf.PAFException as e:
                QtGui.QMessageBox.critical(self,
                        _('Unable to create package'),
                        unicode(e), QtGui.QMessageBox.Ok)
            else:
                self.open.setText(package)
                self.create.setText('')
                self.window.set_page('details')
