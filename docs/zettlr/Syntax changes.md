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

# (Proposal) Disambiguate constant from constructors
Constants must be followed by `()` in vocabulary: `Length():int`  (and in theory ?)

# (Proposal) Type enumeration
A type made of constructors uses the enumeration syntax, e.g., `type color = {red; blue; green}` (instead of `constructed from {red, blue, green}`). Notice the `;`

# (Proposal) Binary quantifications
A quantification has either a type or a sentence:
`! c[color]: p(c).` 
`! c[color(c)]: p(c)`
`! x y [p(x,y)]: q(x).`
(See [[Type and Binary Quantifications]] for possible optimisation)

# (Proposal) Partial enumerations
In a structure:
* `primary = {red; green; blue} else false` → full enumeration
* `primary = {red; green; blue}` → partial enumeration: `primary(yellow)` is uninterpreted by the structure.
* same for functions, with optional `else`

# (Proposal) Constants in structure
The statement to give an interpretation to a predicate or function constant ends with a comma, i.e., `Convex=true. Color=red.` 

# (Proposal) if then else
`if.. then.. else..`is a valid expression.
(what about a case statement ?)

