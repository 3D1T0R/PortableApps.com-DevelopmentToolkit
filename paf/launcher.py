"""
Package details pertaining to the launcher.
"""

import os
from subprocess import Popen
import config
from utils import path_windows
from paf import PAFException
from glob import glob

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

    def path(self):
        """Get the path to the first INI file in App\\AppInfo\\Launcher."""
        try:
            path = self.paths()[0]
        except IndexError:
            raise PAFException('Unable to find any launcher INI files in %s' %
                    self.package.path('App', 'AppInfo', 'Launcher'))
        return path

    def paths(self):
        """Find all launcher INI files in App\\AppInfo\\Launcher."""
        # TODO: this doesn't really belong here. We need a LauncherManager or
        # similar, perhaps just make this Package.launcher_paths() and have
        # Package.launchers = {basename: Launcher()}?
        return glob(self.package.path('App', 'AppInfo', 'Launcher', '*.ini'))

    def build(self, block=True):
        """
        Builds a launcher with the PortableApps.com Launcher Generator.

        Raises an ``OSError`` if run on Linux/OS X and Wine is not installed or
        PortableApps.comLauncherGenerator.exe does not have mode +x.

        Raises a ``PAFException`` if the package has no AppID (that's about the
        only real requirement for building a launcher).

        Returns True on success, or False if either the PortableApps.com
        Launcher Generator was not found or the launcher fails to build. If the
        parameter ``block`` is set to ``False``, this will be an asynchronous
        call and the ``subprocess.Popen`` process handle will be returned.
        """

        if self.package.appid is None:
            # It's a hopeless case, as you can see
            # And in your place I would not be
            # But don't blame me, I'm sorry to be
            # Of your pleasure a diminutioner.
            raise PAFException("Can't build Launcher, AppID is not set.")

        generator_path = config.get('Main', 'LauncherPath')
        if not generator_path or not os.path.isfile(generator_path):
            return False

        full_target = self.package.path('%s.exe' % self.package.appid)
        # Make sure it's not there from a previous build.
        if os.path.isfile(full_target):
            os.remove(full_target)

        proc = Popen([generator_path, path_windows(self.package.path(), True)])
        if block:
            proc.wait()
            return os.path.isfile(full_target)
        else:
            return proc
