# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

from os import makedirs
from os.path import exists, isfile
from languages import LANG
import iniparse
import ConfigParser
from paf import PAFException
from orderedset import OrderedSet
from functools import wraps
from validator.appinfo import AppInfoValidator


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

        try:
            self.ini = iniparse.INIConfig(open(self._path) \
                    if isfile(self._path) else None)
        except ConfigParser.Error as e:
            self.ini_fail = e

    def validate(self):
        """
        Validate the appinfo and put the results into ``errors``, ``warnings``
        and ``info`` in ``self``.
        """
        self.load(False)
        if self.ini is None:
            self.errors.append(self.ini_fail)
            return  # Don't need "section missing" errors

        if not isfile(self._path):
            # If appinfo.ini doesn't exist, we've created an INIConfig which
            # will be empty, for the fix routine. Then as we don't want to spew
            # a whole heap of errors given that an error about appinfo.ini
            # being missing has already been added to the list, we'll give up.
            return

        inivalidator = AppInfoValidator()
        inivalidator.validate(self.ini, self.package)
        self.errors.extend(inivalidator.errors)
        self.warnings.extend(inivalidator.warnings)
        self.info.extend(inivalidator.info)

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
