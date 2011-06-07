from ._base import WindowPage, assert_valid_package_path
from ..ui.pagetest import Ui_PageTest
from languages import LANG


class PageTest(WindowPage, Ui_PageTest):
    @assert_valid_package_path
    def enter(self):
        self.validate()
        self.load_checklist()

    @assert_valid_package_path
    def validate(self):
        """Validate the app."""
        package = self.window.package

        error_count = len(package.errors)
        warning_count = len(package.warnings)
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
            for item in package.errors:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        if warning_count:
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_WARNINGS
            for item in package.warnings:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        if len(package.info):
            out += '<p><strong>%s</strong></p>\n<ul>\n' % \
                LANG.VALIDATION.STR_INFORMATION
            for item in package.info:
                out += '<li>%s</li>\n' % item
            out += '</ul>\n'

        self.validation_results_html.setHtml(out)
        self.validation_results_plain.setPlainText(out)

    @assert_valid_package_path
    def load_checklist(self):
        pass  # TODO

    def go_to_tab(self, tab):
        self.tabwidget.setCurrentWidget(getattr(self, tab + '_tab'))
