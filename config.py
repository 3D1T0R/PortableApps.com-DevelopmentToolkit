"""Things to do with configuration and user settings storage."""

import os
import sys
from iniparse import tidy
from utils import get_ini_str, iniopen

ROOT_DIR = os.path.abspath(os.path.dirname(unicode(sys.executable
    if hasattr(sys, 'frozen') else __file__, sys.getfilesystemencoding())))

settings = None

try:
    dirname = os.path.join(os.environ['PAL:AppDir'], 'AppInfo')
except KeyError:
    dirname = os.path.join(ROOT_DIR, 'resources')
padt_version_info = iniopen(os.path.join(dirname,
        'appinfo.ini')).Version.DisplayVersion
del dirname


def settings_path(filename=''):
    """Finds the path to a settings file."""
    return os.path.join(os.environ.get('PAL:DataDir', ROOT_DIR), filename)


def load():
    """Load the user's settings."""
    global settings
    settings_file = settings_path('settings.ini')
    if os.path.isfile(settings_file):
        settings = iniopen(settings_file)
    else:
        settings = iniopen()


def save():
    """Save the user's settings."""
    tidy(settings)
    with open(settings_path('settings.ini'), 'w') as outfile:
        outfile.write(unicode(settings))


def get(section, key, default=None):
    """Get a value from the user's settings."""
    return get_ini_str(settings, section, key, default)

load()
