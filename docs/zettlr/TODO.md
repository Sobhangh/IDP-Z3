–-
title: TODO
tags: 
Date: TODO
–-

- [ ] Explanations: inject values in message
- [ ] Float ranges
- [ ] avoid duplication of equalities in user interface (enumerated types)
- [ ] min, max aggregates

- [ ] Support for [[Functional constructors]] (p.6 of the IDP3 manual)
- [ ] Lexicographic, Pareto and conditional optimization
- [ ] Support for dates
- [ ] issues on GitLab

#### Syntax changes:
- [ ] structures become data theories consisting of data expressions; these expression can occur also inside theories.
- [ ] standard extensible way of typing as in type theory : p(t1,t2) would be p::(t1,t2):bool
- [ ] distinguish identifiers from constants: an identifier c of type t could be typed c:t while a constant c of type t could be typed c():t
- [ ] [[Type and Binary Quantifications]]
- [ ] require definitions to be constructive
- [ ] move enumerations in vocabulary to the theory block

#### Research topics / may take a while:
- [ ] use list of simplifications steps for explain
- [ ] Support for partial functions
- [ ] Support for partial interpretations (ct, cf, u) (p.17 of the IDP3 manual)
- [ ] Support for [[Non linear equations]]
- [ ] [[use pySMT]] 


#### Of dubious benefit / may never be done:
- [ ] flatten nested applicaton f(f(x))
- [ ] Type inference (p. 14 of the IDP3 manual)
- [ ] Support for type hierarchy
- [ ] Support for namespaces
- [ ] Support for strings
- [ ] Support for recursive definitions
- [ ] Support for multiple vocabulary / theories
- [ ] Support for natural (positive integers)
- [ ] Handling of division by 0 may differ (to be tested)
- [ ] Support order on domain elements (p. 8..9 )
- [ ] Support for LTC vocabulary
- [ ] Support for “quantified quantifiers”, and binary quantifications (p. 11 of the IDP3 manual)
- [ ] Support for aggregates on list of terms or formulas (p. 13 of the IDP3 manual)
- [ ] Support all syntactical forms of structures.
- [ ] Support for factlist (p. 17 of the IDP3 manual)
- [ ] Support of lua
- [ ] Abstract models:
        - show goal to the right of abstract models
        - join 2 disjuncts that differ only by the sign of one atom

#### Performance
- [ ] incremental propagate: use dependency graph (+ block) to propagate selectively
- [ ] full propagate: should have only one expansion per unknown subtence
- [ ] relevance-based optimal propagate (do not propagate irrelevant subtences)
- [ ] do not translate Simplified in propagation: using original theory instead
- [ ] use graph library instead of simplify for relevance
- [ ] reify quantifications and use Z3's simplify (and ignore irrelevant reification) (but what about dReal ?)

- [ ] merge case.co_constraints and case.definitions (many overlaps)
- [ ] use sets to avoid duplicates (e.g. constraints)
- [ ] use weakref to share co_constraints
- [ ] avoid mergeDicts.  Use accumulator instead
- [ ] rewrite in [[Nim]]
- [ ] #Perf

#### other NTH (refactoring)
- [ ] use [macropy](https://macropy3.readthedocs.io/en/latest/): smartAsserts, pattern matching
- [ ] merge Case.assignments and Case.GUILines to be like Structure ([[Questions]] )
- [ ] remove reifier, Solver.py --> expr.reified(solver)
- [ ] simplify the generation of Structure_

- [ ] use EXIST, … instead of AQuantifier.make(), for readability
- [ ] move consequences into case.simplified ?
- [ ] sort the operands of equality
- [ ] Expr.sentence -> Expr.ranking ?
- [ ] distinguish between x=1 entry and x=1 atom in output structure
- [ ] p(real) should be possible
- [ ] #refactoring

#general