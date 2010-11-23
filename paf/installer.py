# -*- coding: utf-8 -*-

# This file is for App/AppInfo/installer.ini validation

from os import makedirs, remove
from os.path import isfile, isdir
import sys
from subprocess import Popen, PIPE
from functools import wraps
import re
import iniparse
from orderedset import OrderedSet
from languages import LANG
from paf import PAFException
import config

__all__ = ['Installer']


def _valid_installer(func):
    "A decorator to ensure installer is set up."
    @wraps(func)
    def decorate(self, *args, **kwargs):
        try:
            if not self._path:
                raise Exception()
            if not self.ini:
                raise Exception()
        except:  # Could potentially be Exception or NameError
            # Naturally though this should never happen.
            raise PAFException(LANG.GENERAL.PACKAGE_NOT_INITIALISED)

        func(self, *args, **kwargs)

    return decorate


class Installer(object):
    "The manager for the app info (installer.ini)."

    _sections = OrderedSet(('CheckRunning', 'Source', 'MainDirectories',
        'OptionalComponents', 'CopyLocalFiles', 'DownloadFiles', 'Languages',
        'DirectoriesToPreserve', 'DirectoriesToRemove', 'FilesToPreserve',
        'FilesToRemove'))

    _keys = dict(
            CheckRunning=OrderedSet(('CloseEXE', 'CloseName')),
            Source=OrderedSet(('IncludeInstallerSource')),
            MainDirectories=OrderedSet(('RemoveAppDirectory',
                'RemoveDataDirectory', 'RemoveOtherDirectory')),
            OptionalComponents=OrderedSet(('OptionalComponents',
                'MainSectionTitle', 'MainSectionDescription',
                'OptionalSectionTitle', 'OptionalSectionDescription',
                'OptionalSectionSelectedInstallType',
                'OptionalSectionNotSelectedInstallType',
                'OptionalSectionPreSelectedIfNonEnglishInstall',
                'OptionalSectionInstalledWhenSilent', 'OptionalDirectory\d+',
                'OptionalFile\d+')),
            CopyLocalFiles=OrderedSet(('CopyLocalFiles', 'CopyFromRegPath',
                'CopyFromRegKey', 'CopyFromRegRemoveDirectories',
                'CopyFromDirectory', 'CopyToDirectory')),
            DownloadFiles=OrderedSet(('DownloadURL', 'DownloadName',
                'DownloadFilename', 'DownloadMD5', 'DownloadTo',
                'AdditionalInstallSize', 'Extract\d+To', 'Extract\d+File',
                'AdvancedExtract\d+To', 'AdvancedExtract\d+Filter',
                'DoubleExtractFilename', 'DoubleExtract\d+To',
                'DoubleExtract\d+Filter')),
            Languages=OrderedSet(('ENGLISH', 'AFRIKAANS', 'ALBANIAN', 'ARABIC',
                'BASQUE', 'BELARUSIAN', 'BOSNIAN', 'BRETON', 'BULGARIAN',
                'CATALAN', 'CIBEMBA', 'CROATIAN', 'CZECH', 'DANISH', 'DUTCH',
                'EFIK', 'ESPERANTO', 'ESTONIAN', 'FARSI', 'FINNISH', 'FRENCH',
                'GALICIAN', 'GEORGIAN', 'GERMAN', 'GREEK', 'HEBREW',
                'HUNGARIAN', 'ICELANDIC', 'IGBO', 'INDONESIAN', 'IRISH',
                'ITALIAN', 'JAPANESE', 'KHMER', 'KOREAN', 'KURDISH', 'LATVIAN',
                'LITHUANIAN', 'LUXEMBOURGISH', 'MACEDONIAN', 'MALAGASY',
                'MALAY', 'MONGOLIAN', 'NORWEGIAN', 'NORWEGIANNYNORSK',
                'PASHTO', 'POLISH', 'PORTUGUESE', 'PORTUGUESEBR', 'ROMANIAN',
                'RUSSIAN', 'SERBIAN', 'SERBIANLATIN', 'SIMPCHINESE', 'SLOVAK',
                'SLOVENIAN', 'SPANISH', 'SPANISHINTERNATIONAL', 'SWAHILI',
                'SWEDISH', 'THAI', 'TRADCHINESE', 'TURKISH', 'UKRAINIAN',
                'UZBEK', 'VALENCIAN', 'VIETNAMESE', 'WELSH', 'YORUBA')),
            DirectoriesToPreserve=OrderedSet(('PreserveDirectory\d+')),
            DirectoriesToRemove=OrderedSet(('RemoveDirectory\d+')),
            FilesToPreserve=OrderedSet(('PreserveFile\d+')),
            FilesToRemove=OrderedSet(('RemoveFile\d+')),
            )

    def __init__(self, package):
        self.package = package
        self.errors = []
        self.warnings = []
        self.info = []
        self.ini = None
        self._path = ''

    def load(self, do_reload=True):
        "Load installer.ini."
        if not do_reload and self.ini:
            return

        if self.package.plugin:
            self._path = self.package.path('Other', 'Source',
                    'plugininstaller.ini')
        else:
            self._path = self.package.path('App', 'AppInfo', 'installer.ini')

        self.ini = iniparse.INIConfig(open(self._path) \
                if isfile(self._path) else None)

    def validate(self):
        """
        Validate installer.ini and put the results into ``errors``,
        ``warnings`` and ``info`` in ``self``.
        """
        self.load(False)

        if not isfile(self._path):
            # If installer.ini doesn't exist, we've created an INIConfig which
            # will be empty, for the fix routine. Then as we don't want to spew
            # a whole heap of errors given that an error about installer.ini
            # being missing has already been added to the list, we'll give up.
            return

        ini = self.ini

        # TODO: style validation

        for extra in OrderedSet(ini) - self._sections:
            self.errors.append(LANG.INSTALLER.SECTION_EXTRA % extra)

        for section in self._sections & ini:
            for extra in ini[section]:
                if not any(re.match('%s$' % key, extra)
                        for key in self._keys[section]):
                    self.errors.append(LANG.INSTALLER.VALUE_EXTRA %
                            dict(section=section, key=extra))

    @_valid_installer
    def fix(self):
        "Some values in installer.ini can be fixed. This fixes such values."
        # TODO
        self.save()

    @_valid_installer
    def save(self):
        "Save the current state in installer.ini"

        if not len(list(self.ini)):
            # There's no content
            if isfile(self._path):
                # Don't write it empty, delete it
                remove(self._path)
            else:
                # Doesn't exist and nothing to write.
                return

        # Tidy it so when sections get added and removed and whatnot it looks
        # generally decent (no multiple blank lines, EOL at EOF)
        iniparse.tidy(self.ini)

        # Make sure the directory exists (Package.fix might potentially not
        # have been called?)
        if self.package.plugin:
            installer_dir = self.package.path('Other', 'Source')
        else:
            installer_dir = self.package.path('App', 'AppInfo')
        if not isdir(installer_dir):
            makedirs(installer_dir)

        # Now write it
        installer = open(self._path, 'w')
        installer.write(unicode(self.ini))
        installer.close()

    def build(self):
        """
        Builds the PortableApps.com Installer.

        Raises an ``OSError`` if run on Linux/OS X and Wine is not installed.

        Returns True on success, or False if either the PortableApps.com
        Installer was not found or the installer fails to build.
        """

        installer_path = config.get('Main', 'InstallerPath')
        if not installer_path or not isfile(installer_path):
            return False

        package_path = self.package.path()
        # On Linux we can execute it with a Linux path, as Wine will take care
        # of that, but it still expects a Windows path out the other side. Use
        # winepath to convert it to the right Windows path.
        if sys.platform != 'win32':
            # Blocking call; throws an OSError if winepath isn't found
            package_path = Popen(['winepath', '-w', package_path],
                    stdout=PIPE).communicate()[0].strip()

        full_target = self.package.path('..', self.filename)
        # Make sure it's not there from a previous build.
        if isfile(full_target):
            remove(full_target)

        Popen([installer_path, package_path]).wait()

        return isfile(full_target)

    @property
    def filename(self):
        """Get the filename (sans directories) of the installer."""
        self.load(False)
        if self.package.plugin:
            filename = self.package.appinfo.ini.Details.PluginName
        else:
            filename = self.package.appid

        filename += '_%s' % self.package.appinfo.ini.Version.DisplayVersion

        # Assume it's there, it'd be a blocking error otherwise
        language = self.package.appinfo.ini.Details.Language
        if language != 'Multilingual':
            filename += '_%s' % language

        filename = filename.replace(' ', '_') \
                .replace('(', '') \
                .replace(')', '') \
                .replace('[', '') \
                .replace(']', '') \
                .replace('~', '-') \
                .replace('&', '-') \
                .replace('#', '-') \
                .replace('"', '-') \
                .replace('*', '-') \
                .replace('/', '_') \
                .replace('\\', '_') \
                .replace(':', '.') \
                .replace('<', '-') \
                .replace('>', '-') \
                .replace('?', '') \
                .replace('|', '-') \
                .replace('=', '-') \
                .replace(',', '.') \
                .replace(';', '.') \
                .replace('+', 'Plus')

        if 'DownloadURL' in self.ini.DownloadFiles:
            filename += '_online'

        return '%s.paf.exe' % filename
