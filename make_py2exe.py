from distutils.core import setup
import py2exe
import os
import re
import sys
import glob
from collections import defaultdict


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

if 'py2exe' not in sys.argv:
    sys.argv.append('py2exe')

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
    # No need for 'images/*.png' etc. yet due to the QRC solution
    'languages/*.ini',
    'app-template/*',
    'app-template/*/*',
    'app-template/*/*/*',
    'app-template/*/*/*/*',
    # Scary. (Or rather, lazy!)
])
data_files += find_data_files(os.path.dirname(sys.executable), '', [
    'msvcr90.dll', 'Microsoft.VC90.CRT.manifest'])

# options['py2exe']['bundle_files']=1 and zipfile=None make it compress less
# well with UPX, so they're not turned on.
setup(
    options={'py2exe': dict(compressed=1, optimize=1, includes=['sip'])},
    data_files=data_files,

    windows=[dict(
        script='main.py',
        icon_resources=[(1, 'graphics/appicon.ico')],
        description='PortableApps.com Development Toolkit',
        # Not including the manifest as it makes the app crash for some reason
        #other_resources=[(24, 1, manifest)],

        dest_base='PortableApps.comDevelopmentToolkit',

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
