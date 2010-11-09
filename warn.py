import warnings
from qt.QtGui import QMessageBox
from utils import _S, _


def warn_qt(message, category, filename, lineno, file_=None, line=None):
    "Warning handler to show a Qt QMessageBox."
    if type(message) == tuple:
        window, message = message
    else:
        window = None

    msg = _S('%(message)s\n\n(From %(file)s, line %(line)s)') % {
            'message': message, 'file': filename, 'line': lineno}

    # Potential danger point: if the QApplication hasn't been initialised yet
    # this will abort and there's no way I can stop it as far as I can tell -
    # try..except doesn't help.
    QMessageBox.warning(window, _('PortableApps.com Development Toolkit'), msg,
            QMessageBox.Ok)


def set_warnings_qt():
    "Set warnings to trigger warn_qt."
    #old_showwarning = warnings.showwarning
    warnings.showwarning = warn_qt
    warnings.simplefilter('always')  # Always warn, not just first time
