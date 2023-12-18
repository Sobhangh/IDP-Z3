.. _vocabulary:
.. index:: vocabulary

Vocabulary
----------

.. code::

    vocabulary V {
        // here comes the vocabulary named V
    }

The *vocabulary* block specifies the types, predicates, functions and variables used to describe the problem domain.
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

The built-in types are:  ``𝔹``, ``ℤ``, ``ℝ``, ``Date``, and ``Concept[signature]``
(where ``signature`` is any type signature, e.g. ``()->Bool``).
The equivalent ASCII symbols are ``Bool``, ``Int``, and ``Real``.

The type ``Concept[T1⨯..⨯Tn -> T]`` has one constructor for each symbol (i.e., function, predicate or constant)
that have been declared in the vocabulary with exactly the domain ``T1⨯..⨯Tn`` and range ``T``.
The constructors are the names of the symbol, prefixed with `````.

Custom types are declared using the keyword ``type``, e.g., ``type color``.
Their name should be singular and capitalized, by convention.

Their extension can be defined in a structure_, or directly in the vocabulary, by specifying:

* a list of (ranges of) numeric literals, e.g., ``type someNumbers ≜ {0,1,2}`` or ``type byte ≜ {0..255}``  (the ASCII equivalent of ``≜`` is ``:=``)

* a list of (ranges of) dates, e.g., ``type dates ≜ {#2021-01-01, #2022-01-01}`` or ``type dates ≜ {#2021-01-01 .. #2022-01-01}``

* a list of nullary constructors, e.g., ``type Color ≜ {Red, Blue, Green}``

* a list of n-ary constructors; in that case, the enumeration must be preceded by ``constructed from``,
e.g., ``type Color2 ≜ constructed from {Red, Blue, Green, RGB(R: Byte, G: Byte, B: Byte)}``

In the above example, the constructors of ```Color`` are : ``Red``, ``Blue``, ``Green``.

The constructors of ```Color2`` are : ``Red``, ``Blue``, ``Green`` and ``RGB``.
Each constructor have an associated function (e.g., ``is_Red``, or ``is_RGB``)
to test if a Color2 term was created with that constructor.
The ``RGB`` constructor takes 3 arguments of type ``Byte``.
``R``, ``G`` and ``B`` are accessor functions:
when given a Color2 term constructed with RGB, they return the associated Byte.
(When given a Color2 not constructed with RGB, they may raise an error)

Constructors can be used to construct :ref:`recursive datatypes<recursive_datatypes>` ,
 e.g., ``type List := constructed from {nil, cons(car:Color, cdr: List)}``.
(However, unsatisfiable theories with recursive definitions do not terminate;
propagation and explanation inferences are not supported).


.. _predicate:
.. index:: predicate

Predicates
++++++++++

A predicate is declared using one of these templates:

.. code::

    p1 : T1⨯..⨯Tn → 𝔹
    p  : T1⨯..⨯Tn → 𝔹T (p << p1)
    p  : T1⨯..⨯Tn → 𝔹T (p << q1⨯..⨯qn)


where ``T1⨯..⨯Tn`` specify the type of the arguments of the predicates,
and the expression between parenthesis specifies a superset of the interpretation of the predicate.
This superset can be a predicate with the same type signature,
or the cross-product of unary predicates that are subsets of the types in the type signature.

The predicate names should start with a lowercase letter, by convention.
The ASCII equivalent of ``⨯`` is ``*``, and of ``→`` is ``->``.

A unary predicate is always interpreted as a subset of a type.
A nullary predicate is a subset of the singleton set containing the empty tuple.


.. _function:
.. index:: function

Functions
+++++++++

The functions with name ``myFunc1``, ``myFunc2``, argument types ``T1⨯..⨯Tn``, and output range ``T``,
are declared using one of these templates:

.. code::

    myFunc0 : T1⨯..⨯Tn → T (total)
    myFunc1, myFunc2 : T1⨯..⨯Tn → T (domain: p1⨯..⨯pn, range: p)

The ``(total)`` keyword is optional.
The ``domain`` (resp. ``range``) must be used to specify
the domain of definition (resp. the range) of the function
when it differs from ``T1⨯..⨯Tn`` (resp. ``T``).
Symbols ``p1, .. pn, p`` can be :

* previously-declared types
* previously-declared unary predicates
* ``Concept[<signature>]`` to denote the set of concepts with a particular domain signature, e.g. ``Concept[Person -> Bool]``.


The function names should start with a lowercase letter, by convention.
The ASCII equivalent of ``⨯`` is ``*``, and of ``→`` is ``->``.



.. _variable declaration:
.. index:: variable declaration

Variable Declarations
+++++++++++++++++++++

A variable may be declared with its type:

.. code::

    var x ∈ T

This is convenient for quantifications:
the type of the variable may be omitted in quantifications:
its declared type will be assumed.

A quantification cannot use a declared variable to quantify over another type than the declared one.

The variables ``x1, x2, ...`` are implicitly declared with the same type as ``x``.
(the variable in the declaration may not have a digital suffix)


.. _built-in functions:

Built-in functions
++++++++++++++++++

The following functions are built-in:

* ``abs: Int → Int`` (or ``abs: Float → Float``) yields the absolute value of an integer (or float) expression;


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
        import V
        // here comes the vocabulary named W
    }


.. _Vannotations:
.. index:: annotation (vocabulary)

Symbol annotations
++++++++++++++++++

To improve the display of functions and predicates in the :ref:`Interactive Consultant <Consultant>`,
their declaration in the vocabulary can be annotated with their intended meaning, a short comment, or a long comment.
These annotations are enclosed in ``[`` and ``]``, and come before the symbol declaration.

.. _meaning:
.. index:: intended meaning

Intended meaning
    ``[this is a text]`` specifies the intended meaning of the symbol.
    This text is shown in the header of the symbol's box.

Short info
    ``[short:this is a short comment]`` specifies the short comment of the symbol.
    This comment is shown when the mouse is over the info icon in the header of the symbol's box.

Long info
    ``[long:this is a long comment]`` specifies the long comment of the symbol.
    This comment is shown when the user clicks the info icon in the header of the symbol's box.

English expression
    ``[EN:{1} is a prime]`` specifies the English expression for ``prime: Int -> Bool``.
    This information is used to generate the informal reading of a Theory.
    The number between brackets represents a placeholder for the English reading of the nth argument.

Slider
    ``[slider: (a, b) in (0, 100)]`` displays as slider for a numeric value.
    The slider has a maximum range of [0, 100] that is reduced to [a(), b()]
    when the values of a() and b() are known
    (``a`` and ``b`` are symbols in the vocabulary).


