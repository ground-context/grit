#!/usr/bin/env python3

import subprocess
import os
import uuid
import time

from typing import List

from . import globals

CHECKOUT_EPSILON = 0.50
MERGE_EPSILON = 1
COMMIT_EPSILON = 0.05


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
        self.currentBranch = __get_current_branch__()

    def __enter__(self):
        subprocess.run(['git', 'checkout', self.target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(CHECKOUT_EPSILON)

    def __exit__(self, type, value, traceback):
        subprocess.run(['git', 'checkout', self.currentBranch], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(CHECKOUT_EPSILON)

def gitlog(sourceKey, typ):
    typ = typ.lower()
    ld = []
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        rawgitlog = __readProc__(['git', 'log', '--all'])
        d = {}
        for line in rawgitlog:
            if 'commit' in line[0:6]:
                d['commit'] = line.split(' ')[1]
            elif 'Author' in line[0:6]:
                d['Author'] = ' '.join(line.split()[1:])
            elif 'Date' in line[0:4]:
                d['Date'] = ' '.join(line.split()[1:])
            elif 'class:' in line:
                line = line.split()
                d['class'] = line[1]
                ld.append(d)
                d = {}
    return ld

def get_first_commit(sourceKey, typ):
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        return __readProc__(['git', 'rev-list', '--max-parents=0', 'HEAD'])[0]

def get_ver_commits(sourceKey, typ):
    ld = gitlog(sourceKey, typ)
    return list(map(lambda x: x['commit'],
                    filter(lambda x: 'Version' in x['class'],
                           ld)))

def get_commits(sourceKey, typ):
    ld = gitlog(sourceKey, typ)
    return list(map(lambda x: x['commit'], ld))

def get_branch_commits(sourceKey, typ):
    # Warning: returns iterator not list (not subscriptable)
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        def clean(s):
            s = s.strip()
            if '* ' in s:
                s = s[2:]
            return s
        branches = [i for i in map(clean, __readProc__(['git', 'branch'])) if i]
        commits = [i for i in __readProc__(['git', 'rev-parse', '--branches']) if i]

    return zip(branches, commits)

def __get_current_branch__():
    def split(s):
        s = s.strip()
        return s.split()
    return [i for i in map(split, __readProc__(['git', 'branch'])) if len(i) == 2][0][1]

def new_branch_name(sourceKey, typ):
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        rawgitlog = __readProc__(['git', 'branch'])
        new_name = uuid.uuid4().hex
        while new_name in rawgitlog:
            new_name = uuid.uuid4().hex

    return new_name

def __runProc__(commands: List):
    start = time.time()
    subprocess.run(commands, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    end = time.time()

    if 'checkout' in commands:
        time.sleep(CHECKOUT_EPSILON)
        print(end-start)
    elif 'commit' in commands:
        time.sleep(COMMIT_EPSILON)
        print(end-start)
    elif 'merge' in commands:
        time.sleep(MERGE_EPSILON)
        print(end-start)

def __readProc__(commands: List):
    p1 = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    rawgitlog = str(p1.stdout, 'UTF-8').split('\n')
    return rawgitlog

def runThere(commands: List, sourceKey, typ):
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        __runProc__(commands)

def readThere(commands: List, sourceKey, typ):
    with chinto(os.path.join(globals.GRIT_D, typ, sourceKey)):
        out = __readProc__(commands)
    return out