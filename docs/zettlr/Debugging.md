–-
title: Debugging
tags: #general
Date: 20200407220958
–-

Don't use the debugger, use [[debugWithYamlLog]]  !

Challenges and solutions:
* highly recursive → Log statements, and asserts (+ conditional breakpoints) 
* complex data structure → improve visualisation →use **YAML logs**
* fix a problem results in a new one → seek to understand → **mermaid chart**, **logs**
* too many changes to main.py → Sandbox executed first

Phases of debugging:
* document theory or principles (possibly in math form)
* simplify test case → sandbox.py
* identify root causes: 
    * identify relevant information → adapt `__debug__` methods to show them
    * place assert to test hypothesis (and keep it there, with 2 spaces after assert, so that it can be removed before release)

