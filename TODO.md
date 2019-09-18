Priority:
    - settings: first underscore = hidden symbol (PC)
    - View Normal (with popup) / Expanded (PC)
    - values:use slider for numeric values (when type is a range) (Bram)
    - values:show valid range of numeric values ?? beware of inequalities and infinite (Bram)
    - compare consequences of 2 different choices (Bram)

    - non-linear
    - settings: minimizable ? describe goal using new syntax ? (PC)
    - error management (for idp code) (PC)
    - show offended rules when unsatisfiable (re-use Explain API) (Bram)
    - option to disable some rules (full workflow)(Bram)
    - settings: group symbols into categories (e.g. using markdown annotations ?)
    - settings: annotations in vocabulary (longinfo)
    - values:how to say how the list box should be organised ?  Annotations ? based on size ?

    - relevance
    - settings: give name to a vocabulary


priority:
    - compact layout (More... --> pop-up)
    - relevance (definitions)
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
    - distinguish between x=1 entry and x=1 atom in output structure
    - simplify Or, And with only one element
    - p(real) should be possible
    - client should send the literal to be explained, not the atom



Bart:
    - add annotation in vocabulary
    - confusing when list of atoms does not match list in drop box