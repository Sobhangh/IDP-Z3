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
from collections import ChainMap, Iterable
import itertools
import time


""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.



start = time.process_time()
def log(action):
    global start
    print("*** ", action, round(time.process_time()-start,3))
    start = time.process_time()


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
        float(eval(str(s if not s.endswith('?') else s[:-1]))) # accepts "2/3" or "3.1415?"
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

# OrderedSet #############################################

class OrderedSet(dict):
    def __init__(self, els=[]):
        assert isinstance(els, Iterable)
        super(OrderedSet, self).__init__(zip((e.code for e in els), els))

    def add(self, el):
        self[el.code] = el