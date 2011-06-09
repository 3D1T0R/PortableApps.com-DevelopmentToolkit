import re
from os import makedirs, remove
from os.path import dirname, exists, isfile
from functools import wraps
import ConfigParser
import iniparse
from orderedset import OrderedSet
from paf import PAFException
from languages import LANG


def assert_valid_ini(func):
    """A decorator to ensure the INI file is set up."""
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not self.path() or self.ini is None:
            # Naturally though this should never happen.
            raise PAFException(LANG.GENERAL.PACKAGE_NOT_INITIALISED)

        return func(self, *args, **kwargs)

    return decorate


class INIManager(object):
    """The manager for the INI files, providing framework and validation."""

    module = None

    def __init__(self, package):
        self.package = package
        self.errors = []
        self.warnings = []
        self.info = []
        self.ini = None

    def path(self):
        return ''

    def path_abs(self):
        return self.package.path(self.path())

    def load(self, do_reload=True):
        """Load the INI file."""
        if not do_reload and self.ini:
            return

        try:
            self.ini = iniparse.INIConfig(open(self.path_abs()) \
                    if isfile(self.path_abs()) else None)
        except ConfigParser.Error as e:
            self.ini_fail = e

    @assert_valid_ini
    def fix(self):
        """Fix the INI file as well as possible. To be overridden (and called as super)."""
        # Clear empty sections
        for section in self.ini:
            if len(self.ini[section]) == 0:
                del self.ini[section]

        # Clear empty file
        if len(self.ini) == 0:
            self.delete()
        else:
            self.save()

    @assert_valid_ini
    def save(self):
        """Save the current state of the INI file."""

        # Tidy it so when sections get added and removed and whatnot it looks
        # generally decent (no multiple blank lines, EOL at EOF)
        iniparse.tidy(self.ini)

        # Make sure the directory exists
        inidir = dirname(self.path_abs())
        if not exists(inidir):
            makedirs(inidir)

        # Now write it
        iniw = open(self.path_abs(), 'w')
        iniw.write(unicode(self.ini))
        iniw.close()

    def delete(self):
        """
        Deletes the INI file; for use when it's empty.
        Does nothing if the file doesn't exist.
        """

        path = self.path_abs()
        if isfile(path):
            remove(path)

    def validate(self):
        """
        Validate the appinfo and put the results into ``errors``, ``warnings``
        and ``info`` in ``self``.
        """
        self.load(False)
        if self.ini is None:
            self.errors.append(self.ini_fail)
            return  # Don't need "section missing" errors

        if not isfile(self.path_abs()):
            # If appinfo.ini doesn't exist, we've created an INIConfig which
            # will be empty, for the fix routine. Then as we don't want to spew
            # a whole heap of errors given that an error about appinfo.ini
            # being missing has already been added to the list, we'll give up.
            return

        ini = self.ini
        package = self.package
        meta = self.Meta(self, ini, package)  # () so properties work
        setini = OrderedSet(ini)

        for missing in meta.mandatory - setini:
            self.errors.append(LANG.INIVALIDATOR.SECTION_MISSING % dict(filename=self.path(), section=missing))

        for extra in setini - meta.order:
            self.errors.append(LANG.INIVALIDATOR.SECTION_EXTRA % dict(filename=self.path(), section=extra))

        # Check that they're in the same order
        if meta.enforce_order and setini & meta.order != meta.order & setini:
            # A warning? We like fancy INI files.
            self.warnings.append(LANG.INIVALIDATOR.SECTIONS_OUT_OF_ORDER % dict(filename=self.path()))

        if len(ini) == 0:
            self.warnings.append(LANG.INIVALIDATOR.FILE_EMPTY % dict(filename=self.path()))

        for section in setini & meta.order:
            if hasattr(self.module, section):
                secval_cls = getattr(self.module, section)
            else:
                for mapping in meta.mappings:
                    if mapping.match(section):
                        secval_cls = getattr(self.module, mapping.target)
                        # TODO: could be nice to know what section is in this case...
                        break
            secval = secval_cls(self, ini, package)
            smeta = secval.Meta(self, ini, package, secval)
            inisection = ini[section]
            inisectionset = OrderedSet(inisection)

            if len(inisection) == 0:
                self.warnings.append(LANG.INIVALIDATOR.SECTION_EMPTY % dict(filename=self.path(), section=section))

            for key in smeta.mandatory:
                if key not in inisection:
                    self.errors.append(LANG.INIVALIDATOR.VALUE_MISSING %
                            dict(filename=self.path(), section=section, key=key))
                elif inisection[key] == '':
                    self.errors.append(LANG.INIVALIDATOR.VALUE_EMPTY %
                            dict(filename=self.path(), section=section, key=key))

            for key in inisectionset - smeta.mandatory:
                if key not in smeta.optional:
                    self.errors.append(LANG.INIVALIDATOR.VALUE_EXTRA %
                            dict(filename=self.path(), section=section, key=key))
                elif inisection[key] == '':
                    self.errors.append(LANG.INIVALIDATOR.OMIT_EMPTY %
                            dict(filename=self.path(), section=section, key=key))

            # Check that they're in the same order
            enforce_order = meta.enforce_order if smeta.enforce_order is Ellipsis else smeta.enforce_order
            if enforce_order and inisectionset & smeta.order != smeta.order & inisectionset:
                # A warning? We like fancy INI files.
                self.warnings.append(LANG.INIVALIDATOR.KEYS_OUT_OF_ORDER %
                        dict(filename=self.path(), section=section))

            # Oh yeah, we may as well validate the value. Could be handy.
            for key in smeta.order:
                if key in inisection:
                    if hasattr(secval, key):
                        self._add_item(getattr(secval, key)(inisection[key]))
                    else:
                        for mapping in smeta.mappings:
                            if mapping.match(key):
                                self._add_item(getattr(secval, mapping.target)(inisection[key]))
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


class StringMapping(object):
    def __init__(self, matcher, target):
        self.matcher = matcher
        self.target = target

    def match(self, value):
        return self.matcher == value


class RegExMapping(object):
    def __init__(self, matcher, target):
        self.matcher = matcher
        self.target = target

    def match(self, value):
        return re.match(self.matcher, value)
