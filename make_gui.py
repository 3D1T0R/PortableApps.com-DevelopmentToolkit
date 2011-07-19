#!/usr/bin/env python
import sys
import subprocess
import pyqt4pysideimporter
pyqt4pysideimporter.autoselect()
from gui.pages import pages


def main():
    uic_files = ['frontend'] + ['page' + s for s in pages]

    tools = Tools.create_from_argv(sys.argv)
    if tools == None:
        print 'Invalid build target, leave blank or specify "pyside" or "pyqt4".'
        sys.exit(1)

    tools.compile_rc('resources/resources.qrc', 'gui/ui/resources_rc.py')

    for f in uic_files:
        tools.compile_ui('gui/ui/%s.ui' % f, 'gui/ui/%s.py' % f)

    tools.finish()


def do(*args):
    return subprocess.Popen(args).communicate()


class Tools(object):
    def __init__(self):
        # Process these things all in one shot at the end
        self.files_rc = []
        self.files_ui = []

    def compile_rc(self, from_, to):
        """Compile an QRC file to a Python module."""
        do(self.rcc, from_, '-o', to)
        self.files_rc.append(to)

    def compile_ui(self, from_, to):
        """Compile a Qt UI file to a Python module."""
        do(self.uic, from_, '-o', to)
        self.files_ui.append(to)

    def finish(self):
        """Update module references and finish processing all resources."""

        # Scrap the timestamp from RCC files as it clutters commits.
        do('sed', '-i', r'N; s/^# Created: .*\n//', *self.files_rc + self.files_ui)

        # Change PySide imports to use PyQt4 (due to use of import redirector)
        if self.pymod != 'PyQt4':
            do('sed', '-i', 's/from %s import /from PyQt4 import /' % self.pymod, *self.files_rc + self.files_ui)

    @staticmethod
    def create_from_argv(argv, *args, **kwargs):
        if len(argv) == 1 or argv[1].lower() == 'pyside':
            return PySideTools(*args, **kwargs)
        elif argv[1].lower() == 'pyqt4':
            return PySideTools(*args, **kwargs)
        else:
            return None


class PySideTools(Tools):
    rcc = 'pyside-rcc'
    uic = 'pyside-uic'
    pymod = 'PySide'


class PyQt4Tools(Tools):
    rcc = 'pyrcc4'
    uic = 'pyuic4'
    pymod = 'PyQt4'


if __name__ == '__main__':
    main()
