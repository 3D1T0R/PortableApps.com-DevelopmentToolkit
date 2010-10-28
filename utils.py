# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QDesktopWidget
from iniparse.config import Undefined
import os

_ = lambda x: QApplication.translate("MainWindow", x, None,
        QApplication.UnicodeUTF8)
_S = lambda x: unicode(_(x))


def ini_defined(val):
    return not isinstance(val, Undefined)


def get_ini_str(iniconfig, section, key, default=None):
    if not ini_defined(iniconfig[section]) or \
    not ini_defined(iniconfig[section][key]):
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


def center_window(window):
    scr = QDesktopWidget().screenGeometry()
    g = window.geometry()
    window.move((scr.width() - g.width()) / 2, (scr.height() - g.height()) / 2)


def path_insensitive(path):
    """
    Get a case-insensitive path for use on a case sensitive system.

    >>> path_insensitive('/Home')
    '/home'
    >>> path_insensitive('/Home/chris')
    '/home/chris'
    >>> path_insensitive('/HoME/CHris/')
    '/home/chris/
    >>> path_insensitive('/home/CHRIS')
    '/home/chris
    >>> path_insensitive('/Home/CHRIS/.gtk-bookmarks')
    '/home/chris/.gtk-bookmarks
    >>> path_insensitive('/home/chris/.GTK-bookmarks')
    '/home/chris/.gtk-bookmarks
    >>> path_insensitive('/HOME/Chris/.GTK-bookmarks')
    '/home/chris/.gtk-bookmarks
    >>> path_insensitive("/HOME/Chris/I HOPE this doesn't exist")
    "/HOME/Chris/I HOPE this doesn't exist"
    """

    return _path_insensitive(path) or path


def _path_insensitive(path):
    """
    Recursive part of path_insensitive to do the work.
    """

    if path == '' or os.path.exists(path):
        return path

    f = os.path.basename(path)  # f may be a directory or a file
    d = os.path.dirname(path)

    suffix = ''
    if not f:  # dir ends with a slash?
        if len(d) < len(path):
            suffix = path[:len(path) - len(d)]

        f = os.path.basename(d)
        d = os.path.dirname(d)

    if not os.path.exists(d):
        d = _path_insensitive(d)
        if not d:
            return False

    # at this point, the directory exists but not the file

    try:  # we are expecting 'd' to be a directory, but it could be a file
        files = os.listdir(d)
    except OSError:
        return False

    f_low = f.lower()

    try:
        f_nocase = [fl for fl in files if fl.lower() == f_low][0]
    except IndexError:
        return False

    if f_nocase:
        return os.path.join(d, f_nocase) + suffix
    else:
        return False
