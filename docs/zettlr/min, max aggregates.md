–-
title: Min, max aggregates
tags: #analysis
Date: 20200514183145
–-

Request: see [issue # 10 on gitlab](https://gitlab.com/krr/autoconfigz3/-/issues/10)

TODO:
- [ ] modify Idp/idp.tx syntax file to accomodate min/max
- [ ] modify Expression.py :
    - [ ] in AAgregate.annotate():
        - [ ] create a new Variable whose name starts with `__` (not a Fresh_variable)
            - [ ] use an AppliedSymbol instead if the aggregate formula has externally quantified variables (stored in .self_vars)
        - [ ] build the 2 constraints described in the issue on gitlab (using make() functions as in Idp/__init__.py : Rule.compute())
        - [ ] set co_constraint to the conjunction of these 2 constraints
- [ ] add a test case in `tests/3 arithmetic`
- [ ] do not send variables starting with `__` to the client

Hopefully, that should do it.