Type and Binary Quantifications
=
20200330121959 

See [trail of e-mails](https://docs.google.com/document/d/1BDB8bp1zC6XUMshnoriQLCOQ2okF4vxZWVDOeqbFeXM/edit)

Principles:
* A _type_ is a category of objects.
* A _typed vocabulary_ describes which category of objects is expected as arguments or results of functions/predicates.  _Type inferences_ can be used to raise _type errors_ when a symbol used in a formula has a wrong type.
* A type always has an _associated predicate_, that tells which object is in that category
* The predicate associated to a type is a parameter of the theory. It may, but does not have to, be constrained by formulas, or defined by enumeration or by construction (i.e. with a definition).
* The enumeration of a type consists of the list of _constructors_, including _functional constructors_.
* A type (or its predicate) is _computable_ if it is defined by
    * a recursion-free enumeration, in which functional constructors are based on other computable types, 
    * or a recursion-free definition based on other computable types
* A formula is _over-approximatable_ if it uses computable types only.  This over-approximation is computed by an algebra.
* A _Binary quantified formula_ is a formula of the form $\forall x [\phi(x)]: \psi(x).$  or $\exists x [\phi(x)]: \psi(x).$, where $\phi(x)$ is over-approximatable

#analysis #research