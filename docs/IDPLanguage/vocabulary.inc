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

IDP-Z3 has the following built-in types:  ``Bool``, ``Int``, ``Real``, ```Symbols``.

Custom types can be defined by specifying a range of numeric literals, or a list of constructors (of arity 0).
Their name should be capitalized, by convention.

.. code::

    type Side = {1..4}
    type Color constructed from {red, blue, green}

The type ```Symbols`` has one constructor for each symbol (i.e., function, predicate or constant) declared in the vocabulary.
The constructors are the names of the symbol, prefixed with `````
For the above example, the constructors of ```Symbols`` are : ```red``, ```blue``, ```green``.


.. _function:
.. index:: function

Functions
+++++++++

A function with name ``MyFunc``, input types ``T1``, ``T2``, ``T3`` and output type ``T``, is declared by:

.. code::

    MyFunc(T1, T2, T3) : T

IDP-Z3 does not support partial functions.

.. _predicate:
.. index:: predicate

Predicates
++++++++++

A predicate with name ``MyPred`` and argument types ``T1``, ``T2``, ``T3`` is declared by:

.. code::

    MyPred(T1, T2, T3)

.. _constant:
.. index:: constant, proposition

Propositions and Constants
++++++++++++++++++++++++++

A proposition is a predicate of arity 0; a constant is a function of arity 0.

.. code::

    MyProposition
    MyConstant: Int


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


