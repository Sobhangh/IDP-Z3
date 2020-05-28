–-
title: O(M) in KnownTemp
tags: #fixed
Date: 20200427134729
–-

Problem: when I choose M->e2, O(M) becomes "to be verified" instead of verified
and when I choose T = 50, OMinT(M) <T < OMaxT(M) is also to be verified

Rationale:
* they can be derived by injecting the given values and universals

Root cause:
* O(M) is not a ground atom.  I need to inject e2, then use universals (not the other way around) → need to compute the fix point ?
* Once I replace M by e2, O(M) has no decision anymore → environmental !

Solution:
- [x] has_environmental should use values
- [x] do not cache has_environmental

still not working perfectly…  Enter T=50, Garanteed ⇒ O(M) should not be "to be verified"
- [x]  don't show _O(M)