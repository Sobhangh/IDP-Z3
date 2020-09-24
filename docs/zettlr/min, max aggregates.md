–-
title: Min, max aggregates
tags: #analysis
Date: 20200514183145
–-

Request: see [issue # 10 on gitlab](https://gitlab.com/krr/autoconfigz3/-/issues/10)

Co-constraints for the simple case: create variable (here a439) with co-constraints
~~~~
// a439 = min{x[type]:phi(x):term(x)}
?x[type]: phi(x) & term(x) = a439.
!x[type]: phi(x) => term(x) =< a439.
~~~~
A bit more complex when the aggregates contain variable y:
~~~~
// a439(y) = min{x[type]:phi(x,y):term(x)}
!y[?]: ?x[type]: phi(x,y) & term(x) = a439(y).
!y[?]: !x[type]: phi(x,y) => term(x) =< a439(y).
~~~~
⇒ Alternative: expand quantifier of y before creating the co-constraints.

# TODO:
- [ ] preliminary : `Substitute.py\AQuantification` expand outermost quantifier before innermost ones
    - and run `python test.py` to detect any regression
- [ ] modify Idp/idp.tx syntax file to accomodate min/max
- [ ] modify `Substitute.py\AQuantification` :
    - [ ] use .make() to create a new Fresh_Variable of appropriate type
        - [ ] the name is the code of the aggregate `min{...}`
    - [ ] store that variable in self.simpler
    - [ ] build the 2 co-constraints (using make() functions as in Idp/__init__.py : Rule.compute())
    - [ ] set co_constraint to the conjunction of these 2 constraints
- [ ] modify Expression.py\Fresh_Variable: process co-constraints in .collect()
- [ ] add test cases in `tests/3 arithmetic`: simple, complex, with environment/decision variables
- [ ] update sphinx documentation
- [ ] close [issue # 10 on gitlab](https://gitlab.com/krr/autoconfigz3/-/issues/10)
