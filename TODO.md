
for the paper:
    - abstract: inject assumptions
    - abstract: remove consequences per background theory
    - add unicity of functions ?
    - reset propagated numeric values
    - dead end in config --> undo !

functional NTH:
    - separate info button
    - join 2 disjuncts that differ only by the sign of one atom
    - separate fixed from relevant ?
    - inject known values in formulas
    - domain should still have atoms (e.g. quantified)
    - domain -> list box + ignore equality atoms with a constant
    - check syntax of int, real on client
    - garanteed order of appearance ?

    - implication semantics for definitions

other NTH (refactor)
    - compile to DNF after edit (cache on client or server ?)
    - join abstract and relevance
    - distinguish between x=1 entry and x=1 atom in output structure
    - simplify Or, And with only one element
    - p(real) should be possible