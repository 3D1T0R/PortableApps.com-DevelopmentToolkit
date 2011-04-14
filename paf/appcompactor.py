# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

import os
import sys
from subprocess import Popen, PIPE
from orderedset import OrderedSet
import config
from utils import win32
from validator.engine import INIManager, SectionValidator, FileMeta, SectionMeta, ValidatorError, StringMapping


__all__ = ['AppCompactor']


class AppCompactor(INIManager):
    "The manager for the AppCompactor data (appcompactor.ini)."

    module = sys.modules[__name__]

    def path(self):
        return os.path.join('App', 'AppInfo', 'appcompactor.ini')

    class Meta(FileMeta):
        mandatory = OrderedSet(('PortableApps.comAppCompactor',))
        order = OrderedSet(('PortableApps.comAppCompactor',))
        enforce_order = True  # Ha! ha!
        mappings = (
                StringMapping('PortableApps.comAppCompactor', 'Section'),
                )

    def compact(self):
        """
        Compacts a package with the PortableApps.com AppCompactor. Currently
        this runs the normal GUI (with the path filled in) and the user will
        still need to press "Go".

        Raises an ``OSError`` if run on Linux/OS X and Wine is not installed.

        Returns True on success, or False if the PortableApps.com AppCompactor
        was not found. If something went otherwise wrong, you probably won't
        hear about it.
        """

        appcompactor_path = config.get('Main', 'AppCompactorPath')
        if not appcompactor_path or not os.path.isfile(appcompactor_path):
            return False

        package_path = self.package.path()
        # On Linux we can execute it with a Linux path, as Wine will take care
        # of that, but it still expects a Windows path out the other side. Use
        # winepath to convert it to the right Windows path.
        if not win32:
            # Blocking call; throws an OSError if winepath isn't found
            package_path = Popen(['winepath', '-w', package_path],
                    stdout=PIPE).communicate()[0].strip()

        Popen([appcompactor_path, package_path]).wait()

        return True


class Section(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('FilesExcluded', 'AdditionalExtensionsExcluded',
            'AdditionalExtensionsIncluded', 'CompressionFileSizeCutOff'))
        order = OrderedSet(('FilesExcluded', 'AdditionalExtensionsExcluded',
            'AdditionalExtensionsIncluded', 'CompressionFileSizeCutOff'))

    def CompressionFileSizeCutOff(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError()
        except ValueError:
            return ValidatorError("must be a positive integer")
