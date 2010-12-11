# From http://www.voidspace.org.uk/python/weblog/arch_d7_2006_02_25.shtml#e241
import sys
import os
import imp
import marshal
import tempfile
from zipimport import zipimporter, ZipImportError

"""
A module that patches ``imp.find_module`` to work from within py2exe.

You must call ``import zip_imp`` *before* importing imp.

On finishing you must call ``zip_imp.cleanup()``. This deletes any temporary
files created.

This will only work if you have a zip file on ``sys.path`.
"""

__all__ = ['cleanup']

_zip_file = None
for entry in sys.path:
    if entry.endswith('.zip'):
        _zip_file = entry
        break

_file_array = []

imp._find_module = imp.find_module


def _find_module(name, path=None):
    try:
        return imp._find_module(name, path)
    except ImportError:
        if _zip_file is None:
            raise ImportError
        z = zipimporter(_zip_file)
        try:
            code = z.get_code(name)
        except ZipImportError:
            raise ImportError('Failed to find module: %s' % name)
        mod = _make_pyc(code)
        mod_names = [_zip_file] + name.split('.')
        mod_names[-1] += '.pyc'
        pathname = os.path.join(*mod_names)
        description = ('.pyc', 'rb', imp.PY_COMPILED)
        return (mod, pathname, description)


def _make_pyc(code):
    """
    Turn a bytecode object back into an open file representing a '.pyc' file.

    Uses the spec laid out at :

        http://bob.pythonmac.org/archives/2005/03/24/pycs-eggs-and-zipimport/

    It uses the magic number from the ``imp`` module, and four null bytes to
    represent the modification time of the bytecode file.
    """
    n = tempfile.mktemp()
    t = open(n, 'w+b')
    t.write(imp.get_magic() + chr(0) * 4 + marshal.dumps(code))
    t.seek(0)
    _file_array.append((n, t))
    return t

imp.find_module = _find_module


def cleanup():
    """Clean up any temporary files created when using ``load_module``."""
    for name, file_obj in _file_array:
        # calling close on an already closed file doesn't hurt
        file_obj.close()
        os.remove(name)

if __name__ == '__main__':
    if not hasattr(sys, 'frozen'):
        print 'This test only works from *inside* Movable Python or a',
        print 'program frozen with py2exe.'
        sys.exit()
    #
    name = 'Cookie'
    try:
        file, pathname, description = imp.find_module(name)
    except ImportError:
        print 'Failed to ``find_module``.'
    else:
        print file, pathname, description
        print '``find_module`` succeeded.'
        m = imp.load_module(name, file, pathname, description)
        print "``load_module`` succeeded."
        file.close()
        #
        print
        print m
        print m.Cookie
    #
    cleanup()
