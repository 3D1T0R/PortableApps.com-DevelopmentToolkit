#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qt import QtCore, QtGui, IS_PYSIDE
from ui.appinfo import Ui_AppInfoDialog
from utils import center_window, ini_defined
from paf.appinfo import valid_appid


class AppInfoDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AppInfoDialog, self).__init__(parent)
        self.ui = Ui_AppInfoDialog()
        self.ui.setupUi(self)
        # XXX The AppID validator is disabled for PySide because it causes a
        # Segmentation fault in PySide (0.4.2). Due to be fixed in the next
        # release.
        if not IS_PYSIDE:
            self.ui.AppID.setValidator(AppIDValidator())

    def accept(self):
        "User submits the form (presses Save). No validation at the moment."
        self.save()
        # Two buttons, Save and Close, let them press Close manually
        #self.close()

    @QtCore.Slot(unicode)
    def on_DisplayVersionType_currentIndexChanged(self, value):
        "Disable the DT/PR/revision number field for an official release."

        if value == '(official release)':
            self.ui.DisplayVersionNum.setEnabled(False)
        else:
            self.ui.DisplayVersionNum.setEnabled(True)

    @QtCore.Slot(unicode)
    def on_Name_textChanged(self, value):
        "Auto-fill some fields when the Name is changed."

        if hasattr(self.ui.Name, 'matched'):
            return
        value = unicode(value)
        if hasattr(self.ui.Name, 'backspacing'):
            self.ui.Name.last_value = value
            return

        # Deal with backspace and this auto-complete thing
        if hasattr(self.ui.Name, 'last_value') and \
                not hasattr(self.ui.Name, 'backspacing') and \
                value == self.ui.Name.last_value:
            self.ui.Name.backspacing = True
            # This does make Delete act as Backspace sometimes, but never mind.
            self.ui.Name.backspace()
            del self.ui.Name.backspacing
            return
        self.ui.Name.last_value = value

        # If the cursor is at the end of the line, and nothing is selected
        if self.ui.Name.cursorPosition() == len(value) and \
                not self.ui.Name.hasSelectedText():
            self.ui.Name.matched = False
            for suffix in ', Portable Edition', ' Portable':
                for end in [suffix[:i] for i in xrange(len(suffix), 0, -1)]:
                    if value.endswith(end):
                        self.ui.Name.matched = True
                        self.ui.Name.insert(suffix[len(end):])
                        # Unfortunately setCursorPosition doesn't make it so
                        # the cursor can be at the start of the selection
                        self.ui.Name.setSelection(len(value),
                                len(suffix) - len(end))
                        value = value + suffix[len(end):]
                        break
                if self.ui.Name.matched:
                    break
            #if not self.ui.Name.matched:
            #    self.ui.Name.matched = True
            #    end = ' Portable'
            #    self.ui.Name.insert(end)
            #    self.ui.Name.setSelection(len(value), len(end))
            #    value = value + end
            del self.ui.Name.matched

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

        if not (ini_defined(self.appinfo.Details) and
                ini_defined(self.appinfo.Details.AppID)) and \
        not self.ui.AppID.isModified():
            self.ui.AppID.setText(appid)

        if not (ini_defined(self.appinfo.Details) and
                ini_defined(self.appinfo.Details.Publisher)) and \
        not self.ui.Publisher.isModified():
            self.ui.Publisher.setText('%s team & PortableApps.com' % name)

        # Homepage: done by on_AppID_textChanged

        if not (ini_defined(self.appinfo.Details) and
                ini_defined(self.appinfo.Details.Description)) and \
        not self.ui.Description.isModified():
            self.ui.Description.setText('%s is a ___' % name)

    @QtCore.Slot(unicode)
    def on_AppID_textChanged(self, value):
        "Auto-fill Homepage when the Name is changed."

        if not (ini_defined(self.appinfo.Details) and
                ini_defined(self.appinfo.Details.Homepage)) and \
        not self.ui.Homepage.isModified():
            self.ui.Homepage.setText('PortableApps.com/%s' % unicode(value))

    def load_package(self, package):
        self.package = package
        self.appinfo = appinfo = package.appinfo.ini
        if ini_defined(appinfo.Details):
            self._fill(self.ui.Name, appinfo.Details.Name)
            self._fill(self.ui.AppID, appinfo.Details.AppID)
            self._fill(self.ui.Publisher, appinfo.Details.Publisher)
            self._fill(self.ui.Homepage, appinfo.Details.Homepage)
            self._fill(self.ui.Category, appinfo.Details.Category)
            self._fill(self.ui.Description, appinfo.Details.Description)
            self._fill(self.ui.Language, appinfo.Details.Language)
            self._fill(self.ui.Trademarks, appinfo.Details.Trademarks)

        if ini_defined(appinfo.License):
            self._fill(self.ui.Shareable, appinfo.License.Shareable)
            self._fill(self.ui.OpenSource, appinfo.License.OpenSource)
            self._fill(self.ui.Freeware, appinfo.License.Freeware)
            self._fill(self.ui.CommercialUse, appinfo.License.CommercialUse)

        if ini_defined(appinfo.Version):
            if ini_defined(appinfo.Version.PackageVersion):
                pv = appinfo.Version.PackageVersion
                try:
                    pv = map(int, pv.split('.'))
                except ValueError:
                    pass
                else:
                    if len(pv) == 4:
                        self._fill(self.ui.PackageVersion1, pv[0])
                        self._fill(self.ui.PackageVersion2, pv[1])
                        self._fill(self.ui.PackageVersion3, pv[2])
                        self._fill(self.ui.PackageVersion4, pv[3])

            # Split DisplayVersion into chunks
            if ini_defined(appinfo.Version.DisplayVersion):
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

                        self._fill(self.ui.DisplayVersionBase, split[0])
                        self._fill(self.ui.DisplayVersionType, target)
                        self._fill(self.ui.DisplayVersionNum, split[1])
                        break
                else:
                    self._fill(self.ui.DisplayVersionBase, dv)
                    self._fill(self.ui.DisplayVersionType,
                            '(official release)')
                    # TODO: this may not be necessary
                    self.ui.DisplayVersionNum.setEnabled(False)

            if not package.eula:
                self.ui.EULAVersion.setEnabled(False)
            self._fill(self.ui.EULAVersion, appinfo.Version.EULAVersion)

        # TODO: no Control section
        #if ini_defined(appinfo.Control):

        if ini_defined(appinfo.SpecialPaths):
            self._fill(self.ui.PluginsPath, appinfo.SpecialPaths.Plugins)

        if ini_defined(appinfo.Dependencies):
            self._fill(self.ui.UsesJava, appinfo.Dependencies.UsesJava)
            self._fill(self.ui.UsesDotNetVersion,
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

        appinfo.Details.Name = self.ui.Name.text()
        appinfo.Details.AppID = self.ui.AppID.text()
        appinfo.Details.Publisher = self.ui.Publisher.text()
        appinfo.Details.Homepage = self.ui.Homepage.text()
        appinfo.Details.Category = self.ui.Category.currentText()
        appinfo.Details.Description = self.ui.Description.text()
        appinfo.Details.Language = self.ui.Language.currentText()
        if self.ui.Trademarks.text():
            appinfo.Details.Trademarks = self.ui.Trademarks.text()

        b = lambda i: 'true' if i.isChecked() else 'false'

        appinfo.License.Shareable = b(self.ui.Shareable)
        appinfo.License.OpenSource = b(self.ui.OpenSource)
        appinfo.License.Freeware = b(self.ui.Freeware)
        appinfo.License.CommercialUse = b(self.ui.CommercialUse)

        if self.ui.EULAVersion.isEnabled() and self.ui.EULAVersion.text():
            appinfo.License.EULAVersion = self.ui.EULAVersion.text()

        appinfo.Version.PackageVersion = '.'.join(map(str, (
            self.ui.PackageVersion1.value(), self.ui.PackageVersion2.value(),
            self.ui.PackageVersion3.value(), self.ui.PackageVersion4.value())))

        dvtype = self.ui.DisplayVersionType.currentText()
        appinfo.Version.DisplayVersion = self.ui.DisplayVersionBase.text()
        if dvtype != '(official release)':
            appinfo.Version.DisplayVersion += ' ' + dvtype + ' ' + \
                    str(self.ui.DisplayVersionNum.value())

        if self.ui.PluginsPath.text():
            appinfo.SpecialPaths.Plugins = self.ui.PluginsPath.text()

        if self.ui.UsesJava.isChecked():
            appinfo.Dependencies.UsesJava = 'true'
        # If it was ticked before, remove it
        elif ini_defined(appinfo.Dependencies) and \
                ini_defined(appinfo.Dependencies.UsesJava):
            del appinfo.Dependencies.UsesJava

        if self.ui.UsesDotNetVersion.currentText() != 'None':
            appinfo.Dependencies.UsesDotNetVersion = \
                    self.ui.UsesDotNetVersion.currentText()
        # If it was set before, remove it
        elif ini_defined(appinfo.Dependencies) and \
                ini_defined(appinfo.Dependencies.UsesDotNetVersion):
            del appinfo.Dependencies.UsesDotNetVersion

        # Deleting the last value in the section doesn't delete the section at
        # the moment, so delete it manually
        if len(list(appinfo.Dependencies)) == 0:
            del appinfo.Dependencies

        # TODO: no proper control of the Control section, dummy code
        if not ini_defined(appinfo.Control):
            appinfo.Control.Icons = 1
            appinfo.Control.Start = '%s.exe' % appinfo.Details.AppID

    def _fill(self, field, value):
        if ini_defined(value):
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
