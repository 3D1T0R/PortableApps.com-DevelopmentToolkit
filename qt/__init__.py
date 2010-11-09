"""
A simple wrapper for both PySide and PyQt4 when they are considered
interchangeable, fixing up bad things in PyQt4 if it's selected.
"""

__all__ = ['QtCore', 'QtGui']

from qt import QtCore, QtGui
