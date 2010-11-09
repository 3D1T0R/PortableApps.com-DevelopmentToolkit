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
    Signal = pyqtSignal
    Slot = pyqtSlot
    Property = pyqtProperty
