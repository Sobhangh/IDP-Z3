–-
title: Bootstrapping
tags: 
   ID: 20200507091746
–-

[Recursive datatypes](https://rise4fun.com/z3/tutorial)
recursive functions: [example](https://stackoverflow.com/questions/36431075/how-to-deal-with-recursive-function-in-z3), [need version > 4.4.2](https://stackoverflow.com/questions/38578674/using-define-fun-rec-in-smt?noredirect=1&lq=1)
* [Z3 online](http://compsys-tools.ens-lyon.fr/z3/) : not enough
* [run SMTLIB via Z3 api](https://github.com/Z3Prover/z3/issues/1811)

```
(declare-datatypes () ((Proposition p q r s t)))
(declare-datatypes () ((Formula (atomic (atom Proposition)) (negation (negated Formula)) )))
(declare-const phi Formula)
(declare-const psi Formula)
(assert (= phi psi))
(check-sat)
(get-model)
```

It works with Z3py 4.8.5 (in python3), but not with 4.8.7 (in python3.8), and again with 4.8.8 !!!  See repos/cnf.py

