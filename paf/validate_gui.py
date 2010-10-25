# -*- coding: utf-8 -*-

"""
Validate an app package in PortableApps.com Format and produce HTML.

This is loaded from config.py.
"""

from PyQt4.QtGui import QDialog
import paf
from ui.validationsimple import Ui_ValidationDialog
from utils import center_window


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

    out = u'<p>PortableApps.com Format validation <strong>'

    try:
        app = paf.Package(path)
    except paf.PAFException as msg:
        out += u'failed</strong> with a critical error: %s</p>' % unicode(msg)
        window.ui.validationResultsHTML.setHtml(out)
        window.ui.validationResultsArea.setPlainText(out)
        window.show()
        return

    error_count = len(app.errors)
    warning_count = len(app.warnings)
    params = {
            'numerrors': error_count,
            'numwarnings': warning_count,
            'strerrors':  error_count == 1 and 'error' or 'errors',
            'strwarnings': warning_count == 1 and 'warning' or 'warnings',
            }
    if error_count and warning_count:
        out += ('failed</strong> with %(numerrors)s %(strerrors)s and ' +
            '%(numwarnings)s %(strwarnings)s.') % params
        window.setWindowTitle('Validation results: fail')
    elif error_count:
        out += 'failed</strong> with %(numerrors)s %(strerrors)s.' % params
        window.setWindowTitle('Validation results: fail')
    elif warning_count:
        out += 'passed</strong> with %(numwarnings)s %(strwarnings)s.' % params
        window.setWindowTitle('Validation results: pass with warnings')
    else:
        out += 'succeeded</strong>.'
        window.setWindowTitle('Validation results: pass')

    out += '</p>\n\n'

    if error_count:
        out += '<p><strong>Errors:</strong></p>\n<ul>\n'
        for error in app.errors:
            out += '<li>' + error + '</li>\n'
        out += '</ul>\n'

    if warning_count:
        out += '<p><strong>Warnings:</strong></p>\n<ul>\n'
        for warning in app.warnings:
            out += '<li>' + warning + '</li>\n'
        out += '</ul>\n'

    if len(app.info):
        out += '<p><strong>Information:</strong></p>\n<ul>\n'
        for info in app.info:
            out += '<li>' + info + '</li>\n'
        out += '</ul>\n'

    window.ui.validationResultsHTML.setHtml(out)
    window.ui.validationResultsArea.setPlainText(out)
    window.show()

    return window
