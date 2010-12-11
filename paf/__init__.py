# -*- coding: utf-8 -*-

FORMAT_VERSION = '2.0'


class PAFException(Exception):
    pass

from paf.package import *
from paf.appinfo import *
from paf.installer import *
from paf.launcher import *
