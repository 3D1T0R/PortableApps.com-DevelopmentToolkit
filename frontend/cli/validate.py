# -*- coding: utf-8 -*-

"""
Validate an app package in PortableApps.com Format from the command line.

This is loaded from config.py.
"""

import paf
from languages import LANG


def validate(path):
    """
    Validate a package.

    The return value is an exit code.

    A return value of 3 indicates critical errors in loading the package.

    A return value of 2 indicates errors in the package.

    A return value of 1 indicates warnings in the package.

    A return value of 0 indicates success.
    """

    try:
        app = paf.Package(path)
    except paf.PAFException as msg:
        print LANG.VALIDATION.CRITICAL % msg
        return 3

    error_count = len(app.errors)
    warning_count = len(app.warnings)
    params = {
            'numerrors': error_count,
            'numwarnings': warning_count,
            'strerrors': error_count == 1 and 'error' or 'errors',
            'strwarnings': warning_count == 1 and 'warning' or 'warnings',
            }
    if error_count and warning_count:
        print LANG.VALIDATION.ERRORS_WARNINGS % params
    elif error_count:
        print LANG.VALIDATION.ERRORS % params
    elif warning_count:
        print LANG.VALIDATION.WARNINGS % params
    else:
        print LANG.VALIDATION.PASS

    print

    if error_count:
        print LANG.VALIDATION.STR_ERRORS + ':'
        print '=' * (len(LANG.VALIDATION.STR_ERRORS) + 1)
        for item in app.errors:
            print item
        print

    if warning_count:
        print LANG.VALIDATION.STR_WARNINGS + ':'
        print '=' * (len(LANG.VALIDATION.STR_WARNINGS) + 1)
        for item in app.warnings:
            print item
        print

    if len(app.info):
        print LANG.VALIDATION.STR_INFORMATION + ':'
        print '=' * (len(LANG.VALIDATION.STR_INFORMATION) + 1)
        for item in app.info:
            print item
        print

    if error_count:
        return 2
    elif warning_count:
        return 1
    else:
        return 0
