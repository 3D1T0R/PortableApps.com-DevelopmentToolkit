from . import ValidatorError
from languages import LANG


def bool_check(section, key):
    def check(self, value):
        if value not in ('true', 'false'):
            return ValidatorError(LANG.APPINFO.BOOL_BAD % dict(section=section, key=key))
    check.__name__ = key
    return check
