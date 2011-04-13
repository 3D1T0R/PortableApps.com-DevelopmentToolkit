import sys
from orderedset import OrderedSet
from .engine import INIValidator, SectionValidator, FileMeta, SectionMeta, ValidatorError, StringMapping


class AppCompactorValidator(INIValidator):
    module = sys.modules[__name__]
    filename = r'App\AppInfo\appcompactor.ini'

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
