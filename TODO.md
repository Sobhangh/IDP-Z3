
for the paper:
    - domain -> list box + ignore equality atoms with a constant
    - Undo
    - abstract variables: remove consequences per background theory
    - add unicity of functions ?
    - reset propagated numeric values
    - dead end in config --> undo !

functional NTH:
    - structure: true, false, arrows for functions, optional parenthesis, no expressions (brackets)
    - compute relevance in propagate
    - separate info button
    - join 2 disjuncts that differ only by the sign of one atom
    - inject known values in formulas
    - predicate symbols should show atoms (e.g. quantified constraints)
    - check syntax of int, real on client
    - garanteed order of appearance ?

    - implication semantics for definitions

other NTH (refactor)
    - organize DSL chronologically
    - distinguish between x=1 entry and x=1 atom in output structure
    - simplify Or, And with only one element
    - p(real) should be possible