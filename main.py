#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from qt import QtCore, QtGui
from ui.mainwindow import Ui_MainWindow
from utils import _, center_window
import paf
import paf.validate_cli
import config
import warnings
import warn
from functools import wraps
from subprocess import Popen, PIPE
from guiqt.main import MainWindow
from guiqt.validate import ValidationDialog


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()

    window.ui.packageText.setText(config.get('Main', 'Package', ''))

    center_window(window)
    window.show()
    warn.set_warnings_qt()
    exit_code = app.exec_()

    prepare_quit(window)

    return exit_code


def prepare_quit(window):
    config.settings.Main.Package = window.ui.packageText.text()
    config.save()


def cli_help():
    print "PortableApps.com Development Toolkit"
    print "Launch without command line arguments to run normally."
    print
    print 'Validate a package (GUI):'
    print '  %s validate <package>' % sys.argv[0]
    print
    print 'Validate a package (command line):'
    print '  %s validate-cli <package>' % sys.argv[0]
    return 0


def validate_gui():
    app = QtGui.QApplication(sys.argv)
    window = ValidationDialog(sys.argv[2])
    center_window(window)
    window.show()
    exit_code = app.exec_()

    return exit_code


def validate_cli():
    return paf.validate_cli.validate(sys.argv[2])


def not_implemented():
    warnings.warn('Sorry, this is not implemented yet.',
            UserWarning, stacklevel=2)


if len(sys.argv) > 1:
    if sys.argv[1] == 'help':
        action = cli_help
    elif sys.argv[1] == 'validate':
        action = len(sys.argv) == 3 and validate_gui or cli_help
    elif sys.argv[1] == 'validate-cli':
        action = len(sys.argv) == 3 and validate_cli or cli_help
    else:
        action = main
else:
    action = main

if __name__ == "__main__":
    sys.exit(action())
