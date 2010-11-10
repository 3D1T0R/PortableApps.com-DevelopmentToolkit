import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
try:
    from PyQt4.QtCore import *
except ImportError:
    try:
        from PySide.QtCore import *
    except ImportError:
        raise ImportError('Neither PySide nor PyQt4 is installed.')
    else:
        _QT_ENGINE = 'PySide'
else:
    Signal = pyqtSignal
    Slot = pyqtSlot
    Property = pyqtProperty
    _QT_ENGINE = 'PyQt4'
