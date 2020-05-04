–-
title: bug in relevance.idp
tags: #bug
   ID: 20200430161236
–-

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
- [ ] do not reduce sub_exprs to expr if expr is a consequence of self !? (but set simpler anyway)
    - [ ] check that another sub_exprs was unknown before
    - [ ] check that it is different from simpler (in change() ?)
    - [ ] check that it is not the last unknown sub_exprs (but beware of (p ∨ ~p)) 
    - [ ] or keep track of the expression that created the substitution ?  Also useful for explain !
    but what about Z3 consequences, such as `Base=4`: they do not come from one constraint → always simplified away ?
- [ ] + fix conjunction, implication, …

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

It works if the last constraint is `l. p.` instead.

Option:
- [ ] remove `if self.value is not None: return self` in Expr.substitute (and AppliedSymbol.substitute)
    - but square.z3 says `16=Base\*Base` becomes irrelevant (because of simplification of Implication)
    - performance hit: + 25 % 
X only substitute the ground (non-defined) facts ?  (here, substitute l, not p)  Hard to do ! Not always equivalent
X  substitute in all tree, then simplify in second step ?  Only for performance purposes.  Batch substitute is preferred.


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