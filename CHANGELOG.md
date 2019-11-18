Most recent first:

* 9 sept 2019: abstract models: fix bug with checkCode, use given and consequences to simplify them, avoid negations
* GUI: hide symbols starting with '\_'.  Replace '\_' by spaces in symbol names, constructors
* GUI: 2 optimize buttons are now next to entry fields (not in box header).  (Remove "do not optimize" button)
* grammar: "goal <symbol>" forces the goal to be shown expanded
* grammar: "view ('normal' | 'expanded')"  Normal view only shows entry fields for a symbol; expanded view also shows the simplest boolean sub-expressions of the idp theory that contain the symbol ("atomQ").
* docs folder contains documentation, such as python call graphs and description of REST API
* fix Issue #1: show entry fields for all possible combinations of arguments of functions / predicates.
* refactoring:
    * remove 'init' method of /eval
    * simplify REST API
    * reorganize source code file per chronological order of calls
    * remove unused code
* improve minization of real terms for theories with strict inequalities (by repeatedly calling minimize)
