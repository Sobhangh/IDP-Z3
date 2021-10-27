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
Symbols begins with a word character excluding digits, followed by word characters.
Word characters include alphabetic characters, digits, ``_``, and unicode characters that can occur in words.
Symbols can also be string literals delimited by ``'``, e.g., ``'blue planet'``.

.. _type:
.. _constructor:
.. _symbol:
.. index:: type, constructor, symbol

Types
+++++

IDP-Z3 supports built-in and custom types.

The built-in types are:  ``𝔹``, ``ℤ``, ``ℝ``, ``Date``, and ``Concept``.
The equivalent ASCII symbols are ``Bool``, ``Int``, and ``Real``.

Boolean literals are ``true`` and ``false``.
Number literals follow Python's conventions.
Date literals follow ISO 8601 conventions, prefixed with ``#`` (``#yyyy-mm-dd``).
``#TODAY`` is also a Date literal.

The type ``Concept`` has one constructor for each symbol (i.e., function, predicate or constant) declared in the vocabulary.
The constructors are the names of the symbol, prefixed with `````

Custom types are declared using the keyword ``type``, e.g., ``type color``.
Their name should be singular and capitalized, by convention.

Their extension can be defined in a structure_, or directly in the vocabulary, by specifying:

* a list of (ranges of) numeric literals, e.g., ``type someNumbers := {0,1,2}`` or ``type byte := {0..255}``

* a list of (ranges of) dates, e.g., ``type dates := {#2021-01-01, #2022-01-01}`` or ``type dates := {#2021-01-01 .. #2022-01-01}``

* a list of nullary constructors, e.g., ``type Color := {Red, Blue, Green}``

* a list of n-ary constructors; in that case, the enumeration must be preceded by ``constructed from``, e.g., ``type Color2 := constructed from {Red, Blue, Green, RGB(R: Byte, G: Byte, B: Byte)}``

In the above example, the constructors of ```Color`` are : ``Red``, ``Blue``, ``Green``.

The constructors of ```Color2`` are : ``Red``, ``Blue``, ``Green`` and ``RGB``.
Each constructor have an associated function (e.g., ``is_Red``, or ``is_RGB``) to test if a Color2 term was created with that constructor.
The ``RGB`` constructor takes 3 arguments of type ``Byte``.
``R``, ``G`` and ``B`` are accessor functions: when given a Color2 term constructed with RGB, they return the associated Byte.
(When given a Color2 not constructed with RGB, they may raise an error)

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

.. _built-in functions:

Built-in functions
++++++++++++++++++

The following functions are built-in:

* ``abs: Int → Int`` (or ``abs: Float → Float``) yields the absolute value of an integer (or float) expression;
* ``arity: Concept → Concept`` yields the arity of a symbol;
* ``input_domain : Concept ⨯ ℤ → Concept`` yields the n-th input-domain of a symbol;
* ``output_domain: Concept → Concept`` yields the output domain of a symbol.

.. _predicate:
.. index:: predicate

Predicates
++++++++++

The predicates with name ``myPred1``, ``myPred2`` and argument types ``T1``, ``T2``, ``T3`` are declared by:

.. code::

    myPred1, myPred2 : T1 ⨯ T2 ⨯ T3 → 𝔹

Their name should not start with a capital letter, by convention.
The ASCII equivalent of ``→`` is ``->``, and of ``𝔹`` is ``Bool``.

There is a built-in predicate ``T: T → 𝔹`` for each type T (``T(x)`` is ``true`` for any ``x`` in ``T``).

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


