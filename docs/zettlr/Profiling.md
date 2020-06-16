–-
title: Profiling
tags: #Perf
Date: 20200417110903
–-

[Types of profilers](https://blog.blackfire.io/profiling-101-for-python-developers-the-many-types-of-profilers-2-6.html)

You can pause a long program in debug mode, by clicking the pause button (in VSCode, PyCharm, …).  This indicates where it spends most of its time.

## pyinstrument
python3 -m pyinstrument -o test.log test.py

installation on python3.8:
* sudo apt-get install python3.8-dev ([source](https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory))
* python3.8 -m pip install pyinstrument

## Observations:
* shows that substitute() is the bottleneck
* translate is also very time consuming

rest.py on Djordje abstract theory:
* 2.2 sec in full_propagate (1 sec in substitute + 0.8 in translate)
* 1.6 in add_given (mostly translate)


## Options:
- [ ] use [cython](https://cython.org/) for substitute on GAE
- [ ] use reification of quantified formulas + Z3 substitute → major rewrite !
- [ ] use pypy locally
- [x] cache the propagation of universals in Case
- [ ] non-interactive version
- [x] use `__slots__` → no change
- [ ] avoid function lookup by testing type