#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
import urllib2
import paf
from iniparse import INIConfig
from urlparse import urlparse
from httplib import HTTPConnection

# Speed things up with concurrency. Each thread spawns two HTTP requests, one at a time.
# If the limit is set too high (8 is too high!?), the network connection falls over.
CONCURRENCY_TECHNIQUE = None
CONCURRENCY_LIMIT = 4

# With further optimisation (multiple connections per site), httplib could be better. At present there's no
# discernible difference, and portableapps.com/bouncer checks get 403 Forbidden which they don't with urllib2.
USE_HTTPLIB = False

if CONCURRENCY_TECHNIQUE == 'multiprocessing':
    from multiprocessing import BoundedSemaphore, Process as Thread
elif CONCURRENCY_TECHNIQUE == 'threading':
    from threading import BoundedSemaphore, Thread


def require(section, key):
    section_name = section._lines[0].name
    if key not in section:
        print '[%s] is missing key %s' % (section_name, key)
    if not section[key]:
        print '[%s] has no value for %s' % (section_name, key)

required = ['Name', 'Description', 'Category', 'SubCategory', 'URL',
'PackageVersion', 'DisplayVersion', 'DownloadFile', 'Hash', 'DownloadSize',
'InstallSize']

optional = ['DownloadPath', 'ReleaseDate', 'UpdateDate', 'InstallSizeTo', 'UpdateOnly']
optional += ['%s_%s' % (p, s) for p in ('DownloadFile', 'Hash',
    'PackageVersion', 'DisplayVersion') for s in paf.LANGUAGES]


def checker(section, appid, semaphore=None):
    if semaphore is not None:
        semaphore.acquire()

    if not paf.appinfo.valid_appid(appid)[0]:
        print '[%s] has an invalid AppID.'

    for key in required:
        require(section, key)

    for key in section:
        if key not in required and key not in optional:
            print '[%s] has extra key %s' % (appid, key)

    if 'PackageVersion' in section:
        try:
            assert len(map(int, section.PackageVersion.split('.'))) == 4
        except:
            print '[%s]:PackageVersion is invalid' % appid

    if 'Hash' in section and (len(section.Hash) != 32 or any(c not in '0123456789abcdef' for c in section.Hash)):
        print '[%s]:Hash is invalid' % appid

    if 'DownloadSize' in section and any(c not in '0123456789' for c in section.DownloadSize):
        print '[%s]:DownloadSize is invalid' % appid

    if 'InstallSize' in section and any(c not in '0123456789' for c in section.InstallSize):
        print '[%s]:InstallSize is invalid' % appid

    for key in ('ReleaseDate', 'UpdateDate'):
        if key in section:
            value = section[key]
            try:
                dateparts = map(int, value.split('-'))
                assert len(dateparts) == 3
                then = datetime.datetime(*dateparts)
                now = datetime.datetime.now()
                assert then.year > 2005
                assert now > then
            except:
                print '[%s]:%s is invalid' % (appid, key)

    if 'URL' in section:
        parsed = urlparse(section.URL)
        if parsed.scheme != 'http':
            print "[%s]:URL isn't an http link."
        else:
            status = url_status(section.URL)
            if status != '200 OK':
                print '[%s]:URL (%s) is invalid (%s)' % (appid, section.URL, status)

    if 'DownloadFile' in section:
        root = section.DownloadPath if 'DownloadPath' in section else 'http://downloads.sourceforge.net/portableapps/'
        path = root + section.DownloadFile
        parsed = urlparse(path)
        if parsed.scheme != 'http':
            print "[%s]:URL isn't an http link."
        else:
            status = url_status(path)
            if status != '200 OK':
                print '[%s] download file %s does not exist (%s)' % (appid, path, status)

    if semaphore is not None:
        semaphore.release()


if USE_HTTPLIB:
    http_connections = {}

    def url_status(url):
        parsed = urlparse(url)
        if parsed.netloc not in http_connections:
            http_connections[parsed.netloc] = HTTPConnection(parsed.netloc)
        connection = http_connections[parsed.netloc]
        connection.request('HEAD', parsed.path)
        response = connection.getresponse()
        response.read()  # Clear the response from the connection
        if response.status in (301, 302):  # Found
            return url_status(response.getheader('Location'))  # Follow redirect
            # Hazard: no recursion checking
        return '%s %s' % (response.status, response.reason)

else:

    class HeadRequest(urllib2.Request):
        def get_method(self):
            return 'HEAD'

    def url_status(url):
        try:
            urllib2.urlopen(HeadRequest(url)).close()
        except urllib2.URLError as e:
            return e
        return '200 OK'


def main():
    iniconfig = INIConfig(urllib2.urlopen('http://portableapps.com/updater/update.ini'))
    if CONCURRENCY_TECHNIQUE in ('multiprocessing', 'threading'):
        main_threaded(iniconfig)
    else:
        main_unthreaded(iniconfig)


def main_unthreaded(iniconfig):
    for appid in iniconfig:
        section = iniconfig[appid]
        checker(section, appid)


def main_threaded(iniconfig):
    semaphore = BoundedSemaphore(CONCURRENCY_LIMIT)
    tasks = []
    for appid in iniconfig:
        section = iniconfig[appid]
        task = Thread(target=checker, args=(section, appid, semaphore))
        tasks.append(task)
        task.start()

    try:
        for t in tasks:
            t.join()
    except KeyboardInterrupt:
        for t in tasks:
            if hasattr(t, 'terminate'):  # multiprocessing
                t.terminate()
        print 'Validation aborted.'
        sys.exit(1)


if __name__ == '__main__':
    main()
