–-
title: Re-use co-constraints
tags: #perf
   ID: 20201023155413
–-

Goal: reduce duplication of effort in interpret()

Todo:
- [ ] theory.co_constraints is a dict : code → expression
- [ ] Expression.co-constraint contains the key to theory.co_constraints
- [ ] expression.interpret(theory): if nodes needs a co_constraints, look it up in theory.co_constraints, and add it if necessary
- [ ] collect co_constraints: traverse the expression, looking up in theory.co_constraints if present
