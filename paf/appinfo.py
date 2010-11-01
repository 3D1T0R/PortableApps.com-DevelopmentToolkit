# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

from os import makedirs
from os.path import exists, isfile, isdir
from utils import ini_defined
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
            if not self.appinfo:
                raise Exception()
        except:  # Could potentially be Exception or NameError
            # Naturally though this should never happen.
            raise PAFException(LANG.PACKAGE_NOT_INITIALISED)

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
        self.appinfo = None
        self._path = ''

    def load(self):
        "Load appinfo.ini."
        if self.package.plugin:
            self._path = self.package.path('Other', 'Source',
                    'plugininstaller.ini')
        else:
            self._path = self.package.path('App', 'AppInfo', 'appinfo.ini')

        self.appinfo = iniparse.INIConfig(open(self._path) \
                if isfile(self._path) else None)

    def validate(self):
        """
        Validate the appinfo and put the results into ``errors``, ``warnings``
        and ``info`` in ``self``.
        """
        if not self.appinfo:
            self.load()

        if not isfile(self._path):
            # If appinfo.ini doesn't exist, we've created an INIConfig which
            # will be empty, for the fix routine. Then as we don't want to spew
            # a whole heap of errors given that an error about appinfo.ini
            # being missing has already been added to the list, we'll give up.
            return

        appinfo = self.appinfo

        # TODO: style validation

        for missing in self._sections_required - OrderedSet(appinfo):
            self.errors.append(LANG.APPINFO_SECTION_MISSING % missing)

        for extra in OrderedSet(appinfo) \
        - self._sections_required - self._sections_optional:
            self.errors.append(LANG.APPINFO_SECTION_EXTRA % extra)

        for section in (self._sections_required | self._sections_optional) & \
                appinfo:
            # The Control section validation comes later as its
            # required/optional values are based on the value of Icons
            if section == 'Control':
                continue

            for missing in self._keys_required[section] - appinfo[section]:
                self.errors.append(LANG.APPINFO_VALUE_MISSING %
                    dict(section=section, key=missing))

            for extra in OrderedSet(appinfo[section]) \
            - self._keys_required[section] - self._keys_optional[section]:
                self.errors.append(LANG.APPINFO_VALUE_EXTRA %
                    dict(section=section, key=extra))

        if ini_defined(appinfo.Format):
            if appinfo.Format.Type != 'PortableApps.comFormat':
                self.errors.append(LANG.APPINFO_BAD_FORMAT_TYPE)

            if appinfo.Format.Version != FORMAT_VERSION:
                if appinfo.Format.Version in ('0.90', '0.91', '1.0'):
                    self.warnings.append(LANG.APPINFO_OLD_FORMAT_VERSION
                    % dict(old_version=appinfo.Format.Version,
                        current_version=FORMAT_VERSION))
                else:
                    self.errors.append(LANG.APPINFO_BAD_FORMAT_VERSION
                            % FORMAT_VERSION)

        if ini_defined(appinfo.Details):
            # Name: no real validation
            if ini_defined(appinfo.Details.Name) and \
                    '&' in appinfo.Details.Name:
                self.warnings.append(LANG.APPINFO_DETAILS_NAME_AMP)

            # AppID
            if ini_defined(appinfo.Details.AppID) and \
            OrderedSet(appinfo.Details.AppID) - '0123456789.-+_' - \
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                self.errors.append(LANG.APPINFO_DETAILS_APPID_BAD)

            # Publisher: no validation

            # Homepage: no validation
            if ini_defined(appinfo.Details.Homepage) and \
            appinfo.Details.Homepage.lower().startswith('http://'):
                self.info.append(LANG.APPINFO_DETAILS_HOMEPAGE_HTTP)

            # Category
            if ini_defined(appinfo.Details.Category) and \
                    appinfo.Details.Category not in ('Accessibility',
                            'Development', 'Education', 'Games',
                            'Graphics & Pictures', 'Internet', 'Music & Video',
                            'Office', 'Security', 'Utilities'):
                self.errors.append(LANG.APPINFO_DETAILS_CATEGORY_BAD)

            # Description: length
            if ini_defined(appinfo.Details.Description):
                chars = len(appinfo.Details.Description)
                if chars > 512:
                    self.errors.append(
                            LANG.APPINFO_DETAILS_DESCRIPTION_TOO_LONG)
                elif chars > 150:
                    self.warnings.append(LANG.APPINFO_DETAILS_DESCRIPTION_LONG
                            % chars)

            # Language
            if ini_defined(appinfo.Details.Language) and \
            appinfo.Details.Language not in ('Multilingual', 'Afrikaans',
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
                self.errors.append(LANG.APPINFO_DETAILS_LANGUAGE_BAD)

            # Trademarks: no validation

            # InstallType: no validation

            # PluginType: only applicable for self.plugin == True
            if ini_defined(appinfo.Details.PluginType):
                if not self.package.plugin:
                    self.errors.append(
                            LANG.APPINFO_DETAILS_PLUGINTYPE_NOT_PLUGIN)
                elif appinfo.Details.PluginType != 'CommonFiles':
                    self.errors.append(
                            LANG.APPINFO_DETAILS_PLUGINTYPE_BAD)

        if ini_defined(appinfo.License):
            for key in ('Shareable', 'OpenSource', 'Freeware',
                    'CommercialUse'):
                if ini_defined(appinfo.License[key]) and \
                appinfo.License[key] not in ('true', 'false'):
                    self.errors.append(LANG.APPINFO_BOOL_BAD %
                    dict(section='License', key=key))

            eula = self.package.eula
            if ini_defined(appinfo.License.EULAVersion) and not eula:
                self.errors.append(LANG.APPINFO_LICENSE_EULAVERSION_NO_EULA
                % dict(eula=eula))

        if ini_defined(appinfo.Version):
            if ini_defined(appinfo.Version.PackageVersion):
                try:
                    if len(map(int,
                            appinfo.Version.PackageVersion.split('.'))) != 4:
                        raise ValueError
                except ValueError:
                    self.errors.append(LANG.APPINFO_VERSION_PACKAGEVERSION_BAD)
            # DisplayVersion: no validation yet (TODO)

        if ini_defined(appinfo.SpecialPaths):
            if not ini_defined(appinfo.SpecialPaths.Plugins):
                self.warnings.append(LANG.APPINFO_SPECIALPATHS_OMIT)
            elif appinfo.SpecialPaths.Plugins == 'NONE':
                self.warnings.append(LANG.APPINFO_OMIT_DEFAULT % dict(
                    section='SpecialPaths', key='Plugins', default='NONE'))
            elif not isdir(self.package.path(appinfo.SpecialPaths.Plugins)):
                self.errors.append(LANG.APPINFO_SPECIALPATHS_PLUGINS_BAD)

        if ini_defined(appinfo.Dependencies):
            if ini_defined(appinfo.Dependencies.UsesJava):
                if appinfo.Dependencies.UsesJava == 'false':
                    self.warnings.append(LANG.APPINFO_OMIT_DEFAULT %
                            dict(section='Dependencies', key='UsesJava',
                                default='false'))
                elif appinfo.Dependencies.UsesJava != 'true':
                    self.errors.append(LANG.APPINFO_DEPENDENCIES_JAVA_BAD)

            if ini_defined(appinfo.Dependencies.UsesDotNetVersion):
                if appinfo.Dependencies.UsesDotNetVersion == '':
                    self.warnings.append(LANG.APPINFO_OMIT_EMPTY %
                        dict(section='Dependencies', key='UsesDotNetVersion'))
                elif appinfo.Dependencies.UsesDotNetVersion \
                not in ('1.1', '2.0', '3.0', '3.5'):
                    self.warnings.append(
                    LANG.APPINFO_DEPENDENCIES_USESDOTNETVERSION_PROBABLY_BAD)
                else:
                    try:
                        map(int,
                            appinfo.Dependencies.UsesDotNetVersion.split('.'))
                    except ValueError:
                        self.errors.append(
                            LANG.APPINFO_DEPENDENCIES_USESDOTNETVERSION_BAD)

        if ini_defined(appinfo.Control):
            if ini_defined(appinfo.Control.Start):
                start = appinfo.Control.Start
                if '/' in start or '\\' in start:
                    self.warnings.append(
                        LANG.APPINFO_CONTROL_START_NO_SUBDIRS %
                        dict(section='Control', key='Start'))
                elif not isfile(self.package.path(start)):
                    self.errors.append(
                            LANG.APPINFO_CONTROL_FILE_NOT_EXIST %
                            dict(section='Control', key='Start'))

            if ini_defined(appinfo.Control.ExtractIcon) and \
            not isfile(self.package.path(appinfo.Control.ExtractIcon)):
                self.errors.append(LANG.APPINFO_CONTROL_FILE_NOT_EXIST %
                    dict(section='Control', key='ExtractIcon'))

            if ini_defined(appinfo.Control.Icons):
                control_required = OrderedSet(self._keys_required['Control'])
                control_optional = OrderedSet(self._keys_optional['Control'])
                try:
                    num = int(appinfo.Control.Icons)
                    if num < 1:
                        raise ValueError()
                    if num > 1:
                        for i in xrange(1, num + 1):
                            control_required.add('Start%d' % i)
                            control_required.add('Name%d' % i)
                            control_optional.add('ExtractIcon%d' % i)

                            if ini_defined(appinfo.Control['Start%d' % i]):
                                start = appinfo.Control['Start%d' % i]
                                if '/' in start or '\\' in start:
                                    self.warnings.append(
                                    LANG.APPINFO_CONTROL_START_NO_SUBDIRS
                                    %
                                    dict(section='Control', key='Start%d' % i))
                                elif not isfile(self.package.path(start)):
                                    self.errors.append(
                                        LANG.APPINFO_CONTROL_FILE_NOT_EXIST %
                                        dict(section='Control', key='Start%d' %
                                            i))

                            # NameN: no validation (see [Details]:Name)

                            if ini_defined(appinfo.Control['ExtractIcon%d'
                                % i]) and not isfile(self.package.path(
                                    appinfo.Control['ExtractIcon%d' % i])):
                                self.errors.append(
                                LANG.APPINFO_CONTROL_FILE_NOT_EXIST %
                                dict(section='Control',
                                    key='ExtractIcon%d' % i))

                except ValueError:
                    self.errors.append(LANG.APPINFO_CONTROL_ICONS_BAD)

                for missing in control_required - appinfo.Control:
                    self.errors.append(LANG.APPINFO_VALUE_MISSING %
                        dict(section='Control', key=missing))

                for extra in OrderedSet(appinfo.Control) \
                - control_required - control_optional:
                    self.errors.append(LANG.APPINFO_VALUE_EXTRA %
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
        iniparse.tidy(self.appinfo)

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
        appinfo.write(unicode(self.appinfo))
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
