–-
title: Functional constructors
tags: #analysis 
Date: 20200525094548
–-

Example:
~~~~
type nat constructed from {0..255}
type color constructed from {rgb(nat, nat, nat)}
~~~~
the constructors for color are `rgb(0,0,0), rgb(0,0,1), ...` (256x256x256 of them !)

Caution:
* a type may have several constructors, with a mix of 0-arity and n-arity constructors !
* in an IDP theory, the argument of a constructor may be an expression !

To do:
- [ ] preliminary: refactor `Parse.py\ConstructedTypeDeclaration` using Z3 Datatypes instead of EnumSort (without functional constructors yet)
    - see [Z3 Reference](https://ericpony.github.io/z3py-tutorial/advanced-examples.htm) - Datatypes section
    - run `python3 test.py` to detect any regression
- [ ] `Idp.tx`adapt grammar to allow functional constructors
    - [ ] add new arguments to `Expression\Constructor`
- [ ] `Parse.py\ConstructedTypeDeclaration`
    - [ ] update init() to refine .translated with the Datatype in Z3 (use "arg1", "arg2" for the accessors, prefixed with "__")
        - we may need [[Syntax changes]] to allow user to define accessors
    - [ ] make sure voc.symbol_decls contains each bare functional constructor (e.g., `rgb`) 
    - [ ] update voc.symbol_decls and self.range with expanded list of constructors with name `rgb(0,0,0)`, …
            - [ ] use AppliedSymbol.make() to create each instance in IDP
- [ ] ~~`Idp_to_Z3`: adapt translation of AppliedSymbol to Z3, for the constructor case~~
- [ ] `Expression` AppliedSymbol.annotate() should detect functional constructors (just as Variable does)
    - [ ] simply flag the AppliedSymbol accordingly
- [ ] AppliedSymbol/collect: do not collect if a constructor
- [ ] write test cases and run `python3 test.py` to see if any other impact
- [ ] verify in Interactive Consultant
    - [ ] display of functional constructors
    - [ ] entry of functional constructors (in list box)
- [ ] update documentation in sphinx
