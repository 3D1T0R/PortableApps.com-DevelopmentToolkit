import os
from functools import wraps
from PyQt4 import QtCore, QtGui
from iniparse.config import Undefined
from .ui import (Ui_MainWindow, Ui_PageStart, Ui_PageDetails, Ui_PageLauncher,
        Ui_PageCompact, Ui_PageTest, Ui_PagePublish, Ui_PageOptions,
        Ui_PageAbout)
import paf
import config
from utils import _, center_window, path_local
from validate import ValidationDialog
import appinfo
from paf.appinfo import valid_appid
from languages import LANG


def assert_valid_package_path(func):
    """Decorator to make sure that something which shouldn't ever happen
    doesn't cause a crash, and to provide a code indication of what's
    happening."""
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if isinstance(self, MainWindow):
            window = self
        elif isinstance(self, WindowPage):
            window = self.window
        else:
            assert False, "assert_valid_package_path only works on MainWindow or WindowPage methods."
        assert paf.valid_package(window.page_start.open.text()), "The package is not valid."

        func(self, *args, **kwargs)
    return decorate


pages = ('start', 'details', 'launcher', 'compact', 'test', 'publish', 'options', 'about')


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Added to self.pages in WindowPage.__init__
        self.page_start = PageStart(self.pages, self)
        self.page_details = PageDetails(self.pages, self)
        self.page_launcher = PageLauncher(self.pages, self)
        self.page_compact = PageCompact(self.pages, self)
        self.page_test = PageTest(self.pages, self)
        self.page_publish = PagePublish(self.pages, self)
        self.page_options = PageOptions(self.pages, self)
        self.page_about = PageAbout(self.pages, self)

        self.page_start.open.setFocus()
        self.page_start.on_open_textChanged(self.page_start.open.text())
        self.set_page('start')

        # TODO: remove this which is in for sideways compatibility
        self.packageText = self.page_start.open

    @QtCore.Slot()
    def set_page(self, name):
        # On the first call, these aren't set, so skip them
        if hasattr(self, 'current_page'):
            # Make sure it's not highlighted, the user click will highlight it but the leave()
            # call can take time (e.g. show QMessageBox) which would make it look bad.
            getattr(self, 'nav_' + name).setChecked(False)
            if self.current_page.leave() is False:
                return
            self.current_nav.setChecked(False)
        self.current_nav = getattr(self, 'nav_%s' % name)
        self.current_page = getattr(self, 'page_%s' % name)
        self.pages.setCurrentIndex(pages.index(name))
        self.current_nav.setChecked(True)
        self.current_page.enter()

    def closeEvent(self, event):
        """Window closed, trigger the leave event for the current page."""
        self.current_page.leave(True)
        # TODO: move state saving from /main.py here

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


class WindowPage(QtGui.QWidget):
    def __init__(self, parent, window):
        super(WindowPage, self).__init__(parent)
        self.setupUi(self)
        self.window = window
        parent.addWidget(self)  # Add self to the pages QStackedWidget

    def enter(self):
        """Event called when the page is entered (startup or user action)."""

        pass

    def leave(self, closing=False):
        """
        Event called when the page is left (could be window close event or
        going to another tab).
        """

        pass


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
                        _('Unable to create package'),
                        unicode(e), QtGui.QMessageBox.Ok)
            else:
                self.open.setText(package)
                self.create.setText('')
                self.window.set_page('details')


