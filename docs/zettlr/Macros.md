–-
title: Macros
tags: #analysis
Date: 20200523062416
–-

## Part 1: `` `Symbols`` type
- [x] the `` `Symbols`` type is the set of symbols defined in the vocabulary.  
- [x] The constructors for the `` `Symbols`` are the symbol names preceded by a backtick (`` ` ``), e.g. `` `edge``
- [x] the `` `Symbols`` type can appear in function and predicate declaration in the vocabulary section, e.g. `` `symmetric(`Symbols)``is a predicate declaration
- [x] predicates and functions over `` `Symbols`` are part of structures, like any other symbols
- [x] it's possible to quantify over `` `Symbols``, e.g. ``?`p[`Symbols]: symmetric(`p).``
    - [x] The backtick  (`` ` ``) should be used in front of a variable to indicate that it represents a symbol.  Its use is optional though.
- [x] a variable of type `` `Symbols`` can be applied to arguments, e.g. ``?`p[`Symbols]: symmetric(`p) => (!x y : `p(x,y) => `p(y,x))``
    - [x]  if the arity is wrong, a valid instance of `p`  is given instead (to avoid error when the instance is irrelevant) (should benefit from partial functions when available)
    - [x] notice that this requires [[Type inference]] AFTER expansion of the first quantifier
    - [x] make types optional in quantification
    - [ ] Alternatively, this could be written using [[Type and Binary Quantifications]] (when available).
- [x] it's possible to quantify over `` `Symbols`` in head of definitions
- [ ] add `` `arity`` predicate

Quantification over symbols in constraints:
- [ ] make it work with symmetric enumeration in theory
    - [x] instantiate an implication should first instantiate the implicant, then, if not false, the consequent.  If implicant is false, value is True, sub_exprs = ….
    - [ ] instantiate AppliedSymbol with Symbol argument should interpret applied symbol, if possible. Test: `Start:node`
- [ ] make it work with symmetric enumeration in structure
    - [ ] Problem should contain merged vocabularies (instead of structures) + detect conflicts
    - [ ] Problem should use vocabularies, not structures
    - [ ] option to give type expansion in structure; expand_quantifier should be done 1) tentatively in annotate; 2) finally in interpret, given all the structures
    - [ ] Symbols.range should be regenerated before interpret and quantification expansion

Questions:
* use `` `edge `` or `` `edge' `` ? 
    * closing tick will later allow to talk about expressions, e.g. to annotate an expression with a reading
    * but we could use other delimiters, such as `[]`
    * so, `` `f(x) `` is the same as `` f(x) ``, but  `` `p `` is not the same as `` `p() ``!
* use backticks in display theory ?
    * simpler to implement, and consistent, but there would be no ambiguity in `relevant(p)`

## Part 2: constructive definitions
* accept only constructive definitions ?
* a definition can be annotated as "constructive"
* in that case, the grounder can just instantiate the definition as needed by occurrences in other constraints/definitions.  He does not have to instantiate it for all possible values of the arguments.
* for example, `{ constructive: !x[real]: square(x) = x*x. }` 
* other than annotation, constructive definitions follow the usual syntax of definitions

## Part 3: `__Rules` type
* the `__Rules` type is the set of Rules defined in the vocabulary.  
* this could be used to implement special cases of a rule (e.g. penguins are birds that don't fly)

Example
- Article 1: birds fly.  
- Article 2: As an exception to Article 1, Penguins do not fly.  

```
theory {  
     {  [Art1] Fly(x) <- Bird(x). }  
     (...)  
     [Art2] Exception(`Art1,  
             {~Fly(x) <- Penguin(x). }  
         ).
}
```
The idea could be generalized with \_\_Definition, \_\_Constraint and __Expression types.

## Part 3: other
* other improvements can be done independently/later, such as binary quantification, partial functions, …

