# -*- coding: utf-8 -*-

"""
Validate an app package in PortableApps.com Format and produce HTML.
"""

from qt.QtGui import QDialog
import paf
from ui.validationsimple import Ui_ValidationDialog
from utils import center_window
from languages import LANG


__all__ = ['ValidationDialog']


class ValidationDialog(QDialog):
    def __init__(self, path=None, parent=None):
        super(ValidationDialog, self).__init__(parent)
        self.ui = Ui_ValidationDialog()
        self.ui.setupUi(self)
        if path:
            self.load_package(path)

    def load_package(self, path):
        """
        Load a package.
        """

        try:
            self.package = paf.Package(path)
        except paf.PAFException as msg:
            out = LANG.VALIDATION.CRITICAL_HTML % msg
            self.ui.validationResultsHTML.setHtml(out)
            self.ui.validationResultsArea.setPlainText(out)
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_CRITICAL)
            return

        error_count = len(self.package.errors)
        warning_count = len(self.package.warnings)
        params = {
                'numerrors': error_count,
                'numwarnings': warning_count,
                'strerrors': error_count == 1 and 'error' or 'errors',
                'strwarnings': warning_count == 1 and 'warning' or 'warnings',
                }
        if error_count and warning_count:
            out = LANG.VALIDATION.ERRORS_WARNINGS_HTML % params
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_FAIL)
        elif error_count:
            out = LANG.VALIDATION.ERRORS_HTML % params
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_FAIL)
        elif warning_count:
            out = LANG.VALIDATION.WARNINGS_HTML % params
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_WARNINGS)
        else:
            out = LANG.VALIDATION.PASS_HTML
            self.setWindowTitle(LANG.VALIDATION.WINDOW_TITLE_PASS)

        out = '<p>' + out + '</p>\n\n'

        if error_count:
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_ERRORS
            for item in self.package.errors:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        if warning_count:
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_WARNINGS
            for item in self.package.warnings:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        if len(self.package.info):
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_INFORMATION
            for item in self.package.info:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        self.ui.validationResultsHTML.setHtml(out)
        self.ui.validationResultsArea.setPlainText(out)
