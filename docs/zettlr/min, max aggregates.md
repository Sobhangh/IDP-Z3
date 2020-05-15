–-
title: Min, max aggregates
tags: #analysis
   ID: 20200514183145
–-

Request: see issue # 10 on gitlab

TODO:
- [ ] modify Idp/idp.tx syntax file to accomodate min/max
- [ ] modify Expression.py :
    - [ ] in AAgregate.annotate():
        - [ ] create a new Variable whose name starts with `_` (not a Fresh_variable)
        - [ ] build the 2 constraints described in the issue on gitlab (using make() functions as in Idp/__init__.py : Rule.compute())
        - [ ] set just_branch to the conjunction of the 2 constraints
- [ ] add a test case in `tests/3 arithmetic`

Hopefully, that should do it.