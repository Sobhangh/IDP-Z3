.. _type_inference:

Type inference in quantifications
---------------------------------

It is often convenient to omit the type of variables in quantifications and aggregates, e.g.,

.. code::

    ! p: 0 =< age(p).

It is also customary to use evocative names for variables, e.g.,
to use ``p`` for a variable ranging over persons,
or ``col`` for a variable ranging over a set of columns.
By extension, one would also consider ``p1, p2`` as variables ranging over persons.

Therefore, we recommend knowledge engineers to declare variables in the vocabulary, e.g.,

.. code::

    var p in Person
    var col in Column

This allows IDP-Z3 to properly infer the type of ``p`` in our example above.
IDP-Z3 also uses the variable declaration to infer the type of variables ``p1``, ``p2``, ...,
e.g., in ``? p1, p2: married(p1, p2).``
(the variable declaration in the vocabulary cannot end with a number)

Note that the variable declaration is only used when the type is not given in the quantification.
In ``! p in Column: ...``, ``p`` ranges over the set of Columns,
even if variable ``p`` is declared differently in the vocabulary.

Note also that ``! p, c in Col: ..`` raises an error because ``p`` is ambiguous:
is it a Person or a Col ?