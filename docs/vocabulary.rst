Vocabulary
----------

The vocabulary block specifies the types, predicates, functions and constants used to describe the problem domain.
Each declaration goes on a new line (or are space separated).

Symbols begins with an alphabetic character or ``_``, followed by alphanumeric characters or ``_``.  
Symbols can also be string literals delimited by ``'``, e.g., ``'blue planet'``.


Types
+++++

IDP-Z3 has the following built-in types:  ``bool``, ``int``, ``real``, ```Symbols``.

Custom types can be defined by specifying a range of numeric values, or a list of constructors (of arity 0).

.. code-block::

    type side = {1..4}
    type color constructed from {red, blue, green}

Functions
+++++++++

IDP-Z3 has the following built-in functions (to be used as operators):

    * ``+(int, int): int``
    * ``-(int, int): int``
    * ``*(int, int): int``
    * ``/(int, int): int``
    * ``%(int, int): int`` modulo operator
    * ``^(int, int): int`` power operator
    * ``abs(int): int``
    * ``+(real, real): real``
    * ``-(real, real): real``
    * ``*(real, real): real``
    * ``/(real, real): real``
    * ``^(real, int): real`` power operator
    * ``abs(real): int``

A function with name ``MyFunc``, input types ``T1``, ``T2``, ``T3`` and output type ``T``, is declared by:

.. code-block::
    
    MyFunc(T1, T2, T3) : T

IDP-Z3 does not support partial functions.

Predicates
++++++++++

IDP-Z3 has the following built-in predicates (to be used as operators): ``<``, ``=<`` (or ``≤``), ``=``, ``>=`` (or ``≥``), ``>``, ``~=`` (or ``≠``).

A predicate with name ``MyPred`` and argument types ``T1``, ``T2``, ``T3`` is declared by:

.. code-block::
    
    MyPred(T1, T2, T3)

Propositions and Constants
++++++++++++++++++++++++++

A proposition is a predicate of arity 0; a constant is a function of arity 0.

.. code-block::
    
    MyProp1 MyProp2.
    MyConstant: int

Symbols type
++++++++++++

The type ```Symbols`` has one constructor for each function/predicate/constant declared in the vocabulary.
For the above example, the ```Symbols`` are : ```MyFunc``, ```MyPred``, ```MyProp1``, ```MyProp1``, ```MyConst``.

