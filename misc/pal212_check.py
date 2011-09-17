#!/usr/bin/env python

'''Check if apps require an upgrade from PAL 2.1.1 to 2.1.2.'''

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paf
from iniparse import INIConfig
from ConfigParser import ParsingError
from collections import defaultdict


def first(iterable):
    '''INIConfig/INIScetion have no easy way of accessing [0].'''
    return iter(iterable).next()


def last(iterable):
    '''INIConfig/INIScetion have no easy way of accessing [-1].'''
    for i in iterable:
        pass
    return i


hide_skips = ('not PAL', 'missing FilesMove and/or DirectoriesMove', 'known good')

known_inside_package = (
        '%PAL:AppDir%',
        '%PAL:DataDir%',
        '%FullAppDir%',
        )

known_outside_package = (
        '%PAL:Drive%',
        '%APPDATA%',
        '%LOCALAPPDATA%',
        '%USERPROFILE%',
        )

skipped = defaultdict(list)
known_bad = {}
maybe_bad = {}


def check_package(path):
    title = os.path.basename(path)

    if not os.path.isdir(path) or title == 'PortableApps.com':
        # Skip files and the "PortableApps.com" directory (Platform etc.)
        return

    package = paf.Package(path)

    if not package.launcher_is_pal:
        skipped['not PAL'].append(title)
        return

    for launcher_path in package.launcher.paths():
        check_launcher(package.path(launcher_path), title)


def check_launcher(launcher_path, title):
    with open(launcher_path) as f:
        try:
            ini = INIConfig(f)
        except ParsingError:
            skipped['bad launcher.ini'].append(title)

    if 'FilesMove' not in ini or 'DirectoriesMove' not in ini:
        skipped['missing FilesMove and/or DirectoriesMove'].append(title)
        return

    last_file = ini.FilesMove[last(ini.FilesMove)]
    first_dir = ini.DirectoriesMove[first(ini.DirectoriesMove)]

    if (any(last_file.startswith(s) for s in known_inside_package) and
        any(first_dir.startswith(s) for s in known_outside_package)):
        known_bad[title] = last_file, first_dir
    elif (any(last_file.startswith(s) for s in known_outside_package) or
            any(first_dir.startswith(s) for s in known_inside_package)):
        skipped['known good'].append(title)
    else:
        maybe_bad[title] = (last_file, first_dir)


def main(containing_directory):
    for path in os.listdir(containing_directory):
        check_package(os.path.abspath(os.path.join(containing_directory, path)))

    print_results()


def print_results():
    for label, description, items in (
            ('Known bad', 'These are losing data and must be upgraded to PAL 2.1.2.', known_bad),
            ('Maybe bad', 'If the last file is inside the package and the first dir is outside the package, '
                'these will be losing data and must be upgraded to PAL 2.1.2.', maybe_bad)):
        if items:
            print label
            print len(label) * '='
            print
            print description
            print
            for title, (last_file, first_dir) in items.iteritems():
                print title
                print '-' * len(title)
                print
                print 'Last file:', last_file
                print 'First dir:', first_dir
                print

    if not known_bad and not maybe_bad:
        print 'No problems found.'
        if skipped:
            print

    if skipped:
        if known_bad or maybe_bad:
            print 'Skipped'
            print '======='
            print

        for category, items in skipped.iteritems():
            if category in hide_skips:
                continue

            for item in items:
                print 'Skipped (%s): %s' % (category, item)

if __name__ == '__main__':
    main(sys.argv[1])
