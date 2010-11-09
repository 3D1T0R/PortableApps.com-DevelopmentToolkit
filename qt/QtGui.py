try:
    from PyQt4.QtGui import *
except ImportError:
    try:
        from PySide.QtGui import *
    except ImportError:
        raise ImportError('Neither PySide nor PyQt4 is installed.')
