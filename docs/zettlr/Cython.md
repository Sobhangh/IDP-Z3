–-
title: Cython
tags: #perf
Date: 20200616143932
–-

Ref: [cython.org](https://cython.org/)

Done:
* add Cython to requirements.txt
* python3.8 -m pip install -r requirements.txt
* undefined symbol: [_py_zeroStruct](https://stackoverflow.com/questions/44737063/cython-bbox-so-undefined-symbol-py-zerostruct) → language level
* problem with pached functions of Expression → add \[# cython: binding=True](https://groups.google.com/forum/#!topic/cython-users/1vEQqVsI8Zo)
* [HTML annotation](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html?highlight=html#primes): cython -a idp_solver/Substitute.pyx
    * need to add a setup.py with cythonize(xxx, annotate=True, language_level=3)
    * pyThreadState error
* Interpret.py → Interpret.pyx : compilation done (where ?), but no gains
    * → test.py unchanged at 3.9 sec
    * → Djordje's abstract : 0.8, 2.0, 2.0

Todo:
- [ ] more type annotations ?
