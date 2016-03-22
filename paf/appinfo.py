# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini management and validation

from os.path import join
from languages import LANG
from paf import PAFException
from functools import wraps

import os
import sys
from orderedset import OrderedSet
from paf import FORMAT_VERSION, CATEGORIES, LANGUAGES
from validator.engine.factory import bool_check
from validator.engine import (INIManager, SectionValidator, FileMeta, SectionMeta,
        ValidatorError, ValidatorWarning, ValidatorInfo, RegExMapping)


__all__ = ['AppInfo', 'valid_appid']


def valid_ini(func):
    "A decorator to ensure the INI file is set up."
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not (getattr(self, '_path', False) and getattr(self, 'ini', False)):
            # Naturally though this should never happen.
            raise PAFException(LANG.GENERAL.PACKAGE_NOT_INITIALISED)

        func(self, *args, **kwargs)

    return decorate


class AppInfo(INIManager):
    "The manager for the app info (appinfo.ini)."

    module = sys.modules[__name__]

    class Meta(FileMeta):
        mandatory = OrderedSet(('Format', 'Details', 'License', 'Version', 'Control'))
        optional = OrderedSet(('SpecialPaths', 'Dependencies'))
        order = OrderedSet(('Format', 'Details', 'License', 'Version', 'SpecialPaths', 'Dependencies', 'Control'))
        enforce_order = True

    def path(self):
        if self.package.plugin:
            return join('Other', 'Source', 'plugininstaller.ini')
        else:
            return join('App', 'AppInfo', 'appinfo.ini')


def valid_appid(appid):
    "Check if an AppID is valid and correct it. Returns (valid, appid)."

    valid_characters = set('0123456789.-+_ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
            'abcdefghijklmnopqrstuvwxyz')

    new = appid.replace(' ', '')
    new = new.replace('(', '')
    new = new.replace(')', '')
    new = new.replace('[', '')
    new = new.replace(']', '')
    new = new.replace('~', '-')
    new = new.replace('&', '+')
    new = new.replace('#', '+')
    new = new.replace('"', '')
    new = new.replace('*', '+')
    new = new.replace('/', '_')
    new = new.replace('\\', '_')
    new = new.replace(':', '.')
    new = new.replace('<', '-')
    new = new.replace('>', '-')
    new = new.replace('?', '')
    new = new.replace('|', '-')
    new = new.replace('=', '-')
    new = new.replace(',', '.')
    new = new.replace(';', '.')

    i = 0
    while i < len(new):
        if new[i] not in valid_characters:
            # Cut out the character
            new = new[:i] + new[i + 1:]
        else:
            i += 1

    if appid != new:
        return False, new
    else:
        return True, appid


# -------- INI Validation --------
#

class Format(SectionValidator):
    class Meta(SectionMeta):
        mandatory = OrderedSet(('Type', 'Version'))
        order = OrderedSet(('Type', 'Version'))

    def Type(self, value):
        if value != 'PortableApps.comFormat':
            return ValidatorError(LANG.APPINFO.BAD_FORMAT_TYPE)

    def Version(self, value):
        if value != FORMAT_VERSION:
            if value < FORMAT_VERSION:
                return ValidatorWarning(LANG.APPINFO.OLD_FORMAT_VERSION
                    % dict(old_version=value, current_version=FORMAT_VERSION))
            else:
                return ValidatorError(LANG.APPINFO.BAD_FORMAT_VERSION
                    % dict(version=FORMAT_VERSION))


