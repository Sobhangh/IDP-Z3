.. _type_checking:

Type checks
-----------

IDP-Z3 performs a static type check of the statements
in each theory and structure block.
It determines the type of each sub-expression,
and checks that this type is expected where the sub-expression occurs.


If ``row`` is intended to be a set of integers that can be used in arithmetic expressions,
it should be declared in the vocabulary as a subset of ``Int``:

.. code::

    row: Int -> Bool

Declaring a subset of integers can not be done as follows.

.. code::

    vocabulary V {
        type row
        c: -> row
    }
    theory { c() < 3. }
    structure S1:V { row := {1..5}. }
    structure S2:V { row := {A, B, C}. }

IDP-Z3 does not accept the theory because it cannot infer that ``c()`` is a number in ``c() < 3.``.
Indeed, it depends on whether S1 or S2 is used.

At some point, we may decide that the elements of ``type row := {1..5}`` are identifiers that may not participate in arithmetic expressions.

Domain checks
-------------

In addition to type checks, IDP-Z3 performs a static domain check of the statements in each theory block.
It verifies that the arguments of a term constructed with a partial function
are within the domain of definitions of the function in the context of the term.
The domain of definition of a function is declared in the vocabulary.

A domain error can be fixed by adding a "guard".
Guards are suggested by the editor in the online web IDE.
For example, the first sentence below does not pass the domain check because of the division by 0,
but the second one passes it thanks to the guard ``x ~= 0``.

.. code::

    ? x,y in Int: y/x < 0.
    ? x,y in Int: x ~= 0 & y/x < 0.

