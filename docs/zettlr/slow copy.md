–-
title: Slow copy
tags: #perf
Date: 20200513173351
–-

Problem: theory of Djordje ran in 1 sec with 0.4.1, but 15 seconds with main on 13 May.

Root cause analysis:
* interrupting the program after 5 seconds shows that it is copying the subtences to create assignment in State.py
    * one subtence is very big due to quantification: 4*4*8*8*14 terms: 14000 terms
    * still, copying it is surprisingly slow
* is the data structure incorrect somehow ?

Differences between 0.4.1 and main:
* 0.4.1 does not do deepcopy of formula, but copies a node whenever it changes
* 0.4.1 does not update every conjuncts if one is false.  main does, to correctly compute relevance

Possible solutions:
* use [ujson](https://stackoverflow.com/questions/24756712/deepcopy-is-extremely-slow) to copy, or [pickle](https://gist.github.com/justinfx/3174062) ?? → 10 times faster ?
    * orjson faster, but needs custom function to (de-)serialize objects
* use 1 deepcopy instead of many copy
    * → a bit slower, and misses some (Z3 ?) consequences
* go back to previous solution where copying is done when necessary: not sure it would help
* rewrite in [[Nim]] ?

* do not instantiate sub_exprs if simpler is available
    * → faster, but "definition proof.idp" becomes unsatisfiable