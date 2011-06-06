#!/usr/bin/env python

"""Validate all packages in a given directory."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frontend.cli.validate import validate


for path in os.listdir(sys.argv[1]):
    if not os.path.isdir(path) or os.path.basename(path) == 'PortableApps.com':
        # Skip files and the "PortableApps.com" directory (Platform etc.)
        continue
    title = os.path.basename(path)
    print title
    print '=' * len(title)
    print
    validate(os.path.abspath(path), rst=True)
