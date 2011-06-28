#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main launch script for PortableApps.com Development Toolkit.
"""

import sys
import pyqt4pysideimporter
pyqt4pysideimporter.autoselect()
from PyQt4 import QtGui
from utils import center_window
import config
import warn
from gui import MainWindow


def main(path=None, page=None):
    """Run the normal interface."""
    app = QtGui.QApplication(sys.argv)
    if path is not None:
        config.settings.Main.Package = path
    window = MainWindow()
    if page is not None:
        window.set_page(page)

    center_window(window)
    window.show()
    warn.set_warnings_qt()
    exit_code = app.exec_()

    prepare_quit(window)

    return exit_code


def prepare_quit(window):
    """Save the window state and settings file."""
    config.save()


def cli_help(*args):
    """Help for command-line usage."""
    print "PortableApps.com Development Toolkit"
    print "Launch without command line arguments to run normally."
    print
    print 'Open with a given package loaded:'
    print '  %s <package>' % sys.argv[0]
    print
    print 'Validate a package (GUI):'
    print '  %s validate <package>' % sys.argv[0]
    print
    print 'Validate a package (command line):'
    print '  %s validate-cli <package>' % sys.argv[0]
    return 0


def validate_gui(command, path):
    """Run the validator (GUI version)."""
    return main(path, 'test')


def validate_cli(command, path):
    """Just run the validator (command-line version)."""
    from cli.validate import validate
    return validate(path)


def select_action():
    """Simple controller for command-line arguments."""
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            return cli_help
        elif sys.argv[1] == 'validate':
            return len(sys.argv) == 3 and validate_gui or cli_help
        elif sys.argv[1] == 'validate-cli':
            return len(sys.argv) == 3 and validate_cli or cli_help
        else:
            return main
    else:
        return main

if __name__ == "__main__":
    sys.exit(select_action()(*sys.argv[1:]))
