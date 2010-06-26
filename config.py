# -*- coding: utf-8 -*-

import os
from iniparse import INIConfig, tidy
from utils import get_ini_str

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def settings_path(filename=None):
    if 'PAL:DataDir' in os.environ and os.path.isdir(os.environ['PAL:DataDir']):
        dirname = os.environ['PAL:DataDir']
    else:
        dirname = os.path.dirname(__file__)

    if filename:
        return os.path.join(dirname, filename)
    else:
        return dirname

def load():
    global settings

    settings_file = settings_path('settings.ini')

    if os.path.isfile(settings_file):
        settings = INIConfig(open(settings_file))
    else:
        settings = INIConfig()

def save():
    f = open(settings_path('settings.ini'), 'w')
    tidy(settings)
    f.write(unicode(settings))
    f.close()

def get(section, key, default=None):
    return get_ini_str(settings, section, key, default)

load()
