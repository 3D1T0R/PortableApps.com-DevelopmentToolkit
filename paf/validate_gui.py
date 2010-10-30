# -*- coding: utf-8 -*-

"""
Validate an app package in PortableApps.com Format and produce HTML.

This is loaded from config.py.
"""

from PyQt4.QtGui import QDialog
import paf
from ui.validationsimple import Ui_ValidationDialog
from utils import center_window
from languages import LANG


class ValidationDialog(QDialog):
    def __init__(self, parent=None):
        super(ValidationDialog, self).__init__(parent)
        self.ui = Ui_ValidationDialog()
        self.ui.setupUi(self)


def validate(path):
    """
    Validate a package.
    """

    window = ValidationDialog()
    center_window(window)

    try:
        app = paf.Package(path)
    except paf.PAFException as msg:
        out = LANG.VALIDATION_CRITICAL_HTML % msg
        window.ui.validationResultsHTML.setHtml(out)
        window.ui.validationResultsArea.setPlainText(out)
        window.setWindowTitle(LANG.VALIDATION_WINDOW_TITLE_CRITICAL)
        window.show()
        return

    error_count = len(app.errors)
    warning_count = len(app.warnings)
    params = {
            'numerrors': error_count,
            'numwarnings': warning_count,
            'strerrors': error_count == 1 and 'error' or 'errors',
            'strwarnings': warning_count == 1 and 'warning' or 'warnings',
            }
    if error_count and warning_count:
        out = LANG.VALIDATION_ERRORS_WARNINGS_HTML % params
        window.setWindowTitle(LANG.VALIDATION_WINDOW_TITLE_FAIL)
    elif error_count:
        out = LANG.VALIDATION_ERRORS_HTML % params
        window.setWindowTitle(LANG.VALIDATION_WINDOW_TITLE_FAIL)
    elif warning_count:
        out = LANG.VALIDATION_WARNINGS_HTML % params
        window.setWindowTitle(LANG.VALIDATION_WINDOW_TITLE_WARNINGS)
    else:
        out = LANG.VALIDATION_PASS_HTML
        window.setWindowTitle(LANG.VALIDATION_WINDOW_TITLE_PASS)

    out = '<p>' + out + '</p>\n\n'

    if error_count:
        out += '<p><strong>%s</strong></p>\n<ul>\n' % LANG.VALIDATION_STR_ERRORS
        for item in app.errors:
            out += '<li>%s</li>\n' % item
        out += '</ul>\n'

    if warning_count:
        out += '<p><strong>%s</strong></p>\n<ul>\n' % \
            LANG.VALIDATION_STR_WARNINGS
        for item in app.warnings:
            out += '<li>%s</li>\n' % item
        out += '</ul>\n'

    if len(app.info):
        out += '<p><strong>%s</strong></p>\n<ul>\n' % \
            LANG.VALIDATION_STR_INFORMATION
        for item in app.info:
            out += '<li>%s</li>\n' % item
        out += '</ul>\n'

    window.ui.validationResultsHTML.setHtml(out)
    window.ui.validationResultsArea.setPlainText(out)
    window.show()

    return window
