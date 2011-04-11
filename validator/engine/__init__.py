from orderedset import OrderedSet
from languages import LANG

class INIValidator(object):
    def __init__(self, module):
        self.module = module
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self, ini, package):
        meta = self.module.Meta(ini, package)  # () so properties work
        setini = OrderedSet(ini)

        for missing in meta.mandatory - setini:
            self.errors.append(LANG.APPINFO.SECTION_MISSING % missing)

        for extra in setini - meta.order:
            self.errors.append(LANG.APPINFO.SECTION_EXTRA % extra)

        # Check that they're in the same order
        if meta.enforce_order and setini & meta.order != meta.order & setini:
            # A warning? We like fancy INI files.
            self.warnings.append(LANG.APPINFO.SECTIONS_OUT_OF_ORDER)

        for section in setini & meta.order:
            secval = getattr(self.module, section)(ini, package)
            smeta = secval.Meta(ini, package, secval)
            inisection = ini[section]
            inisectionset = OrderedSet(inisection)

            for key in smeta.mandatory:
                if key not in inisection:
                    self.errors.append(LANG.APPINFO.VALUE_MISSING %
                            dict(section=section, key=key))
                elif inisection[key] == '':
                    self.errors.append(LANG.APPINFO.VALUE_EMPTY %
                            dict(section=section, key=key))

            for key in inisectionset - smeta.mandatory:
                if key not in smeta.optional:
                    self.errors.append(LANG.APPINFO.VALUE_EXTRA %
                            dict(section=section, key=key))
                elif inisection[key] == '':
                    self.errors.append(LANG.APPINFO.OMIT_EMPTY %
                            dict(section=section, key=key))

            # Check that they're in the same order
            enforce_order = meta.enforce_order if smeta.enforce_order is Ellipsis else smeta.enforce_order
            if enforce_order and inisectionset & smeta.order != smeta.order & inisectionset:
                # A warning? We like fancy INI files.
                self.warnings.append(LANG.APPINFO.KEYS_OUT_OF_ORDER % section)

            # Oh yeah, we may as well validate the value. Could be handy.
            for key in smeta.order:
                if key in inisection and hasattr(secval, key):
                    self._add_item(getattr(secval, key)(inisection[key]))

    def _add_item(self, item):
        if item is None:
            return
        elif isinstance(item, (list, tuple)):
            for i in item:
                self._add_item(i)
        elif isinstance(item, ValidatorError):
            self.errors.append(item)
        elif isinstance(item, ValidatorWarning):
            self.warnings.append(item)
        elif isinstance(item, ValidatorInfo):
            self.info.append(item)
        else:
            raise TypeError("INIValidator._add_item wants list, tuple, error, warning or info.")


class ValidatorObject(object):
    def __init__(self, ini, package):
        self.ini = ini
        self.package = package


class SectionValidator(ValidatorObject):
    pass


class FileMeta(ValidatorObject):
    mandatory = OrderedSet()
    optional = OrderedSet()
    order = OrderedSet()
    enforce_order = False


class SectionMeta(ValidatorObject):
    mandatory = OrderedSet()
    optional = OrderedSet()
    order = OrderedSet()
    enforce_order = Ellipsis  # Inherit from file

    def __init__(self, ini, package, secval):
        super(SectionMeta, self).__init__(ini, package)
        self.parent = secval


class ValidatorItem(object):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

class ValidatorError(ValidatorItem):
    pass


class ValidatorWarning(ValidatorItem):
    pass


class ValidatorInfo(ValidatorItem):
    pass
