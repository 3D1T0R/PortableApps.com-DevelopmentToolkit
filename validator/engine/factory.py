from . import ValidatorError, ValidatorWarning
from languages import LANG


def bool_check(section, key, default=None):
    def check(self, value):
        if value not in ('true', 'false'):
            return ValidatorError(LANG.INIVALIDATOR.BOOL_BAD %
                    dict(filename=self.validator.path, section=section, key=key))
        elif default is not None and value == default:
            return ValidatorWarning(LANG.INIVALIDATOR.OMIT_DEFAULT %
                    dict(filename=self.validator.path, section=section, key=key, default=default))
    check.__name__ = key
    return check
