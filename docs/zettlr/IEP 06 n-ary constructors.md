–-
title: IEP 06 n-ary constructors
tags: #IEP
   ID: 20201119092757
–-

- [ ] preliminary: refactor `Parse.py\ConstructedTypeDeclaration` using Z3 Datatypes instead of EnumSort (without n-ary constructors yet)
    * see [Z3 Reference](https://ericpony.github.io/z3py-tutorial/advanced-examples.htm) \- Datatypes section
    * run `python3 test.py` to detect any regression
* [ ]  `Idp.tx`adapt grammar to allow n-ary constructors
    * [ ]  add new arguments to `Expression\Constructor`
* [ ] `Parse.py\ConstructedTypeDeclaration`
    * [ ]  update init() to refine .translated with the Datatype in Z3
    * [ ]  make sure voc.symbol_decls contains each bare functional constructor (e.g., `rgb`)
    * [ ]  update voc.symbol_decls and self.range with expanded list of constructors with name `rgb(0,0,0)`,... (use AppliedSymbol.make() to create each instance in IDP)
* [ ] `Expression` AppliedSymbol.annotate() should detect n-ary constructors (just as Variable does)
    * [ ]  simply flag the AppliedSymbol accordingly
* [ ]  AppliedSymbol/collect: do not collect if a constructor
* [ ]  write test cases and run `python3 test.py` to see if any other impact
* [ ]  verify in Interactive Consultant
    * [ ]  display of n-ary constructors
    * [ ]  entry of n-ary constructors (in list box)
* [ ]  update documentation in sphinx