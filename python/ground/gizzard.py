#!/usr/bin/env python3

import subprocess
import os

from . import globals

class chinto(object):
    def __init__(self, target):
        self.original_dir = os.getcwd()
        self.target = target

    def __enter__(self):
        os.chdir(self.target)

    def __exit__(self, type, value, traceback):
        os.chdir(self.original_dir)

class chkinto(object):
    def __init__(self, commit):
        self.target = commit

    def __enter__(self):
        p1 = subprocess.Popen(['git', 'checkout', self.target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p1.wait()
        p1.terminate()
        p1.wait()

    def __exit__(self, type, value, traceback):
        p1 = subprocess.Popen(['git', 'checkout', 'master'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p1.wait()
        p1.terminate()
        p1.wait()

def gitlog(sourceKey, typ):
    typ = typ.lower()
    ld = []
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        p1 = subprocess.Popen(['git', 'log', '--follow', '--', sourceKey+'.json'], stdout=subprocess.PIPE,  stderr=subprocess.DEVNULL)
        rawgitlog = str(p1.stdout.read(), 'UTF-8').split('\n')
        p1.stdout.close()
        p1.terminate()
        p1.wait()
        d = {}
        for line in rawgitlog:
            if 'commit' in line[0:6]:
                d['commit'] = line.split(' ')[1]
            elif 'Author' in line[0:6]:
                d['Author'] = ' '.join(line.split()[1:])
            elif 'Date' in line[0:4]:
                d['Date'] = ' '.join(line.split()[1:])
            elif 'id:' in line and 'class:' in line:
                line = line.split()
                d['id'] = int(line[1].split(',')[0])
                d['class'] = line[3]
                ld.append(d)
                d = {}
    return ld

def get_ver_commits(sourceKey, typ):
    ld = gitlog(sourceKey, typ)
    return list(map(lambda x: (x['commit'], x['id']),
                    filter(lambda x: 'Version' in x['class'],
                           ld)))