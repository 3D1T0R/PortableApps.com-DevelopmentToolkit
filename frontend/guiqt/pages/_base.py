from PyQt4.QtGui import QWidget
from functools import wraps
import paf


__all__ = ['assert_valid_package_path', 'WindowPage']


class WindowPage(QWidget):
    def __init__(self, parent, window):
        super(WindowPage, self).__init__(parent)
        self.setupUi(self)
        self.window = window
        parent.addWidget(self)  # Add self to the pages QStackedWidget

    def enter(self):
        """Event called when the page is entered (startup or user action)."""

        pass

    def leave(self, closing=False):
        """
        Event called when the page is left (could be window close event or
        going to another tab).
        """

        pass


def assert_valid_package_path(func):
    """Decorator to make sure that something which shouldn't ever happen
    doesn't cause a crash, and to provide a code indication of what's
    happening."""
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not isinstance(self, WindowPage):
            assert False, "assert_valid_package_path only works on WindowPage methods."
        assert paf.valid_package(self.window.page_start.open.text()), "The package is not valid."

        func(self, *args, **kwargs)
    return decorate
