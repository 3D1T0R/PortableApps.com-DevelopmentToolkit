"""
A simple wrapper for both PySide and PyQt4 when they are considered
interchangeable, fixing up bad things in PyQt4 if it's selected.
"""

__all__ = ('IS_PYQT4', 'IS_PYSIDE', 'autoselect')

import zip_imp  # for py2exe
import imp


def load_pyside():
    """Sets up PyQt4 imports to actually import PySide."""
    class PyQtImporter(object):
        """A simple PyQt4 to PySide import redirector."""
        def find_module(self, name, path):
            """Changes PyQt4 imports to PySide."""
            if name == 'PyQt4' and path is None:
                self.modData = imp.find_module('PySide')
                return self
            return None

        def load_module(self, name):
            """Loads the given module."""
            return imp.load_module(name, *self.modData)

    import sys
    sys.meta_path.append(PyQtImporter())

    # PyQt4? Here, have PySide.
    from PyQt4 import QtCore
    QtCore._QT_ENGINE = 'PySide'

    global IS_PYSIDE
    IS_PYSIDE = True


def load_pyqt4():
    """Sets up PyQt4 nicely to be PySide-compatible as much as possible."""
    # Kill off QString and QVariant to make it act properly like PySide
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)

    from PyQt4 import QtCore
    QtCore._QT_ENGINE = 'PyQt4'

    # Also rename the pyqt things for compatibility.
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    QtCore.Property = QtCore.pyqtProperty

    global IS_PYQT4
    IS_PYQT4 = True


def autoselect():
    """Selects PySide or PyQt4."""

    try:
        # Don't want to import as we need to sip.setapi first
        imp.find_module('PyQt4')
    except ImportError:
        try:
            # Don't want to import two copies (as PySide and as PyQt4)
            imp.find_module('PySide')
        except ImportError:
            raise ImportError('Neither PySide nor PyQt4 is installed.')
        else:
            load_pyside()
    else:
        load_pyqt4()
    zip_imp.cleanup()

IS_PYQT4 = IS_PYSIDE = False
