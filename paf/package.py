# -*- coding: utf-8 -*-

from os.path import exists, isdir, isfile, join, abspath
import os
import config
from utils import ini_defined, path_insensitive, _S as _
from languages import lng
from shutil import copy2 as copy
from paf import PAFException


class Package:
    current_package = None

    _mandatory_dirs = [
            ('App',),
            ('App', 'AppInfo'),
            ('Other',),
            ('Other', 'Source'),
    ]

    _mandatory_files = [
            ('help.html',),
            ('App', 'AppInfo', 'appinfo.ini'),
            ('App', 'AppInfo', 'appicon.ico'),
            ('App', 'AppInfo', 'appicon_16.png'),
            ('App', 'AppInfo', 'appicon_32.png'),
    ]

    _recommended_dirs = [
            ('Other', 'Help'),
            ('Other', 'Help', 'Images'),
    ]

    @property
    def _recommended_files(self):
        files = []
        if not self.launcher_is_pal:
            # With PAL we expect to use the app template which includes all of
            # these values, so we make it errors.
            files += [
                # Always used, so recommended, but not in spec so not mandatory
                ('App', 'readme.txt'),
                ('Other', 'Help', 'Images', 'help_logo_top.png'),
                ('Other', 'Help', 'Images', 'favicon.ico'),
                ('Other', 'Help', 'Images', 'donation_button.png'),
                ('Other', 'Help', 'Images', 'help_background_footer.png'),
                ('Other', 'Help', 'Images', 'help_background_header.png'),
                ('Other', 'Source', 'Readme.txt'),
                ('Other', 'Source', 'License.txt')]
        return files

    _suggested_files = [
            ('App', 'AppInfo', 'appicon_128.png'),
    ]

    _pal_dirs = [
            ('App', 'AppInfo', 'Launcher'),
    ]

    @property
    def _pal_files(self):
        files = [
            # Files from the template
            ('App', 'AppInfo', 'Launcher', 'splash.jpg'),
            ('App', 'readme.txt'),
            ('Other', 'Help', 'Images', 'donation_button.png'),
            ('Other', 'Help', 'Images', 'favicon.ico'),
            ('Other', 'Help', 'Images', 'help_background_footer.png'),
            ('Other', 'Help', 'Images', 'help_background_header.png'),
            ('Other', 'Help', 'Images', 'help_logo_top.png'),
            ('Other', 'Source', 'AppNamePortable.ini'),
            ('Other', 'Source', 'License.txt'),
            ('Other', 'Source', 'Readme.txt')]
        files.insert(0, ('App', 'AppInfo', 'Launcher', '%s.ini' % self.appid))
        return files

    @property
    def appid(self):
        if hasattr(self, 'appinfo') \
        and ini_defined(self.appinfo.Details):
            if ini_defined(self.appinfo.Details.AppID):
                return self.appinfo.Details.AppID
            # Compatibility with a former typo in the PAF spec
            elif ini_defined(self.appinfo.Details.AppId):
                return self.appinfo.Details.AppId
        else:
            return None

    def __init__(self, package, launcher_is_pal=None):
        Package.current_package = self
        self._directory = package

        if abspath(package) == join(config.ROOT_DIR, 'app-template'):
            # No-one's meant to know about this ;-)
            raise PAFException("Nice try. That's a skeleton package - it's " +
                    "not *meant* to be valid. Try somethin' else.")

        if not isdir(package):
            raise PAFException(_("Package directory does not exist!"))

        # Check if it's a plugin installer
        if isfile(self._path('Other', 'Source', 'plugininstaller.ini')):
            self.plugin = True
            self._mandatory_files[self._mandatory_files.index(('App',
                'AppInfo', 'appinfo.ini'))] = \
                        ('Other', 'Source', 'plugininstaller.ini')
        else:
            self.plugin = False

        if launcher_is_pal == None:
            # Auto-detect; new apps: yes. Old apps: no
            if isdir(self._path('App', 'AppInfo')):
                # App/AppInfo exists, what about App/AppInfo/Launcher?
                self.launcher_is_pal = isdir(self._path('App', 'AppInfo',
                    'Launcher'))
            else:
                # New app, so use PAL.
                self.launcher_is_pal = True
        elif launcher_is_pal in (True, False):
            self.launcher_is_pal = launcher_is_pal
        else:
            raise PAFException("Invalid value given for launcher_is_pal, " +
                "must be None, True or False.")

        self.validate()

    def _path(self, *path):
        return path_insensitive(join(self._directory, *path))

    def _dirlist(self, recommended=False):
        dirlist = self._mandatory_dirs
        if recommended:
            filelist += self._recommended_dirs
        if self.launcher_is_pal:
            dirlist += self._pal_dirs
        return dirlist

    def fix_missing_directories(self):
        for dirname in self._dirlist(recommended=True):
            dirpath = self._path(*dirname)
            if exists(dirpath):
                if isdir(dirpath):
                    pass  # Directory exists, fine.
                else:
                    raise PAFException(_('%s should be a directory but a ' +
                        'file with that name already exists') % join(*dirname))
            else:
                os.mkdir(dirpath)

    def _filelist(self, recommended=False):
        filelist = self._mandatory_files
        if recommended:
            filelist += self._recommended_files
        if self.launcher_is_pal:
            filelist += self._pal_files
        return filelist

    def fix_missing_files(self):
        for filename in self._filelist(recommended=True):
            filepath = self._path(*filename)
            if exists(filepath):
                if isfile(filepath):
                    pass  # File exists, fine.
                else:
                    raise PAFException(_('%s should be a file but a ' +
                    'directory with that name already exists') %
                    join(*filename))
            elif isfile(join(config.ROOT_DIR, 'app-template', *filename)):
                copy(join(config.ROOT_DIR, 'app-template', *filename),
                        filepath)

    def fix(self):
        self.fix_missing_directories()
        self.fix_missing_files()
        self.validate()

    def validate(self):
        """
        Validate or revalidate the package to check PortableApps.com Format™
        compliance.
        """

        self.init_appinfo()

        self.errors = []
        self.warnings = []
        self.info = []

        if not self.launcher_is_pal:
            self.info.append(lng.NOT_USING_PAL)

        for directory in self._dirlist():
            if not isdir(self._path(*directory)):
                self.errors.append(lng.DIRECTORY_MISSING % join(*directory))

        for filename in self._filelist():
            if isdir(os.path.dirname(self._path(*filename))) and \
            not isfile(self._path(*filename)):
                self.errors.append(lng.FILE_MISSING % join(*filename))

        for directory in self._recommended_dirs:
            if not isdir(self._path(*directory)):
                self.warnings.append(lng.DIRECTORY_MISSING % join(*directory))

        for filename in self._recommended_files:
            if isdir(os.path.dirname(self._path(*filename))) and \
            not isfile(self._path(*filename)):
                self.warnings.append(lng.FILE_MISSING % join(*filename))

        for filename in self._suggested_files:
            if isdir(os.path.dirname(self._path(*filename))) and \
            not isfile(self._path(*filename)):
                self.info.append(lng.SUGGESTED_FILE_MISSING % join(*filename))

        self.validate_appinfo()


def create_package(path):
    "Create an app package in PortableApps.com Format™"
    if exists(path):
        if isdir(path):
            pass  # Directory exists, fine.
        else:
            raise PAFException(lng.FILE_NOT_DIRECTORY)
    else:
        raise PAFException(lng.DIRECTORY_NOT_EXIST)

    if os.listdir(path):
        raise PAFException(lng.DIRECTORY_NOT_EMPTY)

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
