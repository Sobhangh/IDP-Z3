–-
title: Macros
tags: #analysis
   ID: 20200523062416
–-

aka templates

Syntax of a macro: `{ f(x) -> phi(x). }`
* notice the right arrow `->`
* a symbol is defined only once :`{f(x) -> phi1(x). f(x) -> phi2(x).}` is not allowed
* macros do no have quantifiers for variables in the head.  
* macros have no type information.  Type is verified after macro expansion.  → Symbols defined by a macro may not be declared in the vocabulary !
* symbols defined by a macro may not be part of a structure (and they are NOT shown to the user in the interactive mode of the Interactive Consultant)
* `phi(x)` can  be of any type: bool, int, real, custom type 
* `phi(x)` follows Haskell like syntax: `if-then-else`, `case` on constructors, `let`, `where`

Reserved symbols (always preceded with `__`)
* `__Symbols` : the type containing all symbols in the vocabulary (excluding reserved symbols).  Used for quantification.
* ``__arity(`p)``:  the arity of a symbol.  The backtick  (`` ` ``) should be used in front of a variable to indicate that it represents a symbol.  Its use is optional though.

Examples:    
* `{ square(x) -> x*x .}`  This is a macro for reals.
* ``{ makeSymmetric(`p) -> if __arity(`p)=2 then !x y[`p(x,y)] : `p(y,x) else __error.}``  
    * Notice the use of binary quantification ``!x y[`p(x,y)] :``  This allows type inference after expansion.
    * Notice that we do not need `VAL()` to apply `` `p``, as in ``VAL(`p)(3)``.  A variable followed by a list of arguments is always interpreted as an "application".
    * if `makeSymmetric` is applied to a symbol whose arity is not 2, the expansion will be `__error`, which will result in a syntax error (unknown reserved keyword).
* ``!`p[__Symbols]: symmetric(`p).``
* ``!`f[increasing(`f)]: !x[real] y[real]: x<y => `f(x) < `f(y).``
    * here, ``increasing`` is a predicate defined in the vocabulary as ``increasing(__Symbols)``.  It must be overapproximatable, so that the binary quantification can be expanded.

Implementation:
1. detect (binary) quantification over symbols, and expand them
2. expand macros
3. type verification
4. (binary) quantifier expansion 

To be further investigated: 
* can we always expand quantifiers over symbols before quantifiers over variables ?  Or do we need some kind of fixed point computation ?