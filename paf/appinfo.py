# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

from os import makedirs
from os.path import exists, isfile, isdir, join
from languages import LANG
import iniparse
from paf import FORMAT_VERSION, PAFException
from orderedset import OrderedSet
from functools import wraps

__all__ = ['AppInfo', 'valid_appid']


def _valid_appinfo(func):
    "A decorator to ensure appinfo is set up."
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


class AppInfo(object):
    "The manager for the app info (appinfo.ini)."

    _sections_required = OrderedSet(('Format', 'Details', 'License', 'Version',
                                    'Control'))
    _sections_optional = OrderedSet(('SpecialPaths', 'Dependencies'))
    _keys_required = dict(
            Format=OrderedSet(('Type', 'Version')),
            Details=OrderedSet(('Name', 'AppID', 'Publisher', 'Homepage',
                                'Category', 'Description', 'Language')),
            License=OrderedSet(('Shareable', 'OpenSource', 'Freeware',
                                'CommercialUse')),
            Version=OrderedSet(('PackageVersion', 'DisplayVersion')),
            SpecialPaths=OrderedSet(),
            Dependencies=OrderedSet(),
            Control=OrderedSet(('Icons', 'Start')),
            # Control: also StartN and NameN for 1 to Icons if Icons > 1
            )
    _keys_optional = dict(
            Format=OrderedSet(),
            Details=OrderedSet(('Trademarks', 'InstallType', 'PluginType')),
            # PluginType is only valid for self.plugin == True, validated later
            License=OrderedSet(('EULAVersion',)),
            Version=OrderedSet(),
            SpecialPaths=OrderedSet(('Plugins',)),
            Dependencies=OrderedSet(('UsesJava', 'UsesDotNetVersion')),
            Control=OrderedSet(('ExtractIcon',)),
            # Control: also ExtractIconN for 1 to Icons if Icons > 1
            )

    def __init__(self, package):
        self.package = package
        self.errors = []
        self.warnings = []
        self.info = []
        self.ini = None
        self._path = ''

    def load(self, do_reload=True):
        "Load appinfo.ini."
        if not do_reload and self.ini:
            return

        if self.package.plugin:
            self._path = self.package.path('Other', 'Source',
                    'plugininstaller.ini')
        else:
            self._path = self.package.path('App', 'AppInfo', 'appinfo.ini')

        self.ini = iniparse.INIConfig(open(self._path) \
                if isfile(self._path) else None)

    def validate(self):
        """
        Validate the appinfo and put the results into ``errors``, ``warnings``
        and ``info`` in ``self``.
        """
        self.load(False)

        if not isfile(self._path):
            # If appinfo.ini doesn't exist, we've created an INIConfig which
            # will be empty, for the fix routine. Then as we don't want to spew
            # a whole heap of errors given that an error about appinfo.ini
            # being missing has already been added to the list, we'll give up.
            return

        ini = self.ini

        # TODO: style validation

        for missing in self._sections_required - OrderedSet(ini):
            self.errors.append(LANG.APPINFO.SECTION_MISSING % missing)

        for extra in OrderedSet(ini) \
        - self._sections_required - self._sections_optional:
            self.errors.append(LANG.APPINFO.SECTION_EXTRA % extra)

        for section in (self._sections_required | self._sections_optional) & \
                ini:
            # The Control section validation comes later as its
            # required/optional values are based on the value of Icons
            if section == 'Control':
                continue

            for missing in self._keys_required[section] - ini[section]:
                self.errors.append(LANG.APPINFO.VALUE_MISSING %
                    dict(section=section, key=missing))

            for extra in OrderedSet(ini[section]) \
            - self._keys_required[section] - self._keys_optional[section]:
                self.errors.append(LANG.APPINFO.VALUE_EXTRA %
                    dict(section=section, key=extra))

        # [Format]

        if ini.Format.Type != 'PortableApps.comFormat':
            self.errors.append(LANG.APPINFO.BAD_FORMAT_TYPE)

        if ini.Format.Version != FORMAT_VERSION:
            if ini.Format.Version in ('0.90', '0.91', '0.9.8', '1.0'):
                self.warnings.append(LANG.APPINFO.OLD_FORMAT_VERSION
                % dict(old_version=ini.Format.Version,
                    current_version=FORMAT_VERSION))
            else:
                self.errors.append(LANG.APPINFO.BAD_FORMAT_VERSION
                        % FORMAT_VERSION)

        # [Details]

        # Name: no real validation
        if 'Name' in ini.Details and '&' in ini.Details.Name:
            self.warnings.append(LANG.APPINFO.DETAILS_NAME_AMP)

        # AppID
        if 'AppID' in ini.Details and \
        OrderedSet(ini.Details.AppID) - '0123456789.-+_' - \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            self.errors.append(LANG.APPINFO.DETAILS_APPID_BAD)

        # Publisher: no validation

        # Homepage: no validation
        if 'Homepage' in ini.Details and \
        ini.Details.Homepage.lower().startswith('http://'):
            self.info.append(LANG.APPINFO.DETAILS_HOMEPAGE_HTTP)

        # Category
        if 'Category' in ini.Details and \
                ini.Details.Category not in ('Accessibility',
                        'Development', 'Education', 'Games',
                        'Graphics & Pictures', 'Internet', 'Music & Video',
                        'Office', 'Security', 'Utilities'):
            self.errors.append(LANG.APPINFO.DETAILS_CATEGORY_BAD)

        # Description: length
        if 'Description' in ini.Details:
            chars = len(ini.Details.Description)
            if chars > 512:
                self.errors.append(
                        LANG.APPINFO.DETAILS_DESCRIPTION_TOO_LONG)
            elif chars > 150:
                self.warnings.append(LANG.APPINFO.DETAILS_DESCRIPTION_LONG
                        % chars)

        # Language
        if 'Language' in ini.Details and \
        ini.Details.Language not in ('Multilingual', 'Afrikaans',
                'Albanian', 'Arabic', 'Armenian', 'Basque', 'Belarusian',
                'Bosnian', 'Breton', 'Bulgarian', 'Catalan', 'Cibemba',
                'Croatian', 'Czech', 'Danish', 'Dutch', 'Efik', 'English',
                'Estonian', 'Farsi', 'Finnish', 'French', 'Galician',
                'Georgian', 'German', 'Greek', 'Hebrew', 'Hungarian',
                'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian',
                'Japanese', 'Khmer', 'Korean', 'Kurdish', 'Latvian',
                'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy',
                'Malay', 'Mongolian', 'Norwegian', 'NorwegianNynorsk',
                'Pashto', 'Polish', 'Portuguese', 'PortugueseBR',
                'Romanian', 'Russian', 'Serbian', 'SerbianLatin',
                'SimpChinese', 'Slovak', 'Slovenian', 'Spanish',
                'SpanishInternational', 'Swahili', 'Swedish', 'Thai',
                'TradChinese', 'Turkish', 'Ukranian', 'Uzbek', 'Valencian',
                'Vietnamese', 'Welsh', 'Yoruba'):
            # Language names omitted, it would be too long otherwise.
            self.errors.append(LANG.APPINFO.DETAILS_LANGUAGE_BAD)

        # Trademarks: no validation

        # InstallType: no validation

        # PluginType: only applicable for self.plugin == True
        if 'PluginType' in ini.Details:
            if not self.package.plugin:
                self.errors.append(
                        LANG.APPINFO.DETAILS_PLUGINTYPE_NOT_PLUGIN)
            elif ini.Details.PluginType != 'CommonFiles':
                self.errors.append(
                        LANG.APPINFO.DETAILS_PLUGINTYPE_BAD)

        # [License]

        for key in ('Shareable', 'OpenSource', 'Freeware',
                'CommercialUse'):
            if key in ini.License and \
            ini.License[key] not in ('true', 'false'):
                self.errors.append(LANG.APPINFO.BOOL_BAD %
                dict(section='License', key=key))

        eula = self.package.eula
        if 'EULAVersion' in ini.License and not eula:
            if self.package.plugin:
                eula = join('Other', 'Source', 'PluginEULA')
            else:
                eula = join('Other', 'Source', 'EULA')

            self.errors.append(LANG.APPINFO.LICENSE_EULAVERSION_NO_EULA
            % dict(eula=eula))

        # [Version]

        if 'PackageVersion' in ini.Version:
            try:
                if len(map(int,
                        ini.Version.PackageVersion.split('.'))) != 4:
                    raise ValueError
            except ValueError:
                self.errors.append(LANG.APPINFO.VERSION_PACKAGEVERSION_BAD)
        # DisplayVersion: no validation yet (TODO)

        # [SpecialPaths]

        if 'SpecialPaths' in ini:
            if 'Plugins' not in ini.SpecialPaths:
                self.warnings.append(LANG.APPINFO.SPECIALPATHS_OMIT)
            elif ini.SpecialPaths.Plugins == 'NONE':
                self.warnings.append(LANG.APPINFO.OMIT_DEFAULT % dict(
                    section='SpecialPaths', key='Plugins', default='NONE'))
            elif not isdir(self.package.path(ini.SpecialPaths.Plugins)):
                self.errors.append(LANG.APPINFO.SPECIALPATHS_PLUGINS_BAD)

        # [Dependencies]

        if 'UsesJava' in ini.Dependencies:
            if ini.Dependencies.UsesJava == 'false':
                self.warnings.append(LANG.APPINFO.OMIT_DEFAULT %
                        dict(section='Dependencies', key='UsesJava',
                            default='false'))
            elif ini.Dependencies.UsesJava != 'true':
                self.errors.append(LANG.APPINFO.DEPENDENCIES_JAVA_BAD)

        if 'UsesDotNetVersion' in ini.Dependencies:
            if ini.Dependencies.UsesDotNetVersion == '':
                self.warnings.append(LANG.APPINFO.OMIT_EMPTY %
                    dict(section='Dependencies', key='UsesDotNetVersion'))
            elif ini.Dependencies.UsesDotNetVersion \
            not in ('1.1', '2.0', '3.0', '3.5'):
                self.warnings.append(
                LANG.APPINFO.DEPENDENCIES_USESDOTNETVERSION_PROBABLY_BAD)
            else:
                try:
                    map(int,
                        ini.Dependencies.UsesDotNetVersion.split('.'))
                except ValueError:
                    self.errors.append(
                        LANG.APPINFO.DEPENDENCIES_USESDOTNETVERSION_BAD)

        # [Control]

        if 'Start' in ini.Control:
            start = ini.Control.Start
            if '/' in start or '\\' in start:
                self.warnings.append(
                    LANG.APPINFO.CONTROL_START_NO_SUBDIRS %
                    dict(section='Control', key='Start'))
            elif not isfile(self.package.path(start)):
                self.errors.append(
                        LANG.APPINFO.CONTROL_FILE_NOT_EXIST %
                        dict(section='Control', key='Start'))

        if 'ExtractIcon' in ini.Control and \
        not isfile(self.package.path(ini.Control.ExtractIcon)):
            self.errors.append(LANG.APPINFO.CONTROL_FILE_NOT_EXIST %
                dict(section='Control', key='ExtractIcon'))

        if 'Icons' in ini.Control:
            control_required = OrderedSet(self._keys_required['Control'])
            control_optional = OrderedSet(self._keys_optional['Control'])
            try:
                num = int(ini.Control.Icons)
                if num < 1:
                    raise ValueError()
                if num > 1:
                    for i in xrange(1, num + 1):
                        control_required.add('Start%d' % i)
                        control_required.add('Name%d' % i)
                        control_optional.add('ExtractIcon%d' % i)

                        if 'Start%d' % i in ini.Control:
                            start = ini.Control['Start%d' % i]
                            if '/' in start or '\\' in start:
                                self.warnings.append(
                                LANG.APPINFO.CONTROL_START_NO_SUBDIRS
                                %
                                dict(section='Control', key='Start%d' % i))
                            elif not isfile(self.package.path(start)):
                                self.errors.append(
                                    LANG.APPINFO.CONTROL_FILE_NOT_EXIST %
                                    dict(section='Control', key='Start%d' %
                                        i))

                        # NameN: no validation (see [Details]:Name)

                        if 'ExtractIcon%d' % i in ini.Control and \
                                not isfile(self.package.path(
                                    ini.Control['ExtractIcon%d' % i])):
                            self.errors.append(
                            LANG.APPINFO.CONTROL_FILE_NOT_EXIST %
                            dict(section='Control',
                                key='ExtractIcon%d' % i))

            except ValueError:
                self.errors.append(LANG.APPINFO.CONTROL_ICONS_BAD)

            for missing in control_required - ini.Control:
                self.errors.append(LANG.APPINFO.VALUE_MISSING %
                    dict(section='Control', key=missing))

            for extra in OrderedSet(ini.Control) \
            - control_required - control_optional:
                self.errors.append(LANG.APPINFO.VALUE_EXTRA %
                    dict(section='Control', key=extra))

    @_valid_appinfo
    def fix(self):
        "Some values in appinfo.ini can be fixed. This fixes such values."
        # TODO
        self.save()

    @_valid_appinfo
    def save(self):
        "Save the current state in appinfo.ini"

        # Tidy it so when sections get added and removed and whatnot it looks
        # generally decent (no multiple blank lines, EOL at EOF)
        iniparse.tidy(self.ini)

        # Make sure the directory exists (Package.fix might potentially not
        # have been called?)
        if self.package.plugin:
            appinfo_dir = self.package.path('Other', 'Source')
        else:
            appinfo_dir = self.package.path('App', 'AppInfo')
        if not exists(appinfo_dir):
            makedirs(appinfo_dir)

        # Now write it
        appinfo = open(self._path, 'w')
        appinfo.write(unicode(self.ini))
        appinfo.close()


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
