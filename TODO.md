
for the paper:
    - translate numeric ranges to enum ?
    - isolate non-linear constraints over real ? https://rise4fun.com/z3/tutorial
    - abstract : remove redundant consequences per background theory

functional NTH:
    - explain should include the list of rules used
    - show (quantified) abstract atoms in English (e.g. all lenghts are positive)
    - Undo button
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
    - client should send the literal to be explained, not the atom