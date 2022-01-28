.. index:: structure

.. _structure:

Structure
---------
.. code::

    structure S:V {
        // here comes the structure named S, for vocabulary named V
    }

A *structure* specifies the interpretation of some type_, predicate_\ s and function_\ s.
If the names are omitted, the structure is named S, for vocabulary V.

A structure is a set of symbol interpretations of the form ``<symbol> := <interpretation>.``,
e.g., ``P := {1..9}``, where the interpretation can be:

for nullary predicates (propositions)
    ``true`` or ``false``

for non-numeric types and unary predicates:
    a set of rigid terms (numbers, dates, identifiers, or constructors applied to rigid terms),
    e.g., ``{red, blue, green}``.

for numeric types and unary predicates:
    a set of numeric literals and ranges,
    e.g., ``{0,1,2}``, ``{0..255}`` or ``{0..9, 90..99}``

for date types and unary predicates:
    a set of date literals and ranges,
    e.g., ``{#2021-01-01, #2022-01-01}`` or ``{#2021-01-01 .. #2022-01-01}``

for types:
    a set of n-ary constructors, preceded by ``constructed from``,
    e.g., ``constructed from {Red, Blue, Green, RGB(R: Byte, G: Byte, B: Byte)}``
    (see more details in type_\ s)

for n-ary predicates:
    a set of tuples of rigid terms, e.g., ``{(a,b), (a,c)}``.

for nullary functions:
    a rigid term, e.g. ``5`` or ``#2021-01-01``, or ``red`` or ``rgb(0,0,0)``

for n-ary functions:
    a set of tuples and their associated values,
    e.g., ``{ (1,2)->3, (4, 5)->6 }``

Additional  notes:

* the interpretation of a predicate is specified by the set of the tuples that make the predicate true; any other tuple makes it false.

* the interpretation of a function may be followed by ``else <default>``, where ``<default>`` is a default value (a rigid term), i.e., a value for the non-enumerated tuples, if any.

* parenthesis around a tuple can be omitted when the arity is 1, e.g., ``{1-2, 3->4}``

* the interpretation of a predicate may be specified using the CSV format, with one tuple per line, e.g., :

.. code::

    P := {
    1 2
    3 4
    5 6
    }

* The interpretation of ``goal_string`` is used to compute relevance relative to goals (see the ``determine_relevance`` method in the :ref:`Theory class <Theory_class>`).

* The tuples of an interpretation can be given in any order.
