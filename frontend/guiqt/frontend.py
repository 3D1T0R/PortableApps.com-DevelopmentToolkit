import os
from functools import wraps
from PyQt4 import QtCore, QtGui
from ui.frontend import Ui_MainWindow
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
        if not paf.valid_package(self.page_start.open.text()):
            raise Exception("The package is not valid.")

        func(self, *args, **kwargs)
    return decorate


pages = ('start', 'details', 'launcher', 'compact', 'test', 'publish', 'options', 'about')


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # Automatically added to self.pages
        self.page_start = PageStart(self.pages, self)
        self.page_details = PageDetails(self.pages, self)
        self.page_launcher = PageLauncher(self.pages, self)
        self.page_compact = PageCompact(self.pages, self)
        self.page_test = PageTest(self.pages, self)
        self.page_publish = PagePublish(self.pages, self)
        self.page_options = PageOptions(self.pages, self)
        self.page_about = PageAbout(self.pages, self)

        self.current_page = self.page_start
        self.current_nav = self.nav_start
        self.page_start.open.setFocus()
        self.page_start.on_open_textChanged(self.page_start.open.text())
        self.set_page('start')

        # TODO: remove this which is in for sideways compatibility
        self.packageText = self.page_start.open

    @QtCore.Slot()
    def set_page(self, name):
        self.current_nav.setChecked(False)
        self.current_nav = getattr(self, 'nav_%s' % name)
        self.current_page = getattr(self, 'page_%s' % name)
        self.pages.setCurrentIndex(pages.index(name))
        self.current_nav.setChecked(True)

    @QtCore.Slot()
    def on_nav_start_clicked(self):
        self.set_page('start')

    @QtCore.Slot()
    def on_nav_details_clicked(self):
        self.set_page('details')

    @QtCore.Slot()
    def on_nav_launcher_clicked(self):
        self.set_page('launcher')

    @QtCore.Slot()
    def on_nav_compact_clicked(self):
        self.set_page('compact')

    @QtCore.Slot()
    def on_nav_test_clicked(self):
        self.set_page('test')

    @QtCore.Slot()
    def on_nav_publish_clicked(self):
        self.set_page('publish')

    @QtCore.Slot()
    def on_nav_options_clicked(self):
        self.set_page('options')

    @QtCore.Slot()
    def on_nav_about_clicked(self):
        self.set_page('about')

    @QtCore.Slot()
    @assert_valid_package_path
    def on_detailsButton_clicked(self):
        "Edit PortableApps.com Format details."
        appinfo_dialog = appinfo.AppInfoDialog(self)
        center_window(appinfo_dialog)
        appinfo_dialog.load_package(paf.Package(self.page_start.open.text()))
        appinfo_dialog.setModal(True)
        appinfo_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self._dialog = appinfo_dialog

    @QtCore.Slot()
    @assert_valid_package_path
    def on_validateButton_clicked(self):
        "Validate the app."
        validate_dialog = ValidationDialog(self.page_start.open.text(), self)
        center_window(validate_dialog)
        validate_dialog.setModal(True)
        validate_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self._dialog = validate_dialog

    @QtCore.Slot()
    @assert_valid_package_path
    def on_installerButton_clicked(self):
        "Build the installer with the PortableApps.com Installer."

        package_path = self.page_start.open.text()

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

from ui.pagestart import Ui_PageStart
from ui.pagedetails import Ui_PageDetails
from ui.pagelauncher import Ui_PageLauncher
from ui.pagecompact import Ui_PageCompact
from ui.pagetest import Ui_PageTest
from ui.pagepublish import Ui_PagePublish
from ui.pageoptions import Ui_PageOptions
from ui.pageabout import Ui_PageAbout

class WindowPage(QtGui.QWidget):
    def __init__(self, parent, window):
        super(WindowPage, self).__init__(parent)
        self.setupUi(self)
        self.window = window
        parent.addWidget(self)  # Add self to the pages QStackedWidget


class PageStart(WindowPage, Ui_PageStart):
    @QtCore.Slot(unicode)
    def on_open_textChanged(self, string):
        """
        Enable or disable the buttons below based on whether the text is a
        valid directory. This is used instead of a validator so it can do
        something without being overly hacky.
        """
        valid = paf.valid_package(string)
        for p in pages[1:-2]:  # Don't disable Start, Options or About
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
        if package:
            package = path_local(package)
            try:
                paf.create_package(package)
            except paf.PAFException as e:
                QtGui.QMessageBox.critical(self,
                        _('PortableApps.com Development Toolkit'),
                        unicode(e), QtGui.QMessageBox.Ok)
            else:
                self.open.setText(package)
                self.create.setText('')
                self.window.set_page('details')


class PageDetails(WindowPage, Ui_PageDetails):
    pass

class PageLauncher(WindowPage, Ui_PageLauncher):
    pass

class PageCompact(WindowPage, Ui_PageCompact):
    pass

class PageTest(WindowPage, Ui_PageTest):
    pass

class PagePublish(WindowPage, Ui_PagePublish):
    pass

class PageOptions(WindowPage, Ui_PageOptions):
    pass

class PageAbout(WindowPage, Ui_PageAbout):
    pass

