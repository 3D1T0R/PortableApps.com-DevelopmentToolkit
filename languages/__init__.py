"""
Language handling and i18n. With the exception of language files, ``LANG`` is
the only thing from this class which should be used. It's a proxy object which
gives the strings in the currently selected language.

Usage::

    from languages import LANG
    print LANG.SOME_STRING
"""

import config

__all__ = ['LANG']


class Language(object):
    "Base class for languages, with all strings defined (in English)."
    LANGUAGE_NAME = 'Unset'
    LANGUAGE_NAME_NATIVE = 'Unset'

    # Exceptions

    PACKAGE_NOT_INITIALISED = 'Package has not been properly initialised.'
    FILE_NOT_DIRECTORY = 'You provided a file rather than a directory!'
    DIRECTORY_NOT_EXIST = 'Package directory does not exist!'
    DIRECTORY_NOT_EMPTY = 'The directory you specified is not empty. Please specify an empty directory.'

    # Normal strings

    NOT_USING_PAL = 'The PortableApps.com Launcher is not used. Please consider using it.'

    DIRECTORY_MISSING = 'Directory %s is missing'
    FILE_MISSING = 'File %s is missing'
    SUGGESTED_FILE_MISSING = 'Suggested file %s is missing'

    # appinfo.ini

    APPINFO_SECTION_MISSING = 'appinfo.ini: required section %s is missing'
    APPINFO_SECTION_EXTRA = 'appinfo.ini: invalid section %s'
    APPINFO_VALUE_MISSING = 'appinfo.ini: [%(section)s], required value %(key)s is missing'
    APPINFO_VALUE_EXTRA = 'appinfo.ini: [%(section)s], invalid value %(key)s'

    # Generic messages:
    # Used in [License]
    APPINFO_BOOL_BAD = 'appinfo.ini: [%(section)s]:%(key)s must be "true" or "false"'
    # Used for [SpecialPaths]:Plugins, [Dependencies]:Java
    APPINFO_OMIT_DEFAULT = 'appinfo.ini: [%(section)s]:%(key)s should be omitted if set to %(default)s'
    APPINFO_OMIT_EMPTY = 'appinfo.ini: [%(section)s]:%(key)s should be omitted if empty'

    # [Format]
    APPINFO_BAD_FORMAT_TYPE = 'appinfo.ini: [Format]:Type is not PortableApps.comFormat'
    APPINFO_OLD_FORMAT_VERSION = 'appinfo.ini: [Format]:Version needs to be updated from %(old_version)s to %(current_version)s'
    APPINFO_BAD_FORMAT_VERSION = 'appinfo.ini: [Format]:Version is not %s'

    # [Details]
    APPINFO_DETAILS_NAME_AMP = 'appinfo.ini: [Details]:Name should not contain & as it is generally misinterpreted as an accesskey'
    APPINFO_DETAILS_APPID_BAD = 'appinfo.ini: [Details]:AppID contains invalid characters; only letters, numbers, and the following punctuation: .-+_ are allowed'
    APPINFO_DETAILS_HOMEPAGE_HTTP = 'appinfo.ini: [Details]:Homepage does not need to start with http://'
    APPINFO_DETAILS_CATEGORY_BAD = 'appinfo.ini: [Details]:Category must be exactly Accessibility, Development, Education, Games, Graphics & Pictures, Internet, Music & Video, Office, Security or Utilities'
    APPINFO_DETAILS_DESCRIPTION_TOO_LONG = 'appinfo.ini: [Details]:Description may not be longer than 512 characters.'
    APPINFO_DETAILS_DESCRIPTION_LONG = 'appinfo.ini: [Details]:Description should be shorter than %s characters (aim for no more than 150).'
    APPINFO_DETAILS_LANGUAGE_BAD = 'appinfo.ini: [Details]:Language is invalid, it should be "Multilingual" or one of the valid language names'
    APPINFO_DETAILS_PLUGINTYPE_NOT_PLUGIN = 'appinfo.ini: [Details]:PluginType is only valid for plugin installers.'
    APPINFO_DETAILS_PLUGINTYPE_BAD = 'appinfo.ini: [Details]:PluginType is invalid, it should be "CommonFiles" or omitted.'

    # [License]
    APPINFO_LICENSE_EULAVERSION_NO_EULA = 'appinfo.ini: [License]:EULAVersion is defined but neither %(eula)s.rtf nor %(eula)s.txt exists'

    # [Version]
    APPINFO_VERSION_PACKAGEVERSION_BAD = 'appinfo.ini: [Version]:PackageVersion must be an X.X.X.X version number'

    # [SpecialPaths]
    APPINFO_SPECIALPATHS_OMIT = 'appinfo.ini: [SpecialPaths] section should be omitted if empty'
    APPINFO_SPECIALPATHS_PLUGINS_OMIT = 'appinfo.ini: [SpecialPaths]:Plugins should be omitted if set to NONE'
    APPINFO_SPECIALPATHS_PLUGINS_BAD = 'appinfo.ini: [SpecialPaths]:Plugins must be the path to a directory in the package'

    # [Dependencies]
    APPINFO_DEPENDENCIES_JAVA_BAD = 'appinfo.ini: [Dependencies]:UsesJava should be "true" or omitted'
    APPINFO_DEPENDENCIES_USESDOTNETVERSION_BAD = 'appinfo.ini: [Dependencies]:UsesDotNetVersion should be unset or a .NET version like 1.1, 2.0, 3.0 or 3.5'
    APPINFO_DEPENDENCIES_USESDOTNETVERSION_PROBABLY_BAD = 'appinfo.ini: [Dependencies]:UsesDotNetVersion should probably be unset or 1.1, 2.0, 3.0 or 3.5; you probably have an invalid value'

    # [Control]
    APPINFO_CONTROL_START_NO_SUBDIRS = 'appinfo.ini: [%(section)s]:%(key)s should not include subdirectories'
    APPINFO_CONTROL_FILE_NOT_EXIST = 'appinfo.ini: the file specified in [%(section)s]:%(key)s does not exist'
    APPINFO_CONTROL_ICONS_BAD = 'appinfo.ini: [Control]:Icons must be a number greater than 0'

    # Validation

    VALIDATION_WINDOW_TITLE_CRITICAL = 'Validation results: critical error'
    VALIDATION_WINDOW_TITLE_FAIL = 'Validation results: fail'
    VALIDATION_WINDOW_TITLE_WARNINGS = 'Validation results: pass with warnings'
    VALIDATION_WINDOW_TITLE_PASS = 'Validation results: pass'

    VALIDATION_CRITICAL_HTML = 'PortableApps.com Format validation <strong>failed</strong> with a critical error: %s'
    VALIDATION_CRITICAL = 'Validation failed with a critical error: %s'

    VALIDATION_ERRORS_WARNINGS_HTML = 'PortableApps.com Format validation <strong>failed</strong> with %(numerrors)s %(strerrors)s and %(numwarnings)s %(strwarnings)s.'
    VALIDATION_ERRORS_WARNINGS = 'Validation failed with %(numerrors)s %(strerrors)s and %(numwarnings)s %(strwarnings)s.'

    VALIDATION_ERRORS_HTML = 'PortableApps.com Format validation <strong>failed</strong> with %(numerrors)s %(strerrors)s.'
    VALIDATION_ERRORS = 'Validation failed with %(numerrors)s %(strerrors)s.'

    VALIDATION_WARNINGS_HTML = 'PortableApps.com Format validation <strong>passed</strong> with %(numwarnings)s %(strwarnings)s.'
    VALIDATION_WARNINGS = 'Validation passed with %(numwarnings)s %(strwarnings)s.'

    VALIDATION_PASS_HTML = 'PortableApps.com Format validation <strong>succeeded</strong>.'
    VALIDATION_PASS = 'Validation succeeded.'

    VALIDATION_STR_ERRORS = 'Errors'
    VALIDATION_STR_WARNINGS = 'Warnings'
    VALIDATION_STR_INFORMATION = 'Information'


class _LanguagesController(object):
    """
    The manager for languages. It acts as a simple way to load languages and
    access strings from the current language.
    """

    def __init__(self):
        self._languages = {}
        self._current_language = None
        self.load_language()

    def __getattr__(self, attr):
        return getattr(self._current_language, attr)

    def load_language(self, lang=None):
        "Load the specified language or the language from the user's settings."
        if not lang:
            lang = config.get('Main', 'Language', 'english')

        if not lang.isalpha():
            raise ValueError('Language "%s" contains invalid characters' % lang)

        try:
            self._current_language = __import__('languages.%s' % lang.lower(),
                    fromlist=[None]).language  # non-empty fromlist so it works
            self._languages[lang.lower()] = self._current_language
        except (ImportError, AttributeError):
            raise ValueError('Language "%s" does not exist' % lang)

        config.settings.Main.Language = lang

LANG = _LanguagesController()
