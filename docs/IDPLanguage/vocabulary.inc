.. _vocabulary:
.. index:: vocabulary

Vocabulary
----------

.. code::

    vocabulary V {
        // here comes the vocabulary named V
    }

The *vocabulary* block specifies the types, predicates, functions and constants used to describe the problem domain.
If the name is omitted, the vocabulary is named V.

Each declaration goes on a new line (or are space separated).
Symbols begins with an alphabetic character or ``_``, followed by alphanumeric characters or ``_``.
Symbols can also be string literals delimited by ``'``, e.g., ``'blue planet'``.

.. _type:
.. _constructor:
.. _symbol:
.. index:: type, constructor, symbol

Types
+++++

IDP-Z3 has the following built-in types:  ``𝔹``, ``ℤ``, ``ℝ``, ``Symbol``.
The equivalent ASCII symbols are ``Bool``, ``Int``, and ``Real``.

Custom types can be defined by specifying a range of numeric literals, or a list of constructors (of arity 0).
Their name should be capitalized, by convention.

.. code::

    type Side := {1..4}
    type Color := {red, blue, green}

The type ``Symbol`` has one constructor for each symbol (i.e., function, predicate or constant) declared in the vocabulary.
The constructors are the names of the symbol, prefixed with `````


.. _function:
.. index:: function

Functions
+++++++++

The functions with name ``MyFunc1``, ``MyFunc2``, input types ``T1``, ``T2``, ``T3`` and output type ``T``, are declared by:

.. code::

    myFunc1, myFunc2 : T1 ⨯ T2 ⨯ T3 → T

Their name should not start with a capital letter, by convention.
The ASCII equivalent of ``⨯`` is ``*``, and of ``→`` is ``->``.

IDP-Z3 does not support partial functions.

.. _predicate:
.. index:: predicate

Predicates
++++++++++

The predicates with name ``myPred1``, ``myPred2`` and argument types ``T1``, ``T2``, ``T3`` are declared by:

.. code::

    myPred1, myPred2 : T1 ⨯ T2 ⨯ T3 → 𝔹

Their name should not start with a capital letter, by convention.
The ASCII equivalent of ``→`` is ``->``, and of ``𝔹`` is ``Bool``.

.. _constant:
.. index:: constant, proposition

Propositions and Constants
++++++++++++++++++++++++++

A proposition is a predicate of arity 0; a constant is a function of arity 0.

.. code::

    MyProposition : () → 𝔹
    MyConstant: () → Int


.. _extern:
.. index:: include vocabulary

Include another vocabulary
+++++++++++++++++++++++++++

A vocabulary W may include a previously defined vocabulary V:

.. code::

    vocabulary W {
        extern vocabulary V
        // here comes the vocabulary named V
    }

