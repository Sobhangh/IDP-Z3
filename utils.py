"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""
from collections import ChainMap
import itertools, time
import os


""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.

DEBUG = True

start = time.time()
def log(action):
    global start
    print("*** ", action, round(time.time()-start,3))
    start = time.time()


nl = "\r\n"
indented = "\r\n  "

LOG_FILE = None
def Log_file(path):
    global LOG_FILE
    if 'proof' in path or 'andbox' in path:
        path, filename = os.path.split(path)
        LOG_FILE = newpath = os.path.join(path, filename.replace('.idp', '_log.txt'))
        indent = 0
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    else:
        LOG_FILE = None

def Log(string, indent=0):
    global LOG_FILE
    if LOG_FILE:
        f = open(LOG_FILE, "a")
        out = string.replace(nl, nl+(' '*indent))
        f.write(out)
        f.close()



def unquote(s):
    if s[0]=="'" and s[-1]=="'":
        return s[1:-1]
    return s

def in_list(q, ls):
    if not ls: return True # e.g. for int, real
    if len(ls)==1: return q == ls[0]
    return Or([q == i for i in ls])


def is_number(s):
    if str(s) in ['True', 'False']: return False
    try:
        float(eval(str(s))) # accepts "2/3"
        return True
    except:
        return False



def splitLast(l):
    return l[:-1], l[-1]


def applyTo(sym, arg):
    if len(arg) == 0:
        return sym
    return sym(arg)

def mergeDicts(l):
    # merge a list of dicts (possibly a comprehension
    return dict(ChainMap(*reversed(list(l))))

# Proof #########################################################

import collections

class Proof(collections.OrderedDict, collections.MutableSet):
    # Dict[code, is_subtence]
    def __init__(self, elem=None):
        if elem is not None:
            self[elem.code] = elem.is_subtence
            self.add(elem) # add proof of elem

    def update(self, other):
        " adds the other proof "
        if type(other) == Proof:
            for k, v in other.items():
                self[k] = v
        return self

    def add(self, elem):
        " adds the proof of elem, and elem if it is a subtence "
        self.update(elem.proof)
        if elem.is_subtence:
            self[elem.code] = elem.is_subtence
        return self

    def extend(self, elems):
        " adds a list of expressions and their proofs "
        for elem in elems:
            self.add(elem)
        return self

    def __repr__(self):
        return 'Proof([%s])' % (', '.join(map(repr, self.keys())))

    def __str__(self):
        return '{%s}' % (', '.join(map(repr, self.keys())))

    """
    difference = property(lambda self: self.__sub__)
    difference_update = property(lambda self: self.__isub__)
    intersection = property(lambda self: self.__and__)
    intersection_update = property(lambda self: self.__iand__)
    issubset = property(lambda self: self.__le__)
    issuperset = property(lambda self: self.__ge__)
    symmetric_difference = property(lambda self: self.__xor__)
    symmetric_difference_update = property(lambda self: self.__ixor__)
    def union(self, other):
        return self or other
    """

class NoSet(object):
    def update(self, other):
        return self
    def add(self, elem):
        return self
    def extend(self, elems):
        return self

class ProofZ3(NoSet):
    def __str__(self):
        return 'Z3 proof'
