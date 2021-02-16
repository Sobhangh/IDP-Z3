.. index:: IDP3

Differences with IDP3
---------------------

Here are the main differences with IDP3, listed for migration purposes:

min/max aggregates
    IDP-Z3 does not support these aggregates (yet).
    See `IEP 05 <https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-05-Min-and-Max-aggregate>`_

Inductive definitions
    IDP-Z3 does not support inductive definitions.

Infinite domains
    IDP-Z3 supports infinite domains: ``Int, Real``.
    However, quantifications over infinite domains is discouraged.

if .. then .. else ..
    IDP-Z3 supports `if .. then .. else ..` terms and sentences.

LTC
    IDP-Z3 does not support LTC vocabularies.

Namespaces
    IDP-Z3 does not support namespaces.

N-ary constructors
    IDP-Z3 does not support n-ary constructors, e.g., ``RGB(Int, Int, Int)``.
    See `IEP 06 <https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-06-n-ary-constructors>`_

Partial functions
    IDP-Z3 does not support partial functions.
    The handling of division by 0 may differ.
    See `IEP 07 <https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-07-Division-by-0>`_

Programming API
    IDP3 procedures are written in Lua, IDP-Z3 procedures are written in Python-like language.

Qualified quantifications
    IDP-Z3 does not support qualified quantifications, e.g. ``!2 x[color]: p(x).``. (p. 11 of the IDP3 manual).

Structure
    IDP-Z3 does not support ``u`` uncertain interpretations (p.17 of IDP3 manual).
    Function enumerations must have an ``else`` part.
    (see also `IEP 04 <https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-04-Incomplete-enumerations>`_)

Type
    Type enumerations must be done in the vocabulary block (not in the structure block).
    IDP-Z3 does not support type hierarchies.

To improve performance, do not quantify over the value of a function.
Use ``p(f(x))`` instead of ``?y: f(x)=y & p(y)``.