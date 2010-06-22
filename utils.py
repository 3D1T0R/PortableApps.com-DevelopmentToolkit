# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from iniparse.config import Undefined

_ = lambda x: QApplication.translate("MainWindow", x, None, QApplication.UnicodeUTF8)

def ini_defined(val):
    return not isinstance(val, Undefined)

def get_ini_str(iniconfig, section, key, default=None):
    if not ini_defined(iniconfig[section]) or not ini_defined(iniconfig[section][key]):
        iniconfig[section][key] = default
        return default
    else:
        return iniconfig[section][key]
