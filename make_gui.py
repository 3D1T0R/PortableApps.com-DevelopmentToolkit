#!/usr/bin/env python
import sys
import os
import subprocess
import time


pages = ('start', 'details', 'launcher', 'compact', 'test', 'publish',
        'options', 'about')


def calc_mtimes(filenames):
    return dict((f, os.stat(f).st_mtime) for f in filenames)


def write_polling(actions):
    print 'Processing all...'
    write(actions)
    mtimes = calc_mtimes(actions)
    while True:
        changed = None
        for sfile, mtime in mtimes.iteritems():
            if os.stat(sfile).st_mtime != mtime:
                changed = sfile
                break
        if changed:
            print 'Change detected to %s, processing...' % changed
            write(actions, changed)
            mtimes = calc_mtimes(actions)

        time.sleep(0.5)

def write(actions, item=None):
    if item is None:
        for item in actions:
            write(actions, item)
    else:
        action = actions[item]
        if isinstance(action, tuple):
            action[0](item, *action[1:])
        else:
            action(item)


def main():
    uic_files = ['frontend'] + ['page' + s for s in pages]
    actions = {}
    actions.update(('gui/ui/%s.ui' % f, (tools.compile_ui, 'gui/ui/%s.py' % f)) for f in uic_files)
    actions['resources/resources.qrc'] = tools.compile_rc, 'gui/ui/resources_rc.py'

    if tools is None:
        print 'Invalid build target, leave blank or specify "pyside" or "pyqt4".'
        sys.exit(1)

    try:
        write_polling(actions)
    except KeyboardInterrupt:
        print  # Get a blank line


def do(*args):
    return subprocess.Popen(args).communicate()


class Tools(object):
    def compile_rc(self, from_, to):
        """Compile an QRC file to a Python module."""
        do(self.rcc, from_, '-o', to)
        self._common(to)

    def compile_ui(self, from_, to):
        """Compile a Qt UI file to a Python module."""
        with open(to, 'w') as out:
            try:
                self.uic.compileUi(from_, out)
            except:
                import traceback
                traceback.print_exc()
        self._common(to)

    def _common(self, to):
        do('sed', '-i', r'N; s/^# Created: .*\n//', to)
        if self.pymod != 'PyQt4':
            do('sed', '-i', 's/from %s import /from PyQt4 import /' % self.pymod, to)

    @staticmethod
    def create_from_argv(argv, *args, **kwargs):
        if len(argv) == 1 or argv[1].lower() == 'pyside':
            return PySideTools(*args, **kwargs)
        elif argv[1].lower() == 'pyqt4':
            return PyQt4Tools(*args, **kwargs)
        else:
            return None


class PySideTools(Tools):
    rcc = 'pyside-rcc'
    import pysideuic as uic
    pymod = 'PySide'


class PyQt4Tools(Tools):
    rcc = 'pyrcc4'
    from PyQt4 import uic
    pymod = 'PyQt4'


if __name__ == '__main__':
    tools = Tools.create_from_argv(sys.argv)
    main()
