#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main launch script for PortableApps.com Development Toolkit.
"""

import sys
from qt import QtGui
from utils import center_window
import config
import warn
from frontend.guiqt import MainWindow, ValidationDialog

def main():
    """Run the normal interface."""
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()

    window.packageText.setText(config.get('Main', 'Package', ''))

    center_window(window)
    window.show()
    warn.set_warnings_qt()
    exit_code = app.exec_()

    prepare_quit(window)

    return exit_code


def prepare_quit(window):
    """Save the window state and settings file."""
    config.settings.Main.Package = window.packageText.text()
    config.save()


def cli_help():
    """Help for command-line usage."""
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
    """Just run the validator (GUI version)."""
    app = QtGui.QApplication(sys.argv)
    window = ValidationDialog(sys.argv[2])
    center_window(window)
    window.show()
    exit_code = app.exec_()

    return exit_code


def validate_cli():
    """Just run the validator (command-line version)."""
    from frontend.cli.validate import validate
    return validate(sys.argv[2])


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
    sys.exit(select_action()())
