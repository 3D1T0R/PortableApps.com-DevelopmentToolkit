import sys
from orderedset import OrderedSet
from languages import LANG
from .engine.factory import bool_check
from .engine import (INIValidator, SectionValidator, FileMeta, SectionMeta,
        ValidatorError, ValidatorWarning, ValidatorInfo)


class InstallerValidator(INIValidator):
    module = sys.modules[__name__]
    @property
    def filename(self):
        if self.package.plugin:
            return r'Other\Source\plugininstaller.ini'
        else:
            return r'App\AppInfo\installer.ini'

    class Meta(FileMeta):
        optional = OrderedSet(('CheckRunning', 'Source', 'OptionalComponents', 'CopyLocalFiles', 'DownloadFiles',
            'Languages', 'DirectoriesToPreserve', 'DirectoriesToRemove', 'FilesToPreserve', 'FilesToRemove'))
        order = optional.copy()
        #enforce_order = True


class CheckRunning(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('CloseEXE', 'CloseName'))
        order = OrderedSet(('CloseEXE', 'CloseName'))

    def CloseEXE(self, value):
        if not value.endswith('.exe') and value != 'NONE':
            return ValidatorWarning(LANG.INSTALLER.CHECKRUNNING_CLOSEEXE_NOT_EXE % dict(filename=self.filename))

    def CloseName(self, value):
        if self.package.appinfo.ini and self.package.appinfo.ini.Details.Name == value:
            return ValidatorWarning(LANG.INSTALLER.CLOSENAME_SAME_AS_APPINFO % dict(filename=self.filename))


class Source(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('IncludeInstallerSource',))
        order = OrderedSet(('IncludeInstallerSource',))

    def IncludeInstallerSource(self, value):
        if value not in ('true', 'false'):
            return ValidatorError(LANG.INIVALIDATOR.BOOL_BAD %
                    dict(filename=self.filename, section='Source', key='IncludeInstallerSource'))
        elif value == 'false':
            return ValidatorWarning(LANG.INIVALIDATOR.OMIT_DEFAULT %
                    dict(filename=self.filename, section='Source', key='IncludeInstallerSource', default='false'))
        else:
            return ValidatorWarning(LANG.INSTALLER.INCLUDEINSTALLERSOURCE % dict(filename=self.filename))


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
