–-
title: square(x)
tags: #analysis
Date: 20200515110058
–-

It would be nice to be able to define `square(x)` like this: `{!x[real] : square(x) = x*x. }`
When I do that in tests/arithmetic/square.idp, it does not infer Base correctly.

Root cause:
* Z3 result is probably unknown, not sat/unsat, in propagate()

Option:
* identify the subset of definitions that can be implemented as substitutions: `{!x: f(x)= …x… }` and substitute in place instead of attaching the co_constraint
    * set the new formula in self.simpler
    * allow `if..then..else` constructs.