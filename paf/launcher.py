"""
Package details pertaining to the launcher.
"""

from os import remove
from os.path import isfile
import sys
from subprocess import Popen, PIPE
import config

__all__ = ('Launcher',)


class Launcher(object):
    """
    A class to manage details for the PortableApps.com Launcher.

    Currently this is more or less a stub with only an interface to the
    Generator for use in this own utility's build process.
    """

    def __init__(self, package):
        """Simple constructor; takes a Package."""
        self.package = package

    def build(self):
        """
        Builds a launcher with the PortableApps.com Launcher Generator.

        Raises an ``OSError`` if run on Linux/OS X and Wine is not installed.
        Raises a ``PAFException`` if the package has no AppID (that's about the
        only real requirement for building a launcher).

        Returns True on success, or False if either the PortableApps.com
        Launcher Generator was not found or the launcher fails to build.
        """

        if self.package.appid is None:
            # Hopeless case, the Generator needs an AppID to work on.
            raise PAFException("Can't build Launcher, AppID is not set.")

        generator_path = config.get('Main', 'LauncherGeneratorPath')
        if not generator_path or not isfile(generator_path):
            return False

        package_path = self.package.path()
        # On Linux we can execute it with a Linux path, as Wine will take care
        # of that, but it still expects a Windows path out the other side. Use
        # winepath to convert it to the right Windows path.
        if sys.platform != 'win32':
            # Blocking call; throws an OSError if winepath isn't found
            package_path = Popen(['winepath', '-w', package_path],
                    stdout=PIPE).communicate()[0].strip()

        full_target = self.package.path('%s.exe' % self.package.appid)
        # Make sure it's not there from a previous build.
        if isfile(full_target):
            remove(full_target)

        Popen([generator_path, package_path]).wait()

        return isfile(full_target)
