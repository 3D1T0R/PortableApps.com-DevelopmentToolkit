import re
from orderedset import OrderedSet
from languages import LANG

class INIValidator(object):
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self, ini, package):
        meta = self.Meta(self, ini, package)  # () so properties work
        setini = OrderedSet(ini)

        for missing in meta.mandatory - setini:
            self.errors.append(LANG.INIVALIDATOR.SECTION_MISSING % dict(filename=self.filename, section=missing))

        for extra in setini - meta.order:
            self.errors.append(LANG.INIVALIDATOR.SECTION_EXTRA % dict(filename=self.filename, section=extra))

        # Check that they're in the same order
        if meta.enforce_order and setini & meta.order != meta.order & setini:
            # A warning? We like fancy INI files.
            self.warnings.append(LANG.INIVALIDATOR.SECTIONS_OUT_OF_ORDER % dict(filename=self.filename))

        for section in setini & meta.order:
            secval_cls = getattr(self.module, section)
            if hasattr(self.module, section):
                secval_cls = getattr(self.module, section)
            else:
                for regex, clsname in meta.mappings.iteritems():
                    if re.match(regex, key):
                        secval_cls = getattr(self.module, clsname)
                        # TODO: could be nice to know what section is in this case...
                        break
            secval = secval_cls(self, ini, package)
            smeta = secval.Meta(self, ini, package, secval)
            inisection = ini[section]
            inisectionset = OrderedSet(inisection)

            for key in smeta.mandatory:
                if key not in inisection:
                    self.errors.append(LANG.INIVALIDATOR.VALUE_MISSING %
                            dict(filename=self.filename, section=section, key=key))
                elif inisection[key] == '':
                    self.errors.append(LANG.INIVALIDATOR.VALUE_EMPTY %
                            dict(filename=self.filename, section=section, key=key))

            for key in inisectionset - smeta.mandatory:
                if key not in smeta.optional:
                    self.errors.append(LANG.INIVALIDATOR.VALUE_EXTRA %
                            dict(filename=self.filename, section=section, key=key))
                elif inisection[key] == '':
                    self.errors.append(LANG.INIVALIDATOR.OMIT_EMPTY %
                            dict(filename=self.filename, section=section, key=key))

            # Check that they're in the same order
            enforce_order = meta.enforce_order if smeta.enforce_order is Ellipsis else smeta.enforce_order
            if enforce_order and inisectionset & smeta.order != smeta.order & inisectionset:
                # A warning? We like fancy INI files.
                self.warnings.append(LANG.INIVALIDATOR.KEYS_OUT_OF_ORDER %
                        dict(filename=self.filename, section=section))

            # Oh yeah, we may as well validate the value. Could be handy.
            for key in smeta.order:
                if key in inisection:
                    if hasattr(secval, key):
                        self._add_item(getattr(secval, key)(inisection[key]))
                    else:
                        for regex, fnname in smeta.mappings.iteritems():
                            if re.match(regex, key):
                                self._add_item(getattr(secval, fnname)(inisection[key]))
                                # TODO: could be nice to know what key is in this case...
                                break

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
    def __init__(self, validator, ini, package):
        self.validator = validator
        self.ini = ini
        self.package = package


class SectionValidator(ValidatorObject):
    pass


class FileMeta(ValidatorObject):
    mandatory = OrderedSet()
    optional = OrderedSet()
    order = OrderedSet()
    enforce_order = False
    mappings = {}


class SectionMeta(ValidatorObject):
    mandatory = OrderedSet()
    optional = OrderedSet()
    order = OrderedSet()
    enforce_order = Ellipsis  # Inherit from file
    mappings = {}

    def __init__(self, validator, ini, package, secval):
        super(SectionMeta, self).__init__(validator, ini, package)
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
