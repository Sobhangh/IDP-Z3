.. _type_checking:

Type checking
-------------

IDP-Z3 performs a static type check of the statements
in each theory and structure block.
It determines the type of each sub-expression,
and checks that this type is expected where the sub-expression occurs.

Declaring a subset of integers can not be done as follows.

.. code::

    vocabulary V {
        type row
        c: -> row
    }
    theory { c() < 3. }
    structure S1:V { row := {1..5} }
    structure S2:V { row := {A, B, C} }

IDP-Z3 does not accept the theory because it cannot infer that ``c()`` is a number in ``c() < 3.``.
Indeed, it depends on whether S1 or S2 is used.

If ``row`` is intended to be a set of integers that can be used in arithmetic expressions,
it should be declared in the vocabulary as a subset of ``Int``:

.. code::

    row: Int -> Bool

At some point, we may decide that the elements of ``type row := {1..5}`` are identifiers that may not participate in arithmetic expressions.