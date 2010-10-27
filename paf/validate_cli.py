# -*- coding: utf-8 -*-

"""
Validate an app package in PortableApps.com Format from the command line.

This is loaded from config.py.
"""

import paf


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
        print 'Validation failed with a critical error: %s' % unicode(msg)
        return 3

    error_count = len(app.errors)
    warning_count = len(app.warnings)
    errwarn_dict = dict(
            error_count=error_count,
            warning_count=warning_count,
            str_errors=error_count == 1 and 'error' or 'errors',
            str_warnings=warning_count == 1 and 'warning' or 'warnings',
            )
    if error_count and warning_count:
        print ('Validation failed with %(error_count)s %(str_errors)s and ' +
            '%(warning_count)s %(str_warnings)s.') % errwarn_dict
    elif error_count:
        print 'Validation failed with %(error_count)s %(str_errors)s.' \
                % errwarn_dict
    elif warning_count:
        print 'Validation passed with %(warning_count)s %(str_warnings)s.' \
                % errwarn_dict
    else:
        print 'Validation succeeded!'

    print

    if error_count:
        print 'Errors:'
        print '======='
        for error in app.errors:
            print error
        print

    if warning_count:
        print 'Warnings:'
        print '========='
        for warning in app.warnings:
            print warning
        print

    if len(app.info):
        print 'Information:'
        print '============'
        for info in app.info:
            print info
        print

    if error_count:
        return 2
    elif warning_count:
        return 1
    else:
        return 0
