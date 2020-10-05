–-
title: Type inference
tags: #analysis
Date: 20200528070729
–-

Goal:
X verify types in formula (and raise error) → done by Z3
- [x] allow quantification without types
- [ ] support [[Macros]]
- [ ] predicate overloading
    - [ ] allow predicates with same name, but different **number** of arguments
    - [ ] allow types and functions/predicates with the same name
    - [ ] allow predicates with same name, but different **type** of arguments
- [ ] optimisation: see [[Type and Binary Quantifications]]

Options:
* use top-down and bottom-up inferences
    * top-down when sort of quantified formula is known → allow resolution of ambiguous predicate
    * may require the user to add type to some quantification, to resolve ambiguity
* use SAT solver → smarter, but more complex and not fool-proof → not worth it

Todo:
X fresh_vars : use Dict[name, type?] , not Set() → instead store type in Fresh_Var
X verify types in formula and raise error
- [x] type inference in quantification
    - [x] expand outer quantifier first
    - [ ] int/real type inference from arithmetic operations
- [x] type inference in aggregates
- [ ] add arity to predicate name, to allow overloading by number of arguments
- [ ] separate symbol_decls in 2 dictionaries, one for type, the other for function/predicates
- [ ] overloading of function/predicates with different types
    - [ ] need unique names for Z3 ! → correspondence table
