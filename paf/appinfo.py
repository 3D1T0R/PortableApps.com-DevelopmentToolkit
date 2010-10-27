# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

from package import Package
from os.path import isfile, isdir, join
from utils import ini_defined, method_of, _S as _
import iniparse
from paf import FORMAT_VERSION, PAFException
from orderedset import OrderedSet

__all__ = []

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
        # PluginType is only valid for self.plugin == True, validated later.
        License=OrderedSet(('EULAVersion',)),
        Version=OrderedSet(),
        SpecialPaths=OrderedSet(('Plugins',)),
        Dependencies=OrderedSet(('UsesJava', 'UsesDotNetVersion')),
        Control=OrderedSet(('ExtractIcon',)),
        # Control: also ExtractIconN for 1 to Icons if Icons > 1
        )


def valid_appinfo(fn):
    "A decorator to ensure appinfo is set up."
    def decorate(self, *args, **kwargs):
        try:
            if not self.appinfo_path:
                raise Exception()
            if not self.appinfo:
                raise Exception()
        except:  # Could potentially be Exception or NameError
            # Naturally though this should never happen.
            raise PAFException('Package has not been properly initialised.')

        fn(self, *args, **kwargs)

    return decorate


@method_of(Package)
def init_appinfo(self):
    if self.plugin:
        self.appinfo_path = self._path('Other', 'Source',
                'plugininstaller.ini')
    else:
        self.appinfo_path = self._path('App', 'AppInfo', 'appinfo.ini')

    if isfile(self.appinfo_path):
        fp = open(self.appinfo_path)
    else:
        fp = None

    appinfo = iniparse.INIConfig(fp)
    self.appinfo = appinfo