class PageDetails(WindowPage, Ui_PageDetails):
    def __init__(self, *args, **kwargs):
        super(PageDetails, self).__init__(*args, **kwargs)
        self.AppID.setValidator(AppIDValidator())

    def leave(self, closing=False):
        """User leaves the page, so save. No validation at the moment."""
        self.save()

    @QtCore.Slot(unicode)
    def on_DisplayVersionType_currentIndexChanged(self, value):
        "Disable the DT/PR/revision number field for an official release."

        if value == '(official release)':
            self.DisplayVersionNum.setEnabled(False)
        else:
            self.DisplayVersionNum.setEnabled(True)

    @QtCore.Slot(unicode)
    def on_Name_textChanged(self, value):
        "Auto-fill some fields when the Name is changed."

        if hasattr(self.Name, 'matched'):
            return
        value = unicode(value)
        if hasattr(self.Name, 'backspacing'):
            self.Name.last_value = value
            return

        # Deal with backspace and this auto-complete thing
        if hasattr(self.Name, 'last_value') and \
                not hasattr(self.Name, 'backspacing') and \
                value == self.Name.last_value:
            self.Name.backspacing = True
            # This does make Delete act as Backspace sometimes, but never mind.
            self.Name.backspace()
            del self.Name.backspacing
            return
        self.Name.last_value = value

        # If the cursor is at the end of the line, and nothing is selected
        if self.Name.cursorPosition() == len(value) and \
                not self.Name.hasSelectedText():
            self.Name.matched = False
            for suffix in ', Portable Edition', ' Portable':
                for end in [suffix[:i] for i in xrange(len(suffix), 0, -1)]:
                    if value.endswith(end):
                        self.Name.matched = True
                        self.Name.insert(suffix[len(end):])
                        # Unfortunately setCursorPosition doesn't make it so
                        # the cursor can be at the start of the selection
                        self.Name.setSelection(len(value),
                                len(suffix) - len(end))
                        value = value + suffix[len(end):]
                        break
                if self.Name.matched:
                    break
            #if not self.Name.matched:
            #    self.Name.matched = True
            #    end = ' Portable'
            #    self.Name.insert(end)
            #    self.Name.setSelection(len(value), len(end))
            #    value = value + end
            del self.Name.matched

        for suffix in ', Portable Edition', ' Portable':
            if value.endswith(suffix):
                name = value[:-len(suffix)]
                break
        else:
            name = value

        # AppID for Whatever, Portable Edition is still WhateverPortable
        appid = value
        if appid.endswith(', Portable Edition'):
            appid = appid[:-len(', Portable Edition')] + ' Portable'

        # Correct it (don't care about whether it was valid)
        appid = valid_appid(appid)[1]

        if 'AppID' not in self.appinfo.Details and \
        not self.AppID.isModified():
            self.AppID.setText(appid)

        if 'Publisher' not in self.appinfo.Details and \
        not self.Publisher.isModified():
            self.Publisher.setText('%s team & PortableApps.com' % name)

        # Homepage: done by on_AppID_textChanged

        if 'Description' not in self.appinfo.Details and \
        not self.Description.isModified():
            self.Description.setText('%s is a ___' % name)

    @QtCore.Slot(unicode)
    def on_AppID_textChanged(self, value):
        "Auto-fill Homepage when the Name is changed."

        if 'Homepage' not in self.appinfo.Details and \
        not self.Homepage.isModified():
            self.Homepage.setText('PortableApps.com/%s' % unicode(value))

    def enter(self):
        self.appinfo = appinfo = self.window.package.appinfo.ini

        self._fill(self.Name, appinfo.Details.Name)
        self._fill(self.AppID, appinfo.Details.AppID)
        self._fill(self.Publisher, appinfo.Details.Publisher)
        self._fill(self.Homepage, appinfo.Details.Homepage)
        self._fill(self.Category, appinfo.Details.Category)
        self._fill(self.Description, appinfo.Details.Description)
        self._fill(self.Language, appinfo.Details.Language)
        self._fill(self.Trademarks, appinfo.Details.Trademarks)

        self._fill(self.Shareable, appinfo.License.Shareable)
        self._fill(self.OpenSource, appinfo.License.OpenSource)
        self._fill(self.Freeware, appinfo.License.Freeware)
        self._fill(self.CommercialUse, appinfo.License.CommercialUse)

        if 'PackageVersion' in appinfo.Version:
            pv = appinfo.Version.PackageVersion
            try:
                pv = map(int, pv.split('.'))
            except ValueError:
                pass
            else:
                if len(pv) == 4:
                    self._fill(self.PackageVersion1, pv[0])
                    self._fill(self.PackageVersion2, pv[1])
                    self._fill(self.PackageVersion3, pv[2])
                    self._fill(self.PackageVersion4, pv[3])

        # Split DisplayVersion into chunks
        if 'DisplayVersion' in appinfo.Version:
            dv = appinfo.Version.DisplayVersion
            splits = (
                    (' development test ', 'Development Test'),
                    (' developmenttest ', 'Development Test'),
                    (' devtest ', 'Development Test'),
                    (' dev test ', 'Development Test'),
                    (' prerelease ', 'Pre-Release'),
                    (' pre-release ', 'Pre-Release'),
                    (' prerelease', 'Pre-Release'),
                    (' revision ', 'Revision'),
                    (' rev ', 'Revision'))
            for match, target in splits:
                split = dv.lower().split(match)
                if len(split) == 2:
                    # Get the original case, for cases like "Alpha"
                    split[0] = dv[:len(split[0])]
                    split[1] = dv[-len(split[1]):]
                    try:
                        split[1] = int(split[1])
                    except ValueError:
                        split[1] = 0

                    self._fill(self.DisplayVersionBase, split[0])
                    self._fill(self.DisplayVersionType, target)
                    self._fill(self.DisplayVersionNum, split[1])
                    break
            else:
                self._fill(self.DisplayVersionBase, dv)
                self._fill(self.DisplayVersionType,
                        '(official release)')
                # TODO: this may not be necessary
                self.DisplayVersionNum.setEnabled(False)

        if not self.window.package.eula:
            self.EULAVersion.setEnabled(False)
        self._fill(self.EULAVersion, appinfo.Version.EULAVersion)

        # TODO: no Control section

        self._fill(self.PluginsPath, appinfo.SpecialPaths.Plugins)

        self._fill(self.UsesJava, appinfo.Dependencies.UsesJava)
        self._fill(self.UsesDotNetVersion,
                appinfo.Dependencies.UsesDotNetVersion)

    def save(self):
        "Loads the values from the GUI and saves them to appinfo.ini."
        self.update()
        self.window.package.appinfo.save()

    def update(self):
        "Updates the stored appinfo based on the values in the GUI."

        appinfo = self.appinfo

        appinfo.Format.Type = 'PortableApps.comFormat'
        appinfo.Format.Version = '2.0'

        appinfo.Details.Name = self.Name.text()
        appinfo.Details.AppID = self.AppID.text()
        appinfo.Details.Publisher = self.Publisher.text()
        appinfo.Details.Homepage = self.Homepage.text()
        appinfo.Details.Category = self.Category.currentText()
        appinfo.Details.Description = self.Description.text()
        appinfo.Details.Language = self.Language.currentText()
        if self.Trademarks.text():
            appinfo.Details.Trademarks = self.Trademarks.text()

        b = lambda i: 'true' if i.isChecked() else 'false'

        appinfo.License.Shareable = b(self.Shareable)
        appinfo.License.OpenSource = b(self.OpenSource)
        appinfo.License.Freeware = b(self.Freeware)
        appinfo.License.CommercialUse = b(self.CommercialUse)

        if self.EULAVersion.isEnabled() and self.EULAVersion.text():
            appinfo.License.EULAVersion = self.EULAVersion.text()

        appinfo.Version.PackageVersion = '.'.join(map(str, (
            self.PackageVersion1.value(), self.PackageVersion2.value(),
            self.PackageVersion3.value(), self.PackageVersion4.value())))

        dvtype = self.DisplayVersionType.currentText()
        appinfo.Version.DisplayVersion = self.DisplayVersionBase.text()
        if dvtype != '(official release)':
            appinfo.Version.DisplayVersion += ' ' + dvtype + ' ' + \
                    str(self.DisplayVersionNum.value())

        if self.PluginsPath.text():
            appinfo.SpecialPaths.Plugins = self.PluginsPath.text()

        if self.UsesJava.isChecked():
            appinfo.Dependencies.UsesJava = 'true'
        # If it was ticked before, remove it
        elif 'UsesJava' in appinfo.Dependencies:
            del appinfo.Dependencies.UsesJava

        if self.UsesDotNetVersion.currentText() != 'None':
            appinfo.Dependencies.UsesDotNetVersion = \
                    self.UsesDotNetVersion.currentText()
        # If it was set before, remove it
        elif 'UsesDotNetVersion' in appinfo.Dependencies:
            del appinfo.Dependencies.UsesDotNetVersion

        # Deleting the last value in the section doesn't delete the section at
        # the moment, so delete it manually
        if 'Dependencies' in appinfo and not list(appinfo.Dependencies):
            del appinfo.Dependencies

        # TODO: no proper control of the Control section, dummy code
        if 'Control' not in appinfo:
            appinfo.Control.Icons = 1
            appinfo.Control.Start = '%s.exe' % appinfo.Details.AppID

    def _fill(self, field, value):
        if isinstance(value, Undefined):
            return

        if isinstance(field, QtGui.QComboBox):
            index = field.findText(value)
            if index > -1:
                field.setCurrentIndex(index)
            elif field.isEditable():
                field.setEditText(index)
            # else fail silently
        elif isinstance(field, QtGui.QCheckBox):
            if value == 'true':
                field.setChecked(True)
            elif value == 'false':
                field.setChecked(False)
            # else fail silently
        elif isinstance(field, QtGui.QLineEdit):
            field.setText(value)
            field.setCursorPosition(0)
        elif isinstance(field, QtGui.QSpinBox):
            try:
                value = int(value)
            except ValueError:
                pass
            else:
                field.setValue(value)
        else:
            raise TypeError("Field %s type %s is invalid." % (field,
                type(field)))


