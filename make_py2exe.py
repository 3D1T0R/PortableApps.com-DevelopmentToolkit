from distutils.core import setup
import py2exe
import os
from os.path import join, isdir
import re
import sys
import shutil
import glob
from collections import defaultdict
from paf import create_package
from config import ROOT_DIR


__all__ = ('do_all', 'build', 'paffify', 'upload')


def find_data_files(source, target, patterns):
    """
    Locates the specified data-files and returns the matches in a data_files
    compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.

    Modified slightly from http://www.py2exe.org/index.cgi/data_files
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = defaultdict(list)
    for pattern in patterns:
        pattern = os.path.join(source, pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename,
                    source))
                ret[os.path.dirname(targetpath)].append(filename)
    return sorted(ret.items())


version = sys.argv[-1]
if re.findall('^([0-9]+\.)*[0-9]+(b[0-9]+)?$', version):
    del sys.argv[-1]
else:
    version = '1.0.0.0'

manifest = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="PortableApps.comDevelopmentToolkit"
    type="win32"
/>
<description>PortableApps.com Development Toolkit</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

data_files = find_data_files('', '', [
    # No need for resources/ - its own PAF stuff gets used for build only and
    # the images go in the QRC and so get built in
    'languages/*.ini',
    'app-template/*',
    'app-template/*/*',
    'app-template/*/*/*',
    'app-template/*/*/*/*',
    # Scary. (Or rather, lazy!)
])
data_files += find_data_files(os.path.dirname(sys.executable), '', [
    'msvcr90.dll', 'Microsoft.VC90.CRT.manifest'])


def build():
# options['py2exe']['bundle_files']=1 and zipfile=None make it compress less
# well with UPX, so they're not turned on.
    argv = sys.argv
    sys.argv = [sys.argv[0], 'py2exe']
    success = setup(
    options={'py2exe': dict(compressed=1, optimize=1, includes=['sip'])},
    data_files=data_files,
    windows=[dict(
        script='main.py',
        icon_resources=[(1, 'resources/appicon.ico')],
        description='PortableApps.com Development Toolkit',
        # Not including the manifest as it makes the app crash for some reason
        #other_resources=[(24, 1, manifest)],

        dest_base='DevelopmentToolkit',

        # VersionInfo table stuff
        version=version,
        name='PortableApps.com Development Toolkit',
        comments=('A simple yet powerful way to develop portable apps. ' +
               'For additional details, visit PortableApps.com'),
        company_name='PortableApps.com',
        copyright='PortableApps.com',
        trademarks='PortableApps.com is a Trademark of Rare Ideas, LLC.',
        )],
    )
    sys.argv = argv
    return success


def paffify():
    """We muft paffify the package."""
    global paf_path
    paf_path = join(ROOT_DIR, 'dist-paf')
    if isdir(paf_path):
        shutil.rmtree(paf_path)
    package = create_package(paf_path, True)

    copy('appinfo.ini', ('App', 'AppInfo'))
    package.appinfo.load()
    copy('appicon.ico', ('App', 'AppInfo'))
    copy('appicon_16.png', ('App', 'AppInfo'))
    copy('appicon_32.png', ('App', 'AppInfo'))
    copy('appicon_128.png', ('App', 'AppInfo'))

    # Replace help.html
    os.remove(join(paf_path, 'help.html'))
    copy('help.html', ())

    # At the present we wish to remove the splash screen.
    os.remove(join(paf_path, 'App', 'AppInfo', 'Launcher', 'splash.jpg'))
    copy('pal.ini', ('App', 'AppInfo', 'Launcher',
        'PortableApps.comDevelopmentToolkit.ini'))
    os.rename(join(ROOT_DIR, 'dist'),
            join(paf_path, 'App', 'DevelopmentToolkit'))

    return package

def upload():
    """Voom!"""
    raise NotImplementedError()


def copy(source, target):
    shutil.copy(join(ROOT_DIR, 'resources', source),
            join(paf_path, *target))


def do_all():
    print "Compiling it..."
    if not build():
        print "Failed to build with py2exe!"
        return
    print "Bending it into shape..."
    package = paffify()
    print "Finding a pal for it..."
    if not package.launcher.build():
        print "Couldn't find PortableApps.com Launcher!",
        print "(Please run and configure this before trying to build it.)"
        return
    print "Scrunching it up..."
    if not package.compact():
        print "Couldn't find PortableApps.com AppCompactor!",
        print "(Please run and configure this before trying to build it.)"
        return
    print "Tying it up in knots..."
    if not package.installer.build():
        print "Couldn't find PortableApps.com Installer!",
        print "(Please run and configure this before trying to build it.)"
        return
    #print "Sending it up the tube..."
    #upload()
    print "Delivered."

if __name__ == '__main__':
    do_all()
