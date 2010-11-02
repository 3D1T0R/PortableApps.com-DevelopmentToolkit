"""
Language handling and i18n. With the exception of language files, ``LANG`` is
the only thing from this class which should be used. It's a proxy object which
gives the strings in the currently selected language.

Usage::

    from languages import LANG
    print LANG.SECTION.STRING
"""

import os
from collections import defaultdict
import config
from iniparse import INIConfig
from utils import path_insensitive, ini_defined

__all__ = ['LANG']


class _LanguagesController(object):
    """
    The manager for languages. It acts as a simple way to load languages and
    access strings from the current language.
    """

    class _LanguageSection(object):
        """
        Language section proxy to handle getting default values from English.
        This would be better implemented in INIConfig with a default model, but
        for the moment it's just here, separate.
        """
        def __init__(self, controller, section):
            if not ini_defined(controller._languages['english'][section]):
                raise AttributeError('Invalid language section "%s"' % section)

            self._section_name = section
            self._section = controller._current_language[section]
            self._english_section = controller._languages['english'][section]

        def __getattr__(self, attr):
            """
            Get a language string. Raises an AttributeError if the string
            doesn't exist in the current language or English.
            """
            if ini_defined(self._section[attr]):
                return self._section[attr]
            elif ini_defined(self._english_section[attr]):
                return self._english_section[attr]
            else:
                raise AttributeError('Invalid language string %s.%s' %
                        (self._section_name, attr))

    def __init__(self):
        self._languages = {}
        self._current_language_name = None
        self._current_language = None
        self._language_sections = defaultdict(dict)
        self.load_language()

    def __getattr__(self, attr):
        "Get a language section."

        if attr not in self._language_sections[self._current_language_name]:
            self._language_sections[self._current_language_name][attr] = \
                    _LanguagesController._LanguageSection(self, attr)
        return self._language_sections[self._current_language_name][attr]

    def load_language(self, lang=None):
        "Load the specified language or the language from the user's settings."

        if not lang:
            lang = config.get('Main', 'Language', 'english')

        if not lang.isalpha():
            raise ValueError('Language %s contains invalid characters' % lang)

        lang_name = lang.lower()
        if lang_name in self._languages:
            self._current_language_name = lang_name
            self._current_language = self._languages[lang_name]
        else:
            path = path_insensitive(os.path.join(config.ROOT_DIR,
                'languages', '%s.ini' % lang))
            if not os.path.isfile(path):
                raise ValueError('Language "%s" does not exist' % lang)
            with open(path) as langfile:
                self._current_language_name = lang_name
                self._current_language = INIConfig(langfile)
                self._languages[lang_name] = self._current_language

        config.settings.Main.Language = lang

LANG = _LanguagesController()
