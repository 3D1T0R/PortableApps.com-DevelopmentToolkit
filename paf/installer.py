# -*- coding: utf-8 -*-

# This file is for App/AppInfo/installer.ini validation

from os import remove
from os.path import isfile, join
import sys
from subprocess import Popen
import re
from orderedset import OrderedSet
from languages import LANG
import config
from utils import path_windows, ini_list_from_numbered
from validator.engine.factory import bool_check
from validator.engine import (INIManager, SectionValidator, FileMeta, SectionMeta,
        ValidatorError, ValidatorWarning)

__all__ = ['Installer']


class Installer(INIManager):
    "The manager for the app info (installer.ini)."

    module = sys.modules[__name__]

    class Meta(FileMeta):
        optional = OrderedSet(('CheckRunning', 'Source', 'MainDirectories', 'OptionalComponents',
            'CopyLocalFiles', 'DownloadFiles', 'Languages',
            'DirectoriesToPreserve', 'DirectoriesToRemove', 'FilesToPreserve', 'FilesToRemove'))
        order = OrderedSet(('CheckRunning', 'Source', 'MainDirectories', 'OptionalComponents',
            'CopyLocalFiles', 'DownloadFiles', 'Languages',
            'DirectoriesToPreserve', 'DirectoriesToRemove', 'FilesToPreserve', 'FilesToRemove'))
        #enforce_order = True

    # Kept until validation is finished (TODO)
    """
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
    """

    def path(self):
        if self.package.plugin:
            return join('Other', 'Source', 'plugininstaller.ini')
        else:
            return join('App', 'AppInfo', 'installer.ini')

    def build(self, block=True):
        """
        Builds the PortableApps.com Installer.

        Raises an ``OSError`` if run on Linux/OS X and Wine is not installed or
        PortableApps.comInstaller.exe does not have mode +x.

        Returns True on success, or False if either the
        PortableApps.com Installer was not found or the installer fails to
        build. If the parameter ``block`` is set to ``False``, this will be an
        asynchronous call and the ``subprocess.Popen`` process handle will be
        returned.
        """

        installer_path = config.get('Main', 'InstallerPath')
        if not installer_path or not isfile(installer_path):
            return False

        full_target = self.package.path('..', self.filename)
        # Make sure it's not there from a previous build.
        if isfile(full_target):
            remove(full_target)

        proc = Popen([installer_path, path_windows(self.package.path(), True)])
        if block:
            proc.wait()
            return isfile(full_target)
        else:
            return proc

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

    def optional_component_directories(self):
        """
        Get a list of directories in the optional component. Paths are relative
        to the base of the package (package.path()) and are in Windows form.
        """
        if self.ini.OptionalComponents.OptionalComponents != 'true':
            return []
        else:
            return ini_list_from_numbered(self.ini, 'OptionalComponents', 'OptionalDirectory%i')

    def optional_component_files(self):
        """
        Get a list of files in the optional component. Paths are relative to
        the base of the package (package.path()) and are in Windows form.
        """
        if self.ini.OptionalComponents.OptionalComponents != 'true':
            return []
        else:
            return ini_list_from_numbered(self.ini, 'OptionalComponents', 'OptionalFile%i')


class CheckRunning(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('CloseEXE', 'CloseName'))
        order = OrderedSet(('CloseEXE', 'CloseName'))

    def CloseEXE(self, value):
        if not value.endswith('.exe') and value != 'NONE':
            return ValidatorWarning(LANG.INSTALLER.CHECKRUNNING_CLOSEEXE_NOT_EXE % dict(filename=self.validator.path()))

    def CloseName(self, value):
        if self.package.appinfo.ini and self.package.appinfo.ini.Details.Name == value:
            return ValidatorWarning(LANG.INSTALLER.CLOSENAME_SAME_AS_APPINFO % dict(filename=self.validator.path()))


class Source(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('IncludeInstallerSource',))
        order = OrderedSet(('IncludeInstallerSource',))

    def IncludeInstallerSource(self, value):
        if value not in ('true', 'false'):
            return ValidatorError(LANG.INIVALIDATOR.BOOL_BAD %
                    dict(filename=self.validator.path(), section='Source', key='IncludeInstallerSource'))
        elif value == 'false':
            return ValidatorWarning(LANG.INIVALIDATOR.OMIT_DEFAULT %
                    dict(filename=self.validator.path(), section='Source', key='IncludeInstallerSource', default='false'))
        else:
            return ValidatorWarning(LANG.INSTALLER.INCLUDEINSTALLERSOURCE % dict(filename=self.validator.path()))


class MainDirectories(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('RemoveAppDirectory', 'RemoveDataDirectory', 'RemoveOtherDirectory'))
        order = OrderedSet(('RemoveAppDirectory', 'RemoveDataDirectory', 'RemoveOtherDirectory'))

    RemoveAppDirectory = bool_check('MainDirectories', 'RemoveAppDirectory', 'true')
    RemoveDataDirectory = bool_check('MainDirectories', 'RemoveDataDirectory', 'false')
    RemoveOtherDirectory = bool_check('MainDirectories', 'RemoveOther', 'true')


class OptionalComponents(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('OptionalComponents', 'MainSectionTitle', 'MainSectionDescription',
            'OptionalSectionTitle', 'OptionalSectionDescription', 'OptionalSectionSelectedInstallType',
            'OptionalSelectionNotSelectedInstallType', 'OptionalSelectionPreSelectedIfNotEnglish',
            'OptionalSectionInstalledWhenSilent',
            re.compile(r'OptionalDirectory[1-9]\d*'), re.compile(r'OptionalFile[1-9]\d*')))
        # TODO: order!

    def OptionalComponents(self, value):
        pass


# Notes for later:
# Need some way to have ``order`` et al. accept numbered things
# appinfo.ini:[Details]:Name is PluginName for self.package.plugin?
# appinfo.ini:[Details]:Name is PluginName for self.package.plugin?
# [MainDirectories]:* default to false for self.package.plugin
