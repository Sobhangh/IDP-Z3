–-
title: Informational relevance
tags: #analysis
Date: 20200518121626
–-

What is "given"  ?
* if x=3 → any arithmetic consequences of x=3 ?  x<4, x~=4, …
* if x~= 3 ? → just that ?
* defined = 5 → how to block communication between the constraint and the co-constraint ?!
* decision variables are never "given" ? otherwise could make environmental implicants irrelevant.  Or OK for decision-only constraints/definitions ? → 2-pass ?

How to deal with implicit dependence between questions, e.g.:
* polygon with Sides = 4 ⇒ "1 angle is 90°" is irrelevant ??  Yet, if false, it cannot be square/rectangle ("all angles are 90°")
* polygon with Sides = 4, All same lengths → all same lengths should be relevant
* if O(M) is relevant and M, O(M) unknown, O(e3) should be relevant
* [quantification over infinite domains](https://autoconfigparam.herokuapp.com/?G4ewxghgRgrgNhATgTwAQG8BQAzAFIgUwjgEoAuQ4zABUwF9NMAXACwJBQ0YEIAPAbUpwAuqmSCiIsql4BeADzJZAPlR5eJBXmQkAdKhy4AjCWWyATLszpqqeQFo1uc6dlHddA4waYA5iGJUWkxgAEsCAHdUAl4ABwgAOwATAiTGIA)

Todo:
- [x] flatten the constraints, i.e. separate the co-constraints
- [x] propagate from goals, avoiding given
- [x] `__goal(symbol instance)` instead of typeConstraint of symbol instances
- [ ] quantifier expansion: should be done by reification + co-constraint (not via simpler) so that the link can be broken by given (but only if no fresh_vars)
- [ ] nested functions: also using co-constraint ? ∃y:O(y)=O(M).  or use a new annotation for links ?
- [ ] add "learned clauses" obtained by propagating with Z3

abandoned:
- [ ] use instantiate, not substitute, for Given. But what if decision given vs environmental ? would break propagation
- [ ] transform into CNF ?
- [ ] collect questions without going through given ?
    - [ ] is a top-down approach… does not work for bottom up reasoning (i.e. if goal is at the bottom)