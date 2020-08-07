–-
title: bug in relevance.idp
tags: #bug
Date: 20200430161236
–-

option: simplify constraint only if it is not a justification of the propagated atoms (→ keep track of what justifies a propagated value)

## Problem 1
set q=false in GUI ⇒ q becomes irrelevant, but shouldn't. (it works if ~q added to theory)
```
vocabulary {
    p q r
}
theory {
  p | q.
}
```
Option
- [x] do not reduce sub_exprs to expr if expr is a consequence of self !? (but set simpler anyway)
    - [x] check that another sub_exprs was unknown before
    - [ ] or keep track of the expression that created the substitution ?  Also useful for explain !
    but what about Z3 consequences, such as `Base=4`: they do not come from one constraint → always simplified away ?
- [x] + fix conjunction, implication, …

## Problem 2
r is relevant with this code, but shouldn't.
```
vocabulary {
    p l r rd i
}
theory {
  { p <- l | r.}
  p.l. 
}
goal p
```

Root cause:
* after p is set to True, Expression.substitute stops because (p∨~p) has value True 
* update_arith replaces Base * Base by Number(16) → no Base symbols anymore

It works if the last constraint is `l. p.` instead.

Option:
- [x] remove `if self.value is not None: return self` in Expr.substitute (and AppliedSymbol.substitute)
    - but square.z3 says `16=Base\*Base` becomes irrelevant (arithmetic is simplified)
    - performance hit: + 25 % 
X only substitute the ground (non-defined) facts ?  (here, substitute l, not p)  Hard to do ! Not always equivalent
X  substitute in all tree, then simplify in second step ?  Only for performance purposes.  Batch substitute is preferred.

## Problem 3
some subtences should be relevant in isa.py

root cause: 
* quantified comparisons not considered subtences
* mark_subtences is run before expansion to avoid too many lines in GUI, but it impacts relevance !


## other problem
p(f) is relevant ! Because of type constraint on p ?
```
vocabulary {
    type binary constructed from {t,f}
    p(binary)
}
theory {
  p(t).
}
```
Root cause: get_relevant_subtences considers all instances of relevant symbols
because subtences() only returns subtences, not questions