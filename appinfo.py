# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from ui.appinfo import Ui_AppInfoDialog
from utils import center_window, ini_defined


class AppInfoDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AppInfoDialog, self).__init__(parent)
        self.ui = Ui_AppInfoDialog()
        self.ui.setupUi(self)

    def on_AppInfoDialog_accepted(self, *args):
        print 'on_AppInfoDialog_accepted', args

    def on_accepted(self, *args):
        print 'on_accepted', args

    def accepted(self, *args):
        print 'accepted', args

    def on_DisplayVersionType_currentIndexChanged(self, value):
        # Gets called twice: once with the index, once with a QString.
        if type(value) == int:
            return

        if str(value) == '(official release)':
            self.ui.DisplayVersionNum.setEnabled(False)
        else:
            self.ui.DisplayVersionNum.setEnabled(True)

    def load_package(self, package):
        self.package = package
        self.appinfo = appinfo = package.appinfo
        if ini_defined(appinfo.Details):
            self._load_set_value(self.ui.Name, appinfo.Details.Name)
            self._load_set_value(self.ui.AppID, appinfo.Details.AppID)
            self._load_set_value(self.ui.Publisher, appinfo.Details.Publisher)
            self._load_set_value(self.ui.Homepage, appinfo.Details.Homepage)
            self._load_set_value(self.ui.Category, appinfo.Details.Category)
            self._load_set_value(self.ui.Description, appinfo.Details.Description)
            self._load_set_value(self.ui.Language, appinfo.Details.Language)
            self._load_set_value(self.ui.Trademarks, appinfo.Details.Trademarks)

        if ini_defined(appinfo.License):
            self._load_set_value(self.ui.Shareable, appinfo.License.Shareable)
            self._load_set_value(self.ui.OpenSource, appinfo.License.OpenSource)
            self._load_set_value(self.ui.Freeware, appinfo.License.Freeware)
            self._load_set_value(self.ui.CommercialUse,
                    appinfo.License.CommercialUse)

        if ini_defined(appinfo.Version):
            if ini_defined(appinfo.Version.PackageVersion):
                pv = appinfo.Version.PackageVersion
                try:
                    pv = map(int, pv.split('.'))
                except ValueError:
                    pass
                else:
                    if len(pv) == 4:
                        self._load_set_value(self.ui.PackageVersion1, pv[0])
                        self._load_set_value(self.ui.PackageVersion2, pv[1])
                        self._load_set_value(self.ui.PackageVersion3, pv[2])
                        self._load_set_value(self.ui.PackageVersion4, pv[3])

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

                        self._load_set_value(self.ui.DisplayVersionBase, split[0])
                        self._load_set_value(self.ui.DisplayVersionType, target)
                        self._load_set_value(self.ui.DisplayVersionNum, split[1])
                        break
                else:
                    self._load_set_value(self.ui.DisplayVersionBase, dv)
                    self._load_set_value(self.ui.DisplayVersionType,
                            '(official release)')
                    # TODO: this may not be necessary
                    self.ui.DisplayVersionNum.setEnabled(False)

            if not package.eula_exists:
                self.ui.EULAVersion.setEnabled(False)
            self._load_set_value(self.ui.EULAVersion,
                    appinfo.Version.EULAVersion)

        # TODO: no Control section
        #if ini_defined(appinfo.Control):

        if ini_defined(appinfo.SpecialPaths):
            self._load_set_value(self.ui.PluginsPath,
                    appinfo.SpecialPaths.Plugins)

        if ini_defined(appinfo.Dependencies):
            self._load_set_value(self.ui.UsesJava,
                    appinfo.Dependencies.UsesJava)
            self._load_set_value(self.ui.UsesDotNetVersion,
                    appinfo.Dependencies.UsesDotNetVersion)

    def save_appinfo(self):
        package = self.package
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

        # TODO: no proper control of the Control section, dummy code
        if not ini_defined(appinfo.Control):
            appinfo.Control.Icons = 1
            appinfo.Control.Start = '%s.exe' % appinfo.Details.AppID

        if self.ui.PluginsPath.text():
            appinfo.SpecialPaths.Plugins = self.ui.PluginsPath.text()

        if self.ui.UsesJava.isChecked():
            appinfo.Dependencies.UsesJava = 'true'

        if self.ui.UsesDotNetVersion.currentText() != 'None':
            appinfo.Dependencies.UsesDotNetVersion = \
                    self.ui.UsesDotNetVersion.currentText()

        print 'Not saving appinfo, but here it is:'
        print '-----'
        print appinfo
        print '-----'

    def _load_set_value(self, field, value):
        if ini_defined(value):
            if isinstance(field, QtGui.QComboBox):
                index = field.findText(value)
                if index > -1:  # TODO: I've assumed invalid is -1?
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


def show():
    window = AppInfoDialog()
    center_window(window)
    window.show()
    return window

if __name__ == '__main__':
    import sys
    import paf
    app = QtGui.QApplication(sys.argv)
    window = show()
    window.load_package(paf.Package(sys.argv[1]))
    exit_code = app.exec_()
    window.save_appinfo()
    sys.exit(exit_code)
