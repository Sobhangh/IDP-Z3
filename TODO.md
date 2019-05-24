
for the paper:
    - simplify abstract models
        - extract fixed atoms
        - remove consequences in disjunct
        - join 2 disjuncts that differ only by the sign of one atom

functional NTH:
    - send on enter only
    - convert fractions, update formulas
    - interval predicate
    - domain -> list box + ignore equality atoms with a constant
    - check syntax of int, real
    - garanteed order of appearance ?

    - inject found value into atom and simplify
    - implication semantics for definitions
    - simplify intervals
    - keep quantified expressions in full

other NTH (refactor)
    - join propagate and relevance
    - distinguish between x=1 entry and x=1 atom in output structure
    - simplify Or, And with only one element
    - why multiple unnecessary calls to idp ?
    - p(real) should be possible