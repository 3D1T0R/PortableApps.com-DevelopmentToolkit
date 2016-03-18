import os
from PyQt4 import QtCore, QtGui
from ._base import WindowPage
from ..ui.pageoptions import Ui_PageOptions
import config
from utils import _, path_local


def _options_path_finder(thing):
    def wrapped(self, mode=None):
        path = config.get('Main', thing + 'Path')
        if mode == 'silent' and path is not None:
            return path

        if mode == 'browse' or not path or not os.path.isfile(path):
            # Try intelligently guessing if in PAF structure
            portableapps_dir = os.path.dirname(
                    config.ROOT_DIR.rpartition(
                        os.path.sep + 'App' + os.path.sep)[0])
            path = os.path.join(portableapps_dir,
                    'PortableApps.com' + thing,
                    'PortableApps.com%s.exe' % thing)
            if not os.path.isfile(path):
                path = os.path.join(portableapps_dir,
                    'PortableApps.com' + thing,
                    'PortableApps.com%sGenerator.exe' % thing)
            if mode == 'silent':
                return path if portableapps_dir and os.path.isfile(path) else ''
            if mode == 'browse' or not portableapps_dir or not os.path.isfile(path):
                path = path_local(QtGui.QFileDialog.getOpenFileName(self,
                        _('Select the path to the PortableApps.com ' + thing),
                        config.ROOT_DIR,
                        'PortableApps.com %s (PortableApps.com%s.exe)' % (thing,
                        thing)) if not thing == "Launcher" else QtGui.QFileDialog.getOpenFileName(self,
                        _('Select the path to the PortableApps.com ' + thing),
                        config.ROOT_DIR,
                        'PortableApps.com %s (PortableApps.com%s.exe PortableApps.com%sGenerator.exe)' % (thing,
                        thing, thing)))

            if path and os.path.isfile(path):
                config.settings.Main[thing + 'Path'] = path
            elif not mode == 'browse':
                QtGui.QMessageBox.critical(self,
                        _('PortableApps.com Development Toolkit'),
                        _('Unable to locate the PortableApps.com %s.' % thing),
                        QtGui.QMessageBox.Ok)
                return
        return path
    wrapped.func_name = wrapped.__name__ = 'find_%s_path' % thing.lower()
    return wrapped


class PageOptions(WindowPage, Ui_PageOptions):
    find_installer_path = _options_path_finder('Installer')
    find_launcher_path = _options_path_finder('Launcher')
    find_appcompactor_path = _options_path_finder('AppCompactor')

    def enter(self):
        self.installer.setText(self.find_installer_path('silent'))
        self.launcher.setText(self.find_launcher_path('silent'))
        self.appcompactor.setText(self.find_appcompactor_path('silent'))

    def leave(self, closing=False):
        config.settings.Main.InstallerPath = self.installer.text()
        config.settings.Main.LauncherPath = self.launcher.text()
        config.settings.Main.AppCompactorPath = self.appcompactor.text()

    @QtCore.Slot()
    def on_installer_browse_clicked(self):
        """PortableApps.com Installer Path."""
        text_box = self.installer
        current_path = text_box.text()
        text_box.setText(self.find_installer_path('browse') or current_path)

    @QtCore.Slot()
    def on_launcher_browse_clicked(self):
        """PortableApps.com Launcher Path."""
        text_box = self.launcher
        current_path = text_box.text()
        text_box.setText(self.find_launcher_path('browse') or current_path)

    @QtCore.Slot()
    def on_appcompactor_browse_clicked(self):
        """PortableApps.com AppCompactor Path."""
        text_box = self.appcompactor
        current_path = text_box.text()
        text_box.setText(self.find_appcompactor_path('browse') or current_path)