class Details(SectionValidator):
    class Meta(SectionMeta):
        mandatory = OrderedSet(('Name', 'AppID', 'Publisher', 'Homepage', 'Category', 'Description'))
        optional = OrderedSet(('Language', 'Donate', 'Trademarks', 'InstallType', 'PluginType'))
        order = OrderedSet(('Name', 'AppID', 'Publisher', 'Homepage', 'Donate', 'Category', 'Description',
            'Language', 'Trademarks', 'PluginType', 'InstallType'))

    # Name: no validation

    def AppID(self, value):
        if OrderedSet(value) - '0123456789.-+_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            return ValidatorError(LANG.APPINFO.DETAILS_APPID_BAD)

    # Publisher: no validation

    # Homepage: no real validation

    def Homepage(self, value):
        if value.lower().startswith('http://'):
            return ValidatorInfo(LANG.APPINFO.DETAILS_NO_HTTP % dict(key='Homepage'))

    # Donate: again, no real validation
    # TODO: warn if Donate is missing that it should be there if possible
    def Donate(self, value):
        if value.lower().startswith('http://'):
            return ValidatorInfo(LANG.APPINFO.DETAILS_NO_HTTP % dict(key='Donate'))

    def Category(self, value):
        if value not in CATEGORIES:
            return ValidatorError(LANG.APPINFO.DETAILS_CATEGORY_BAD)

    def Description(self, value):
        chars = len(value)
        if chars > 512:
            return ValidatorError(LANG.APPINFO.DETAILS_DESCRIPTION_TOO_LONG)
        elif chars > 150:
            return ValidatorWarning(LANG.APPINFO.DETAILS_DESCRIPTION_LONG % dict(chars=chars))

    def Language(self, value):
        if value not in LANGUAGES:
            return ValidatorError(LANG.APPINFO.DETAILS_LANGUAGE_BAD)

    # Trademarks: no validation

    # InstallType: no validation

    def PluginType(self, value):
        # Only applicable for package.plugin == True
        if not self.package.plugin:
            return ValidatorError(LANG.APPINFO.DETAILS_PLUGINTYPE_NOT_PLUGIN)
        elif value != 'CommonFiles':
            return ValidatorError(LANG.APPINFO.DETAILS_PLUGINTYPE_BAD)


class License(SectionValidator):
    class Meta(SectionMeta):
        mandatory = OrderedSet(('Shareable', 'OpenSource', 'Freeware', 'CommercialUse'))
        optional = OrderedSet(('EULAVersion',))
        order = OrderedSet(('Shareable', 'OpenSource', 'Freeware', 'CommercialUse', 'EULAVersion'))

    Shareable = bool_check('License', 'Shareable')
    OpenSource = bool_check('License', 'OpenSource')
    Freeware = bool_check('License', 'Freeware')
    CommercialUse = bool_check('License', 'CommercialUse')

    def EULAVersion(self, value):
        if not self.package.eula:
            if self.package.plugin:
                eula = os.path.join('Other', 'Source', 'PluginEULA')
            else:
                eula = os.path.join('Other', 'Source', 'EULA')

            return ValidatorError(LANG.APPINFO.LICENSE_EULAVERSION_NO_EULA
            % dict(eula=eula))


class Version(SectionValidator):
    class Meta(SectionMeta):
        mandatory = OrderedSet(('PackageVersion', 'DisplayVersion'))
        order = OrderedSet(('PackageVersion', 'DisplayVersion'))

    def PackageVersion(self, value):
        try:
            if len(map(int, value.split('.'))) != 4:
                raise ValueError()
        except ValueError:
            return ValidatorError(LANG.APPINFO.VERSION_PACKAGEVERSION_BAD)

    # DisplayVersion: no validation yet (TODO)


class SpecialPaths(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('Plugins',))
        order = OrderedSet(('Plugins',))

    def Plugins(self, value):
        if value == 'NONE':
            return ValidatorWarning(LANG.INIVALIDATOR.OMIT_DEFAULT % dict(filename=self.validator.path(),
                section='SpecialPaths', key='Plugins', default='NONE'))
        elif not os.path.isdir(self.package.path(value)):
            return ValidatorError(LANG.APPINFO.SPECIALPATHS_PLUGINS_BAD)


