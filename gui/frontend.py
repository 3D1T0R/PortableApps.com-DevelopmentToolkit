from PyQt4 import QtCore, QtGui
from .ui import Ui_MainWindow
from pages import pages
import config


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        for name, cls in pages.iteritems():
            setattr(self, 'page_' + name, cls(self.pages, self))

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
        self.pages.setCurrentWidget(self.current_page)
        self.current_nav.setChecked(True)
        self.current_page.enter()

    def closeEvent(self, event):
        """Window closed, trigger the leave event for the current page."""
        self.current_page.leave(True)
        config.settings.Main.Package = self.page_start.open.text()

for page in pages:
    fn_name = 'on_nav_%s_clicked' % page
    setattr(MainWindow, fn_name, QtCore.Slot(name=fn_name)((lambda page: lambda self: self.set_page(page))(page)))
