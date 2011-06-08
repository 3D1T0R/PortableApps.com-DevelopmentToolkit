"""Things to do with configuration and user settings storage."""

import os
import sys
from iniparse import INIConfig, tidy
from utils import get_ini_str

ROOT_DIR = os.path.abspath(os.path.dirname(unicode(sys.executable
    if hasattr(sys, 'frozen') else __file__, sys.getfilesystemencoding())))

settings = None

try:
    dirname = os.path.join(os.environ['PAL:DataDir'], 'AppInfo')
except KeyError:
    dirname = os.path.join(ROOT_DIR, 'resources')
with open(os.path.join(dirname, 'appinfo.ini')) as fp:
    ini = INIConfig(fp)
padt_version_info = ini.Version.DisplayVersion
del dirname, ini


def settings_path(filename=''):
    """Finds the path to a settings file."""
    return os.path.join(os.environ.get('PAL:DataDir', ROOT_DIR), filename)


def load():
    """Load the user's settings."""
    global settings
    settings_file = settings_path('settings.ini')
    if os.path.isfile(settings_file):
        settings = INIConfig(open(settings_file))
    else:
        settings = INIConfig()


def save():
    """Save the user's settings."""
    tidy(settings)
    with open(settings_path('settings.ini'), 'w') as outfile:
        outfile.write(unicode(settings))


def get(section, key, default=None):
    """Get a value from the user's settings."""
    return get_ini_str(settings, section, key, default)

load()
