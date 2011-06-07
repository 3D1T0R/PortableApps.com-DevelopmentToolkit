from PyQt4 import QtCore, QtGui
from .ui import Ui_MainWindow
from pages import (PageStart, PageDetails, PageLauncher, PageCompact, PageTest,
        PagePublish, PageOptions, PageAbout)
import config


pages = ('start', 'details', 'launcher', 'compact', 'test', 'publish', 'options', 'about')


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Added to self.pages in WindowPage.__init__
        self.page_start = PageStart(self.pages, self)
        self.page_details = PageDetails(self.pages, self)
        self.page_launcher = PageLauncher(self.pages, self)
        self.page_compact = PageCompact(self.pages, self)
        self.page_test = PageTest(self.pages, self)
        self.page_publish = PagePublish(self.pages, self)
        self.page_options = PageOptions(self.pages, self)
        self.page_about = PageAbout(self.pages, self)

        self.page_start.open.setFocus()
        self.page_start.on_open_textChanged(self.page_start.open.text())
        self.set_page('start')

        self.page_start.open.setText(config.get('Main', 'Package', ''))

    @QtCore.Slot()
    def set_page(self, name):
        # On the first call, these aren't set, so skip them
        if hasattr(self, 'current_page'):
            # Make sure it's not highlighted, the user click will highlight it but the leave()
            # call can take time (e.g. show QMessageBox) which would make it look bad.
            getattr(self, 'nav_' + name).setChecked(False)
            if self.current_page.leave() is False:
                return
            self.current_nav.setChecked(False)
        self.current_nav = getattr(self, 'nav_%s' % name)
        self.current_page = getattr(self, 'page_%s' % name)
        self.pages.setCurrentIndex(pages.index(name))
        self.current_nav.setChecked(True)
        self.current_page.enter()

    def closeEvent(self, event):
        """Window closed, trigger the leave event for the current page."""
        self.current_page.leave(True)
        config.settings.Main.Package = self.page_start.open.text()

    @QtCore.Slot()
    def on_nav_start_clicked(self):
        self.set_page('start')

    @QtCore.Slot()
    def on_nav_details_clicked(self):
        self.set_page('details')

    @QtCore.Slot()
    def on_nav_launcher_clicked(self):
        self.set_page('launcher')

    @QtCore.Slot()
    def on_nav_compact_clicked(self):
        self.set_page('compact')

    @QtCore.Slot()
    def on_nav_test_clicked(self):
        self.set_page('test')

    @QtCore.Slot()
    def on_nav_publish_clicked(self):
        self.set_page('publish')

    @QtCore.Slot()
    def on_nav_options_clicked(self):
        self.set_page('options')

    @QtCore.Slot()
    def on_nav_about_clicked(self):
        self.set_page('about')
