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

- [x] use `:=` instead of `=` to give interpretation of a symbol
- [x] allow predicate enumerations in theory → with copy
- [ ] rename Constructor into Identifier
- [ ] use Identifier in Enumerations
- [ ] use enumerations for constructedFrom
- [ ] allow enumeration of type extension in theory/structure
    - [ ] store type enumeration to vocabulary.interpretations, using enumeration
    - [ ] copy type enumerations from vocabulary to Problem in theory/structure annotate
    - [ ] use type enumeration in Problem to expand quantifier
    - [ ] move creation of EnumSort to Problem._interpret
    - [ ] remove dead code in constructedFrom

## Binary quantifications
- [ ] update syntax of quantification over type
- [ ] rewrite Quantification.interpret using generator of cross-product → quant, aggregate
- [ ] allow several variables in quantification
- [ ] allow quantification over unary predicate 
    - [ ] type inference on the predicate
    - [ ] transform AQuantification
- [ ] allow quantification over n-ary predicates
- [ ] allow quantification over expression