# -*- coding: utf-8 -*-

from os.path import exists, isdir, isfile, join
import os
import config
from utils import _S as _
from shutil import copy2 as copy

class PAFException(Exception): pass

class Package:
    _mandatory_dirs = (
            ('App',),
            ('App', 'AppInfo'),
            ('Other',),
            ('Other', 'Help'),
            ('Other', 'Help', 'Images'),
            ('Other', 'Source'),
    )

    _mandatory_files = (
            ('help.html',),
            ('App', 'readme.txt'),
            ('Other', 'Help', 'Images', 'help_logo_top.png'),
            ('Other', 'Help', 'Images', 'favicon.ico'),
            ('Other', 'Help', 'Images', 'donation_button.png'),
            ('Other', 'Help', 'Images', 'help_background_footer.png'),
            ('Other', 'Help', 'Images', 'help_background_header.png'),
    )

    _recommended_files = (
            ('Other', 'Source', 'Readme.txt'),
            ('Other', 'Source', 'License.txt'),
            ('Other', 'Source', 'AppNamePortable.ini'),
    )

    _pal_dirs = (
            ('App', 'AppInfo', 'Launcher'),
    )

    _pal_files = (
            ('App', 'AppInfo', 'Launcher', 'splash.jpg'),
    )

    def __init__(self, package, launcher_is_pal=None):
        self._directory = package

        if package == join(config.ROOT_DIR, 'app-template'):
            # No-one's meant to know about this ;-)
            raise PAFException("Nice try. That's a skeleton package - it's not *meant* to be valid. Try somethin' else.")

        if not isdir(package):
            raise PAFException(_("Package directory does not exist!"))

        if launcher_is_pal == None:
            # Auto-detect; new apps: yes. Old apps: no
            if isdir(self._path('App', 'AppInfo')):
                # App/AppInfo exists, what about App/AppInfo/Launcher?
                self.launcher_is_pal = isdir(self._path('App', 'AppInfo', 'Launcher'))
            else:
                # New app, so use PAL.
                self.launcher_is_pal = True
        elif launcher_is_pal in (True, False):
            self.launcher_is_pal = launcher_is_pal
        else:
            raise PAFException("Invalid value given for launcher_is_pal, must be None, True or False.")

        self.validate()

    def _path(self, *path):
        return join(self._directory, *path)

    def _dirlist(self):
        dirlist = Package._mandatory_dirs
        if self.launcher_is_pal:
            dirlist += Package._pal_dirs
        return dirlist

    def fix_missing_directories(self):
        for dirname in self._dirlist():
            dirpath = self._path(*dirname)
            if exists(dirpath):
                if isdir(dirpath):
                    pass # Directory exists, fine.
                else:
                    raise PAFException(_('%s should be a directory but a file with that name already exists') % join(*dirname))
            else:
                os.mkdir(dirpath)

    def _filelist(self, recommended=False):
        filelist = Package._mandatory_files
        if recommended:
            filelist += Package._recommended_files
        if self.launcher_is_pal:
            filelist += Package._pal_files
        return filelist

    def fix_missing_files(self):
        for filename in self._filelist(recommended=True):
            filepath = self._path(*filename)
            if exists(filepath):
                if isfile(filepath):
                    pass # File exists, fine.
                else:
                    raise PAFException(_('%s should be a file but a directory with that name already exists') % join(*filename))
            else:
                copy(join(config.ROOT_DIR, 'app-template', *filename), filepath)

    def fix(self):
        self.fix_missing_directories()
        self.fix_missing_files()
        self.validate()

    def validate(self):
        "Validate or revalidate the package to check PortableApps.com Format™ compliance."

        self.errors   = []
        self.warnings = []
        self.info     = []

        for directory in self._dirlist():
            if not isdir(self._path(*directory)):
                self.errors.append(_('Directory %s is missing') % join(*directory))

        for filename in self._filelist():
            if not isfile(self._path(*filename)):
                self.errors.append(_('File %s is missing') % join(*filename))

        for filename in Package._recommended_files:
            if not isfile(self._path(*filename)):
                self.warnings.append(_('File %s is missing') % join(*filename))

def create_package(path):
    "Create an app package in PortableApps.com Format™"
    if exists(path):
        if isdir(path):
            pass # Directory exists, fine.
        else:
            raise PAFException(_('You provided a file rather than a directory!'))
    else:
        raise PAFException(_('Package directory does not exist!'))

    if os.listdir(path):
        raise PAFException(_('The directory you specified is not empty. Please specify an empty directory.'))

    package = Package(path)
    package.fix()
    return package

def valid_package(path):
    """
    Method to check if a given directory is a PAF package.  At present this
    does nothing more than check that the path exists and is a directory. The
    Package class can fix up anything if it's got a directory.
    """
    return isdir(path)
