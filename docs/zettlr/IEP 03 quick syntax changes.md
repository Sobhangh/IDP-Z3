# IEP 03 Quick syntax changes
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
- [x] goal, relevant atoms (instances must be interpreted → part of Problem specs)
- [x] whole-domain constraint for definition
- [x] else part of an enumeration
- [x] constructors
- [ ] quantifications
- [x] assignments of instances + .original
- [x] symbol instances
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

problems:
- [x] lower speed of test: because of body.interpret() 
- [x]  abstract models for polygon
- [x]   environmental theories
- [x]   DMN
- [x]   all angles are 60° → no consequences !  OK if given as axiom though.  Universal are lost at the second formula is called. 

problem with speed:
* original : 8 sec but DMN, abstract fail
* add body.interpret(theory) + fix decision_table → 9+ sec, but DMN OK, (abstract fails ?)
* quad in double_def: original ok !  How ?  no def_constraints ,but instantiate_def
* So, maybe I can fix DMN + abstract without body.interpret(theory) ?
* Options: test on decl.domain in AppliedSymbol.interpret to create co_constraint
    * faster, but DMN missing conditions (collect is incomplete)
    - [ ] option: use def_constraint to cache all co_constraints ?  -> no impact on relevance

## Binary quantifications
- [x] update syntax of quantification over type
- [x] allow quantification over unary predicate
    - [x] type inference on the predicate
    - [x] transform AQuantification
- [ ] rewrite Quantification.interpret using generator of cross-product → quant, aggregate
- [ ] allow several variables in quantification
- [ ] allow quantification over n-ary predicates
- [ ] allow quantification over expression
