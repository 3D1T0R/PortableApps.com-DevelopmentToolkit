# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from iniparse.config import Undefined

_  = lambda x: QApplication.translate("MainWindow", x, None, QApplication.UnicodeUTF8)
_S = lambda x: unicode(_(x))

def ini_defined(val):
    return not isinstance(val, Undefined)

def get_ini_str(iniconfig, section, key, default=None):
    if not ini_defined(iniconfig[section]) or not ini_defined(iniconfig[section][key]):
        iniconfig[section][key] = default
        return default
    else:
        return iniconfig[section][key]

def method_of(cls):
    """
    Make a function a method of a class after the class is defined.
    Usage:
        @method_of(ClassName)
        def method_name(): pass
    """

    def decorate(fn):
        setattr(cls, fn.__name__, fn)
        # No return value, leaves def as None where it is written
    return decorate
