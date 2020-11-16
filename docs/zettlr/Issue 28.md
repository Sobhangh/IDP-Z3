–-
title: Issue 28
tags: #issue
Date: 20201016125353
–-
See also [[Non-linear equations in Z3]]
Observations:
* theory.definitions quantify also over the range of a function → correct for non-constructive definitions
    * if replace quantification by injecting f(x), the problem is fixed, but non-constructive definitions yield different results
* attach definition to typeConstraints : not a good idea, because of type constraints may contain inequalities (+repetitions)
* theory.definitions are not simplified by propagation → constraint cannot be solved by Z3
* do not translate definitions → instances not used in theory are not propagated
* append all expanded rules to theory.constraints (i.e. remove quantification)
    * → change_making does not halt !
    * all definitions are subtences now
    * more stuff is relevant
* substitute propagated numeric values in definitions → fixes issues 48

could still be done:
- [ ] avoid duplication of expressions in def_constraints and co_constraints


Code without quantification on range in rule.compute():
~~~~
if  self.out:
    expr = AppliedSymbol.make(self.symbol, self.args\[:-1\])
    expr = self.body.instantiate(self.args\[-1\], expr)
    expr = AQuantification.make('∀', dict(list(self.q_vars.items())\[:-1\]), expr)
else:
    expr = AppliedSymbol.make(self.symbol, self.args)
    expr = AEquivalence.make('⇔', \[expr, self.body\])
    expr = AQuantification.make('∀', {**self.q_vars}, expr)
~~~~