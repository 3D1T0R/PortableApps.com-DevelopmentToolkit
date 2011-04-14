# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

import os
import sys
from orderedset import OrderedSet
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
