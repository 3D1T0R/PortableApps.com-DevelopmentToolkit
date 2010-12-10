#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.appinfo import Ui_AppInfoDialog
from utils import center_window
from paf.appinfo import valid_appid
from iniparse.config import Undefined


__all__ = ['AppInfoDialog']


class AppInfoDialog(QtGui.QDialog, Ui_AppInfoDialog):
    def __init__(self, parent=None):
        super(AppInfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.AppID.setValidator(AppIDValidator())

    def accept(self):
        "User submits the form (presses Save). No validation at the moment."
        self.save()
        # Two buttons, Save and Close, let them press Close manually
        #self.close()

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

    def load_package(self, package):
        self.package = package
        self.appinfo = appinfo = package.appinfo.ini

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
                split = map(str.strip, dv.lower().split(match))
                if len(split) == 2:
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

        if not package.eula:
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
        self.package.appinfo.save()

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


def show():
    window = AppInfoDialog()
    center_window(window)
    window.show()
    return window


def main(argv):
    import paf
    app = QtGui.QApplication(argv)
    window = show()
    window.load_package(paf.Package(argv[1]))
    return app.exec_()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