class AppIDValidator(QtGui.QValidator):
    "A QValidator for the AppID."
    def validate(self, input, pos):
        "Validate the AppID."

        valid, appid = valid_appid(input)
        if valid:
            return QtGui.QValidator.Acceptable, appid, pos
        else:
            return QtGui.QValidator.Invalid, appid, pos


class PageLauncher(WindowPage, Ui_PageLauncher):
    pass


class PageCompact(WindowPage, Ui_PageCompact):
    pass


class PageTest(WindowPage, Ui_PageTest):
    @assert_valid_package_path
    def enter(self):
        self.validate()
        self.load_checklist()

    @assert_valid_package_path
    def validate(self):
        """Validate the app."""
        package = self.window.package

        error_count = len(package.errors)
        warning_count = len(package.warnings)
        params = {
                'numerrors': error_count,
                'numwarnings': warning_count,
                'strerrors': error_count == 1 and 'error' or 'errors',
                'strwarnings': warning_count == 1 and 'warning' or 'warnings',
                }
        if error_count and warning_count:
            out = LANG.VALIDATION.ERRORS_WARNINGS_HTML % params
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_FAIL)
        elif error_count:
            out = LANG.VALIDATION.ERRORS_HTML % params
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_FAIL)
        elif warning_count:
            out = LANG.VALIDATION.WARNINGS_HTML % params
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_WARNINGS)
        else:
            out = LANG.VALIDATION.PASS_HTML
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_PASS)

        out = '<p>' + out + '</p>\n\n'

        if error_count:
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_ERRORS
            for item in package.errors:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        if warning_count:
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_WARNINGS
            for item in package.warnings:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        if len(package.info):
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_INFORMATION
            for item in package.info:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        self.validation_results_html.setHtml(out)
        self.validation_results_plain.setPlainText(out)

    @assert_valid_package_path
    def load_checklist(self):
        pass  # TODO

class PagePublish(WindowPage, Ui_PagePublish):
    pass


class PageOptions(WindowPage, Ui_PageOptions):
    pass


class PageAbout(WindowPage, Ui_PageAbout):
    pass
