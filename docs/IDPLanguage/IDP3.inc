.. index:: IDP3

Differences with IDP3
---------------------

Here are the main differences with IDP3 (the previous version of IDP-Z3), listed for migration purposes:

Infinite domains
    IDP-Z3 supports infinite domains: ``Int, Real``.
    However, quantifications over infinite domains is discouraged.

Type
    IDP-Z3 supports type hierarchies differently from IDP3:
    subtypes are now represented by unary predicates;
    unary predicates can be used wherever types can be used, i.e., in type signatures and in quantifiers.

LTC
    IDP-Z3 does not support LTC vocabularies.

Namespaces
    IDP-Z3 does not support namespaces.

Partial functions
    In IDP-Z3, a function must be total over a cross-product of (sub-)types.
    The handling of division by 0 may differ.
    See `IEP 07 <https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-07-Division-by-0>`_

Syntax changes
    The syntax of quantifications and aggregates has slightly change.
    IDP-Z3 does not support qualified quantifications, e.g. ``!2 x[color]: p(x).``. (p. 11 of the IDP3 manual).
    Such statements can be implemented in IDP-Z3 using cardinality constraints instead.

if .. then .. else ..
    IDP-Z3 supports `if .. then .. else ..` terms and sentences.

Structure
    IDP-Z3 supports partial interpretations of functions using the `:>=` sign.
    (It currently does not support partial interpretations of predicates)

Procedure blocks
    IDP-Z3 only recognizes the `main()` block, written in Python (instead of in Lua).

To improve performance, do not quantify over the value of a function.
Use ``p(f(x))`` instead of ``?y: f(x)=y & p(y)``.