class Dependencies(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('UsesGhostscript', 'UsesJava', 'UsesDotNetVersion'))
        order = OrderedSet(('UsesGhostscript', 'UsesJava', 'UsesDotNetVersion'))

    def UsesGhostscript(self, value):
        if value == 'no':
            return ValidatorWarning(LANG.INIVALIDATOR.OMIT_DEFAULT %
                    dict(filename=self.validator.path(), section='Dependencies', key='UsesGhostscript',
                        default='no'))
        elif value not in ('yes', 'optional'):
            return ValidatorError(LANG.APPINFO.DEPENDENCIES_USESGHOSTSCRIPT_BAD)

    def UsesJava(self, value):
        if value == 'no':
            return ValidatorWarning(LANG.INIVALIDATOR.OMIT_DEFAULT %
                    dict(filename=self.validator.path(), section='Dependencies', key='UsesJava',
                        default='no'))
        elif value in ('true', 'false'):
            if value == 'true':
                new_value = 'yes'
            elif value == 'false':
                new_value = 'no'
            return ValidatorError(LANG.INIVALIDATOR.VALUE_DEPRECATED %
                    dict(filename=self.validator.path(),section='Dependencies', key='UsesJava',
                        old_value=value, new_value=new_value))
        elif value not in ('yes', 'optional'):
            return ValidatorError(LANG.APPINFO.DEPENDENCIES_USESJAVA_BAD)

    def UsesDotNetVersion(self, value):
        if value not in ('1.1', '2.0', '3.0', '3.5', '4.0'):
            return ValidatorWarning(LANG.APPINFO.DEPENDENCIES_USESDOTNETVERSION_PROBABLY_BAD)
        else:
            try:
                map(int, value.split('.'))
            except ValueError:
                return ValidatorError(LANG.APPINFO.DEPENDENCIES_USESDOTNETVERSION_BAD)


class Control(SectionValidator):
    class Meta(SectionMeta):
        # TODO: what does self mean here?
        def __icons(self):
            """Gets the value of [Control]:Icons, or 1 if unset or invalid."""
            if 'Icons' not in self.parent.ini.Control:
                return 1
            icons = self.parent.ini.Control.Icons
            try:
                return int(icons)
            except ValueError:
                return 1

        @property
        def mandatory(self):
            base = ['Icons', 'Start']
            icons = self.__icons()
            if icons > 1:
                return OrderedSet(base +
                        ['Start%i' % i for i in xrange(1, icons + 1)] +
                        ['Name%i' % i for i in xrange(1, icons + 1)])
            return OrderedSet(base)

        @property
        def optional(self):
            base = ['ExtractIcons']
            icons = self.__icons()
            if icons > 1:
                return OrderedSet(base + ['ExtractIcon%i' % i for i in xrange(1, icons + 1)])
            return OrderedSet(base)

        @property
        def order(self):
            result = ['Icons', 'Start', 'ExtractIcon']
            icons = self.__icons()
            if icons > 1:
                for i in xrange(1, icons + 1):
                    result.append('Start%i')
                    result.append('Name%i')
                    result.append('ExtractIcon%i')
            return OrderedSet(result)

        mappings = (
                RegExMapping('Start[1-9]\d*$', 'Start'),
                RegExMapping('ExtractIcon[1-9]\d*$', 'ExtractIcon'),
                #RegExMapping('Name[1-9]\d*$'), 'Name_'), # no validation
                )

    def Start(self, value):
        if '/' in value or '\\' in value:
            return ValidatorWarning(LANG.APPINFO.CONTROL_START_NO_SUBDIRS %
                    dict(section='Control', key='Start'))
        elif not os.path.isfile(self.package.path(value)):
            return ValidatorError(LANG.APPINFO.CONTROL_FILE_NOT_EXIST %
                    dict(section='Control', key='Start'))

    def ExtractIcon(self, value):
        if not os.path.isfile(self.package.path(value)):
            return ValidatorError(LANG.APPINFO.CONTROL_FILE_NOT_EXIST %
                    dict(section='Control', key='ExtractIcon'))
        else:
            return ValidatorWarning(LANG.APPINFO.CONTROL_EXTRACTICON_OMIT_UNLESS_REQUIRED)

    def Icons(self, value):
        try:
            value = int(value)
            if value < 1:
                raise ValueError()
        except ValueError:
            return ValidatorError(LANG.APPINFO.CONTROL_ICONS_BAD)
