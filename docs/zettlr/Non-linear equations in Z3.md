–-
title: Non-linear equations in Z3
tags: #issue #perf
Date: 20201020103221
–-

# version 4.8.8.0
solver.check() returns `unknown` when there is a non-linearity, e.g. in `tests/5 polygon/Sides3.idp`, `/5 polygon/triangle.idp`, `8 DMN/BMI.idp`. The solver has to be restarted to propage other values (e.g. for `Sides3`).  It returns `sat` as soon as a value is given that removes the non-linearity.
Except in [[Issue 28]] !?
Substituting a numeric value is needed for definitions over infinite domains, e.g. `/tests/3 arithmetic/double_def.idp`

Workaround is to aggressively simplify the theory whenever a (numeric) value is found by propagation.
But it reduces performance unnecessarily when the theory has no non-linearity.
- [ ] simplify only for new numeric value ?
- [ ] do not simplify if theory has no non-linearity

Does not seem to always unit-propagate numeric values.  See [[Issue 28]]
Yet, this code works:
~~~~
from z3 import *
print(get\_version\_string())

p = Bool('p')
bmi = Real("bmi")
weight = Real("weight")
height = Real("height")
solve(p==(bmi==weight/(height*height)), weight==80, height==179, p)

x = Real("x")
forall = ForAll(\[x\], (bmi==x) == (x==weight/(height*height)))
solve(forall, weight==80, height==179)
~~~~


# version 4.8.9.0
issues: [[Issue 28]], [issue 25](https://gitlab.com/krr/autoconfigz3/-/issues/25)
version 4.8.9.0 has regressions for Non-linear real arithmetic (NRA) ([source](https://github.com/Z3Prover/z3/blob/master/RELEASE_NOTES))
- [ ] the new solver can be deactivated by setting `smt.arith.solver=2` (todo)

