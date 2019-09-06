
priority:
    - compact layout (More... --> pop-up)
    - relevance
    - environmental variables
    - goal --> to the right of abstract models
    - join 2 disjuncts that differ only by the sign of one atom
    - optimal propagation -> surface and non-linear


    - translate numeric ranges to enum ?
    - isolate non-linear constraints over real ? https://rise4fun.com/z3/tutorial
    - Show 1 model: numeric values should not have "explain"

functional NTH:
    - improve metaJSON() to allow hiding of some variables, optimisation on some variables only
    - how to hide some of the atoms
    - Undo button
    - structure syntax: true, false, arrows for functions, optional parenthesis, no expressions (brackets)
    - compute relevance in propagate
    - separate info button
    - inject known values in formulas
    - predicate symbols should show atoms (e.g. quantified constraints)
    - dates
    - check syntax of int, real on client
    - garanteed order of appearance ?

    - implication semantics for definitions

other NTH (refactor)
    - organize DSL chronologically
    - distinguish between x=1 entry and x=1 atom in output structure
    - simplify Or, And with only one element
    - p(real) should be possible
    - client should send the literal to be explained, not the atom

GUI enhancements:
    - show offended rules when unsatisfiable

Merge with Explain branch:
    - use slider for numeric values
    - show valid range of numeric values
    - scroll bar for list of values
    - categories to group symbols
    - nested symbols
    - option to disable some rules (full workflow)
    - compare consequences of 2 different choices

Bart:
    - add annotation in vocabulary
    - confusing when list of atoms does not match list in drop box