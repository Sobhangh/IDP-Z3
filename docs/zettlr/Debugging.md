–-
title: Debugging
tags: #general
   ID: 20200407220958
–-
 
Challenges and solutions:
* highly recursive → **use conditional breakpoints**, Log statements, and asserts
* complex data structure → improve visualisation →use **repr**, **logs**
* fix a problem results in a new one → seek to understand → **mermaid chart**, **logs**
* too many changes to main.py → Sandbox executed first

Phases of debugging:
* document theory or principles (possibly in math form)
* simplify test case → sandbox.py
* identify root causes: 
    * place conditional breakpoints occurring before observed problem → narrow the place of the problem
    * place assert to test hypothesis (and keep it there, with 2 spaces after assert, so that it can be removed before release)
    * test hypothesis : change the cause manually and see it if fixes it ?

