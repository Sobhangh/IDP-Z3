–-
title: Profiling
tags: #Perf
Date: 20200417110903
–-

[Types of profilers](https://blog.blackfire.io/profiling-101-for-python-developers-the-many-types-of-profilers-2-6.html)

You can pause a long program in debug mode, by clicking the pause button (in VSCode, PyCharm, …).  This indicates where it spends most of its time.

## pyinstrument
python3 -m pyinstrument -o test.log test.py

shows that substitute() is the bottleneck
Options:
- [ ] use pypy locally
- [ ] cache the propagation of universals in Case
- [ ] non-interactive version
- [ ] use [cython](https://cython.org/) for substitute on GAE
- [ ] use reification of quantified formulas + Z3 substitute → major rewrite !
- [X] use `__slots__` → no change
- [ ] avoid function lookup by testing type