from distutils.core import setup
import py2exe
import os
import re
import sys

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

# options['py2exe']['bundle_files']=1 and zipfile=None make it compress less
# well with UPX, so they're not turned on.
setup(
    options={'py2exe': dict(compressed=1, optimize=1, includes=['sip'])},
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
