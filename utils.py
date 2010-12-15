"""Various utility functions."""

from PyQt4.QtGui import QApplication, QDesktopWidget
import os

_ = lambda x: QApplication.translate("MainWindow", x, None,
        QApplication.UnicodeUTF8)


def get_ini_str(ini, section, key, default=None):
    """Get a value from an INIConfig with a default value if not set."""
    return ini[section][key] if key in ini[section] else default


def center_window(window):
    """Center a window on the screen."""
    s = QDesktopWidget().screenGeometry()
    g = window.geometry()
    window.move((s.width() - g.width()) // 2, (s.height() - g.height()) // 2)


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

    base = os.path.basename(path)  # may be a directory or a file
    dirname = os.path.dirname(path)

    suffix = ''
    if not base:  # dir ends with a slash?
        if len(dirname) < len(path):
            suffix = path[:len(path) - len(dirname)]

        base = os.path.basename(dirname)
        dirname = os.path.dirname(dirname)

    if not os.path.exists(dirname):
        dirname = _path_insensitive(dirname)
        if not dirname:
            return

    # at this point, the directory exists but not the file

    try:  # we are expecting dirname to be a directory, but it could be a file
        files = os.listdir(dirname)
    except OSError:
        return

    baselow = base.lower()
    try:
        basefinal = [fl for fl in files if fl.lower() == baselow][0]
    except IndexError:
        return

    if basefinal:
        return os.path.join(dirname, basefinal) + suffix
    else:
        return
