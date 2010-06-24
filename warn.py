import warnings
import logging
from PyQt4.QtGui import QMessageBox
from utils import _S, _

logging.basicConfig(level=logging.INFO)

def warn_ui(message, category, filename, lineno, file=None, line=None):
    if type(message) == tuple:
        window, message = message
    else:
        window = None

    msg = _S('%(message)s\n\n(From %(file)s, line %(line)s)') % {'message': message, 'file': filename, 'line': lineno }

    # Potential danger point: if the QApplication hasn't been initialised yet
    # this will abort and there's no way I can stop it as far as I can tell -
    # try..except doesn't help.
    QMessageBox.warning(window, _('PortableApps.com Development Toolkit'), msg, QMessageBox.Ok)

#old_showwarning = warnings.showwarning
warnings.showwarning = warn_ui
warnings.simplefilter('always') # Always use warnings, don't just show it the first time.