@method_of(Package)
def validate_appinfo(self):
    if not hasattr(self, 'appinfo') or not self.appinfo:
        self.init_appinfo()

    if not isfile(self.appinfo_path):
        # If appinfo.ini doesn't exist, we've created an INIConfig which will
        # be empty, for the fix routine. Then as we don't want to spew a whole
        # heap of errors given that an error about appinfo.ini being missing
        # has already been added to the list, we'll give up.
        return

    appinfo = self.appinfo

    # TODO: style validation

    for missing in _sections_required - OrderedSet(appinfo):
        self.errors.append(_('appinfo.ini: required section %s is missing') %
                missing)

    for extra in OrderedSet(appinfo) \
    - _sections_required - _sections_optional:
        self.errors.append(_('appinfo.ini: invalid section %s') % extra)

    for section in (_sections_required | _sections_optional) & appinfo:
        # The Control section validation comes later as its required/optional
        # values are based on the value of Icons
        if section == 'Control':
            continue

        for missing_value in _keys_required[section] - set(appinfo[section]):
            self.errors.append(_('appinfo.ini: [%(section)s], ' +
                'required value %(key)s is missing') %
                dict(section=section, key=missing_value))

        for extra_value in OrderedSet(appinfo[section]) \
        - _keys_required[section] - _keys_optional[section]:
            self.errors.append(_('appinfo.ini: [%(section)s], ' +
                'invalid value %(key)s') %
                dict(section=section, key=extra_value))

    if ini_defined(appinfo.Format):
        if appinfo.Format.Type != 'PortableApps.comFormat':
            self.errors.append(_('appinfo.ini: [Format]:Type is not ' +
                'PortableApps.comFormat'))

        if appinfo.Format.Version != FORMAT_VERSION:
            if appinfo.Format.Version in ('0.90', '0.91', '1.0'):
                self.warnings.append(_('appinfo.ini: [Format]:Version needs ' +
                'to be updated from %(old_version)s to %(current_version)s')
                % dict(old_version=appinfo.Format.Version,
                    current_version=FORMAT_VERSION))
            else:
                self.errors.append(_('appinfo.ini: [Format]:Version is not %s')
                        % FORMAT_VERSION)

    if ini_defined(appinfo.Details):
        # Name: no real validation
        if ini_defined(appinfo.Details.Name) and '&' in appinfo.Details.Name:
            self.warnings.append(_('appinfo.ini: [Details]:Name should not ' +
                'contain & as it is generally misinterpreted as an accesskey'))

        # AppID
        if ini_defined(appinfo.Details.AppID) and
        OrderedSet(appinfo.Details.AppID) - \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-+_':
            self.errors.append(_('appinfo.ini: [Details]:AppID contains ' +
                'invalid characters; only letters, numbers, and the ' +
                'following punctuation: .-+_ are allowed'))

        # Publisher: no validation

        # Homepage: no validation
        if ini_defined(appinfo.Details.Homepage) and
        appinfo.Details.Homepage.lower().startswith('http://'):
            self.info.append(_('appinfo.ini: [Details]:Homepage does not ' +
                'need to start with http://'))

        # Category
        if ini_defined(appinfo.Details.Category) and appinfo.Details.Category \
                not in ('Accessibility', 'Development', 'Education', 'Games',
                        'Graphics & Pictures', 'Internet', 'Music & Video',
                        'Office', 'Security', 'Utilities'):
            self.errors.append(_('appinfo.ini: [Details]:Category must be ' +
                'exactly Accessibility, Development, Education, Games, ' +
                'Graphics & Pictures, Internet, Music & Video, Office, ' +
                'Security or Utilities'))

        # Description: length
        if ini_defined(appinfo.Details.Description):
            chars = len(appinfo.Details.Description)
            if chars > 512:
                self.errors.append(_('appinfo.ini: [Details]:Description ' +
                    'may not be longer than 512 characters.'))
            elif chars > 150:
                self.warnings.append(_('appinfo.ini: [Details]:Description ' +
                    'should be shorter than %s characters ' +
                    '(aim for no more than 150).') % chars)

        # Language
        if ini_defined(appinfo.Details.Language) and appinfo.Details.Language
        not in ('Multilingual', 'Afrikaans', 'Albanian', 'Arabic', 'Armenian',
                'Basque', 'Belarusian', 'Bosnian', 'Breton', 'Bulgarian',
                'Catalan', 'Cibemba', 'Croatian', 'Czech', 'Danish', 'Dutch',
                'Efik', 'English', 'Estonian', 'Farsi', 'Finnish', 'French',
                'Galician', 'Georgian', 'German', 'Greek', 'Hebrew',
                'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish',
                'Italian', 'Japanese', 'Khmer', 'Korean', 'Kurdish', 'Latvian',
                'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy',
                'Malay', 'Mongolian', 'Norwegian', 'NorwegianNynorsk',
                'Pashto', 'Polish', 'Portuguese', 'PortugueseBR', 'Romanian',
                'Russian', 'Serbian', 'SerbianLatin', 'SimpChinese', 'Slovak',
                'Slovenian', 'Spanish', 'SpanishInternational', 'Swahili',
                'Swedish', 'Thai', 'TradChinese', 'Turkish', 'Ukranian',
                'Uzbek', 'Valencian', 'Vietnamese', 'Welsh', 'Yoruba'):
            # Language names omitted, it would be too long otherwise.
            self.errors.append(_('appinfo.ini: [Details]:Language is invalid' +
                ', it should be "Multilingual" or one of the valid language ' +
                'names'))

        # Trademarks: no validation

        # InstallType: no validation

        # PluginType: only applicable for self.plugin == True
        if ini_defined(appinfo.Details.PluginType):
            if not self.plugin:
                self.errors.append(_('appinfo.ini: [Details]:PluginType is ' +
                'only valid for plugin installers.'))
            elif appinfo.Details.PluginType != 'CommonFiles':
                self.errors.append(_('appinfo.ini: [Details]:PluginType is ' +
                'invalid, it should be "CommonFiles" or omitted.'))

    if ini_defined(appinfo.License):
        for key in ('Shareable', 'OpenSource', 'Freeware', 'CommercialUse'):
            if ini_defined(appinfo.License[key]) and
            appinfo.License[key] not in ('true', 'false'):
                self.errors.append(_('appinfo.ini: [%(section)s]:%(key)s ' +
                'must be "true" or "false"') %
                dict(section='License', key=key))

        if self.plugin:
            eula_path = join('Other', 'Source', 'PluginEULA')
        else:
            eula_path = join('Other', 'Source', 'EULA')

        if ini_defined(appinfo.License.EULAVersion) and
        not isfile(self._path('%s.rtf' % eula_path)) and
        not isfile(self._path('%s.txt' % eula_path)):
            self.errors.append(_('appinfo.ini: [License]:EULAVersion is ' +
            'defined but neither %(eula)s.rtf nor %(eula)s.txt exists')
            % dict(eula=eula_path))

    if ini_defined(appinfo.Version):
        if ini_defined(appinfo.Version.PackageVersion):
            try:
                if len(map(int, appinfo.Version.PackageVersion.split('.'))) \
                        != 4:
                    raise ValueError
            except ValueError:
                self.errors.append(_('appinfo.ini: [Version]:PackageVersion ' +
                    'must be an X.X.X.X version number'))
        # DisplayVersion: no validation yet; TODO some reasonable validation

    if ini_defined(appinfo.SpecialPaths):
        if not ini_defined(appinfo.SpecialPaths.Plugins):
            self.warnings.append(_('appinfo.ini: [SpecialPaths] section ' +
                'should be omitted if empty'))
        elif appinfo.SpecialPaths.Plugins == 'NONE':
            self.warnings.append(_('appinfo.ini: [SpecialPaths]:Plugins ' +
                'should be omitted if set to NONE'))
        elif not isdir(self._path(appinfo.SpecialPaths.Plugins)):
            self.errors.append(_('appinfo.ini: [SpecialPaths]:Plugins must ' +
                'be the path to a directory in the package'))

    if ini_defined(appinfo.Dependencies):
        if ini_defined(appinfo.Dependencies.UsesJava):
            if appinfo.Dependencies.UsesJava == 'false':
                self.warnings.append(_('appinfo.ini: [Dependencies]:UsesJava' +
                    ' should be omitted if set to false'))
            elif appinfo.Dependencies.UsesJava != 'true':
                self.errors.append(_('appinfo.ini: [Dependencies]:UsesJava ' +
                    'should be "true" or omitted'))

        if ini_defined(appinfo.Dependencies.UsesDotNetVersion):
            if appinfo.Dependencies.UsesDotNetVersion == '':
                self.warnings.append(_('appinfo.ini: ' +
                '[Dependencies]:UsesDotNetVersion should be omitted if empty'))
            elif appinfo.Dependencies.UsesDotNetVersion \
            not in ('1.1', '2.0', '3.0', '3.5'):
                self.warnings.append(_('appinfo.ini: ' +
                '[Dependencies]:UsesDotNetVersion should probably be unset ' +
                'or 1.1, 2.0, 3.0 or 3.5; you probably have an invalid value'))
            else:
                try:
                    map(int, appinfo.Dependencies.UsesDotNetVersion.split('.'))
                except ValueError:
                    self.errors.append(_('appinfo.ini: ' +
                    '[Dependencies]:UsesDotNetVersion should be unset or a '
                    '.NET version like 1.1, 2.0, 3.0 or 3.5'))

    if ini_defined(appinfo.Control):
        if ini_defined(appinfo.Control.Start):
            start = appinfo.Control.Start
            if '/' in start or '\\' in start:
                self.warnings.append(_('appinfo.ini: [%(section)s]:%(key)s ' +
                ' should not include subdirectories') %
                dict(section='Control', key='Start'))
            elif not isfile(self._path(start)):
                self.errors.append(_('appinfo.ini: the file specified in ' +
                '[%(section)s]:%(key)s does not exist') %
                dict(section='Control', key='Start'))

        if ini_defined(appinfo.Control.ExtractIcon) and
        not isfile(self._path(appinfo.Control.ExtractIcon)):
            self.errors.append(_('appinfo.ini: the file specified in ' +
            '[%(section)s]:%(key)s does not exist') %
            dict(section='Control', key='ExtractIcon'))

        if ini_defined(appinfo.Control.Icons):
            control_keys_required = OrderedSet(_keys_required['Control'])
            control_keys_optional = OrderedSet(_keys_optional['Control'])
            try:
                num = int(appinfo.Control.Icons)
                if num < 1:
                    raise ValueError
                if num > 1:
                    for i in xrange(1, num + 1):
                        control_keys_required.add('Start%d' % i)
                        control_keys_required.add('Name%d' % i)
                        control_keys_optional.add('ExtractIcon%d' % i)

                        if ini_defined(appinfo.Control['Start%d' % i]):
                            start = appinfo.Control['Start%d' % i]
                            if '/' in start or '\\' in start:
                                self.warnings.append(_('appinfo.ini: ' +
                                    '[%(section)s]:%(key)s should not ' +
                                    'include subdirectories') %
                                    dict(section='Control', key='Start%d' % i))
                            elif not isfile(self._path(start)):
                                self.errors.append(_('appinfo.ini: the file ' +
                                    'specified in [%(section)s]:%(key)s does' +
                                    ' not exist') %
                                    dict(section='Control', key='Start%d' % i))

                        # NameN: no validation (see [Details]:Name)

                        if ini_defined(appinfo.Control['ExtractIcon%d' % i]) \
                        and not isfile(self._path(
                        appinfo.Control['ExtractIcon%d' % i])):
                            self.errors.append(_('appinfo.ini: the file ' +
                            'specified in [%(section)s]:%(key)s does not ' +
                            'exist') %
                            dict(section='Control', key='ExtractIcon%d' % i))

            except ValueError:
                self.errors.append(_('appinfo.ini: [Control]:Icons must be a' +
                    ' number greater than 0'))

            for missing_value in control_keys_required - appinfo.Control:
                self.errors.append(_('appinfo.ini: [%(section)s], required ' +
                    'value %(key)s is missing') %
                    dict(section='Control', key=missing_value))

            for extra_value in OrderedSet(appinfo.Control) \
            - control_keys_required - control_keys_optional:
                self.errors.append(_('appinfo.ini: [%(section)s], invalid ' +
                    'value %(key)s') %
                    dict(section='Control', key=extra_value))


@method_of(Package)
@valid_appinfo
def fix_appinfo(self):
    "Some values in appinfo.ini can be fixed. This fixes such values."
    self.write_appinfo()


@method_of(Package)
@valid_appinfo
def write_appinfo(self):
    try:
        if not self.appinfo_path:
            raise Exception()
        if not self.appinfo:
            raise Exception()
    except:  # Could potentially be Exception or NameError
        # Naturally though this should never happen.
        raise PAFException('Package has not been properly initialised.')

    fp = open(self.appinfo_path, 'w')
    fp.write(appinfo)
    fp.close()
