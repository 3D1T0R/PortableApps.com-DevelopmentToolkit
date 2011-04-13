# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

import os
from os.path import isfile
import iniparse
import ConfigParser
from validator.appcompactor import AppCompactorValidator


__all__ = ['AppCompactor']


class AppCompactor(object):
    "The manager for the AppCompactor data (appcompactor.ini)."

    def __init__(self, package):
        self.package = package
        self.errors = []
        self.warnings = []
        self.info = []
        self.ini = None
        self._path = ''

    def load(self, do_reload=True):
        "Load appcompactor.ini."
        if not do_reload and self.ini:
            return

        self._path = self.package.path('App', 'AppInfo', 'appcompactor.ini')

        try:
            self.ini = iniparse.INIConfig(open(self._path) \
                    if isfile(self._path) else None)
        except ConfigParser.Error as e:
            self.ini_fail = e

    def validate(self):
        """
        Validate the INI file and put the results into ``errors``, ``warnings``
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

        inivalidator = AppCompactorValidator()
        inivalidator.validate(self.ini, self.package)
        self.errors.extend(inivalidator.errors)
        self.warnings.extend(inivalidator.warnings)
        self.info.extend(inivalidator.info)

    def fix(self):
        "Some values in appinfo.ini can be fixed. This fixes such values."
        # TODO
        if len(self.ini) == 0:
            self.delete()
        elif len(self.ini['PortableApps.comAppCompactor']) == 0:
            self.delete()

    def delete(self):
        """Deletes appcompactor.ini; for use when it's empty."""
        os.remove(self._path)
