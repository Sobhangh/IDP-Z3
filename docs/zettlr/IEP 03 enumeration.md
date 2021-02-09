# IEP 03 enumeration
## change the notation of enumeration
- [x] distinguish predicate and function enumerations
    - [x] create 2 identical enumerations: FunctionEnum, PredicateEnum
    - [x] use arrow for FunctionEnum; (), "," for tuples; fix test cases
    - [x] use (), "," for predicate enumerations
- [x] use ":=",
- [x] set .function based on syntax
- [x] docs
- [x] allow enumerations in theory
- [n/a] disable constants in structure ?
- [x] support CSV enumerations

## type enumerations in theory/structure:

Design principles:
* move all translations to Idp_to_Z3.py
* interpret() re-translate the types, functions at every call → declaration.interpret()
* translate quantified variables when translating quantifier
    * it is not possible to compare the extension of Z3's Sort.
* type enumerations are saved in block.interpretations; SymbolDeclaration in block.declarations
    * beware that multiple blocks can have the same vocabulary → detect duplication (use namedObjects ?)

Objects to recompute:
- [ ] goal, relevant atoms
- [ ] else part of an enumeration
- [ ] quantifications
- [ ] assignments of instances
- [ ] symbol instances
- [ ] Symbols

- [x] use `:=` instead of `=` to give interpretation of a symbol
- [x] allow predicate enumerations in theory → with copy
- [ ] rename Constructor into Identifier
- [x] use Identifier in Enumerations
- [x] use SymbolInterpretation for constructedFrom
- [ ] allow enumeration of type extension in theory/structure
    - [x] copy type enumerations from vocabulary to Problem in theory/structure annotate
    - [ ] use type enumeration in Problem to expand quantifier
    - [x] delay translation of quantified variables
    - [x] move translation of functions, predicates to Problem._interpret
    - [x] move translation of types to Problem._interpret
    - [ ] delay construction of `Symbols`
    - [x] move creation of assignments to Problem._interpret
    - [x] move is_complete to where it's used
    - [ ] test a change of enumeration → re-translate functions that depend on it ?
    - [ ] remove dead code in constructedFrom
- [ ] allow range enumeration in theory/structure


## Binary quantifications
- [ ] update syntax of quantification over type
- [ ] rewrite Quantification.interpret using generator of cross-product → quant, aggregate
- [ ] allow several variables in quantification
- [ ] allow quantification over unary predicate
    - [ ] type inference on the predicate
    - [ ] transform AQuantification
- [ ] allow quantification over n-ary predicates
- [ ] allow quantification over expression
