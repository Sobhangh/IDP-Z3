–-
title: Macros
tags: #analysis
   ID: 20200523062416
–-

## Part 1: `__Symbols` type
* the `__Symbols` type is the set of symbols defined in the vocabulary.  
* The constructors for the `__Symbols` are the symbol names preceded by a backtick (`` ` ``), e.g. `` `edge``
* the `__Symbols` type can appear in function and predicate declaration in the vocabulary section, e.g. `symmetric(__Symbols)`is a predicate declaration
* predicates and functions over `__Symbols` are part of structures, like any other symbols
* it's possible to quantify over `__Symbols`, e.g. ``?`p[__Symbols]: symmetric(`p).``
    * The backtick  (`` ` ``) should be used in front of a variable to indicate that it represents a symbol.  Its use is optional though.
* a variable of type `__Symbols` can be applied to arguments, e.g. ``?`p[__Symbols]: symmetric(`p) => (!x y : `p(x,y) => `p(y,x))``
    * notice that this requires type inference AFTER expansion of the first quantifier.  
    * if the arity is wrong, an error is raised by the grounder
    * Alternatively, this could be written using binary quantification (when available).

## Part 2: constructive definitions
* accept only constructive definitions ?
* a definition can be annotated as "constructive"
* in that case, the grounder can just instantiate the definition as needed by occurrences in other constraints/definitions.  He does not have to instantiate it for all possible values of the arguments.
* for example, `{ constructive: !x[real]: square(x) = x*x. }` 
* other than annotation, constructive definitions follow the usual syntax of definitions

## Part 3: other
* other improvements can be done independently/later, such as binary quantification, partial functions, …

