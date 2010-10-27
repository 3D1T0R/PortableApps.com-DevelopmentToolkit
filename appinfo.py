# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from ui.appinfo import Ui_AppInfoDialog
from utils import center_window


class AppInfoDialog(QDialog):
    def __init__(self, parent=None):
        super(AppInfoDialog, self).__init__(parent)
        self.ui = Ui_AppInfoDialog()
        self.ui.setupUi(self)


def show():
    window = AppInfoDialog()
    center_window(window)
    window.show()
    return window
