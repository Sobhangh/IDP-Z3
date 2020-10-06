–-
title: Syntax changes
tags: 
Date: 20200923082141
–-

This document lists decisions about permanent changes of syntax compared to IDP3.  (Current limitations of IDP-Z3 are not included)

# (Proposal) Enumerations in theory block
An enumeration is valid in a theory block, e.g., `primary = {red; green; blue}`.  

# (Proposal) Predicate declared as function
A predicate is declared as a function of type`bool` , e.g., `prime(nat): bool`
Does it mean that enumerations must include the value true for every tuple ?

# (Proposal) Disambiguate constant from constructors
Constants must be followed by `()` in vocabulary: `Length():int`  (and in theory ?)

# (Proposal) Type enumeration
A type made of constructors uses the enumeration syntax, e.g., `type color = {red; blue; green}` (instead of `constructed from {red, blue, green}`). Notice the `;`

To consider: accessors for functional constructors ? e.g. `type color = rgb(red:nat, blue:nat, green:nat)`
Alternative: place the enumeration in the theory or structure

# (Proposal) Binary quantifications
A quantification has either a type or a sentence:
~~~~
! c1 c2 [color]: p(c1,c2).
! c[color(c)]: p(c).
! x y [p(x,y)]: q(x)
! c[color] q: p(c,q)
~~~~
A type applies to the variable(s) that precede it; a sentence applies to the variable(s) that precede it. Type inference uses every sentence available.

(See [[Type and Binary Quantifications]] for possible optimisation)

# (Proposal) Partial enumerations
(This works only if the types of the arguments are fully enumerated)
In a structure:
* `primary = {red; green; blue} else false` → full enumeration
* `primary = {red; green; blue}` → partial enumeration: `primary(yellow)` is uninterpreted by the structure.
* same for functions, with optional `else`

# (Proposal) Full stop in structure
Enumerations in a structure ends with a full stop (for consistency with theory)
`Convex=true. Color=red.` 

# (Proposal) define a hit policy in definitions
e.g. first applicable rule is applied.
to ensure that definitions are constructive.

# (Proposal) unit of measures
see [[Units of measure]]

# (Proposal) dates


# Already implemented
## quantification over symbols
See [[Macros]]
## if then else
`if.. then.. else..`is a valid expression.
(what about a case statement ?)
