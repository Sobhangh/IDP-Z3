–-
title: Informational relevance
tags: #analysis
   ID: 20200518121626
–-

What is "given"  ?
* if x=3 → any arithmetic consequences of x=3 ?  x<4, x~=4, …
* if x~= 3 ? → just that ?
* defined = 5 → how to block communication between the constraint and the co-constraint ?!
* decision variables are never "given" ? otherwise could make environmental implicants irrelevant.  Or OK for decision-only constraints/definitions ? → 2-pass ?

How to deal with implicit dependence between questions, e.g.:
* polygon with Sides = 4 ⇒ "1 angle is 90°" is irrelevant ??  Yet, if false, it cannot be square/rectangle ("all angles are 90°")
* if O(M) is relevant and M unknown, O(e3) should be relevant

Options:
- [ ] flatten the constraints, i.e. separate the co-constraints
    - [ ] + collect questions without going through co-constraints
- [ ] use instantiate, not substitute, for Given. What if environmental ?

- [ ] transform into CNF ?
- [ ] collect questions without going through given ?
    - [ ] is a top-down approach… does not work for bottom up reasoning (i.e. if goal is at the bottom)