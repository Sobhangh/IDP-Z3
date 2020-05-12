–-
title: TODO
tags: 
   ID: TODO
–-
- [ ] Aanbesteding demo
- [ ] [[AWS hosting]] [[20200401113342]] 

- [ ] flatten nested applicaton f(f(x))
- [ ] Explanations: inject values in message
- [ ] [[consequence in dropdown]] [[20200408162211]] 
- [ ] Float ranges
- [ ] avoid duplication of equalities in user interface (enumerated types)
- [ ] min, max aggregates

- [ ] Support for constructor functions (p.6 of the IDP3 manual)
    - grammar
    - generate list of constructors
    - transform occurrences in source code, using If() if variables
- [ ] Lexicographic, Pareto and conditional optimization
- [ ] Support for dates
- [ ] issues on GitLab

#### Syntax changes:
- [ ] move enumerations in vocabulary to the theory block
- [ ] move enumerations in structure to the theory block
- [ ] 'Expand all' or list (instead of View expanded/normal)

#### Research topics / may take a while:
- [ ] Support for partial functions
- [ ] Support for partial interpretations (ct, cf, u) (p.17 of the IDP3 manual)
- [ ] Support for non-linear equations [[20200328122541]]
- [ ] Parse English [[20200327095115]] 
- [ ] use pySMT [[20200328102421]] 


#### Of dubious benefit / may never be done:
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
- [ ] reduce number of substitution
    - [ ] Expr.questions for each constraint → do not substitute if no matching question
- [ ] rewrite in Nim !
- [ ] use sets to avoid duplicates (e.g. constraints)
- [ ] use weakref to share justifications
- [ ] subtences() → exp is_in expr
- [ ] avoid mergeDicts.  Use accumulator instead
- [ ] use `__slots__`
- [ ] cython, pypy
- [ ] #Perf

#### other NTH (refactoring)
- [ ] reorganize project folders
- [ ] get rid of brackets ?  Need to keep multiple annotations
- [ ] remove Assignment.__hash__, .__eq__
- [ ] merge Case.assignments and Case.GUILines to be like Structure
- [ ] remove reifier, Solver.py --> expr.reified(solver)
- [ ] simplify the generation of Structure_

- [ ] use EXIST, … instead of AQuantifier.make(), for readability
- [ ] move consequences into case.simplified ?
- [ ] sort the operands of equality
- [ ] AppliedSymbol is_subtence only if no Fresh_Variable !
- [ ] Expr.sentence -> Expr.ranking ?
- [ ] distinguish between x=1 entry and x=1 atom in output structure
- [ ] p(real) should be possible
- [ ] #refactoring

#general