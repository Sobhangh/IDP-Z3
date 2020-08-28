.. _vocabulary:
.. index:: vocabulary

Vocabulary
----------

.. code-block::

    vocabulary V {
        // here comes the vocabulary named V
    }

The vocabulary block specifies the types, predicates, functions and constants used to describe the problem domain.
Each declaration goes on a new line (or are space separated).

Symbols begins with an alphabetic character or ``_``, followed by alphanumeric characters or ``_``.  
Symbols can also be string literals delimited by ``'``, e.g., ``'blue planet'``.

.. _type:
.. _constructor:
.. index:: type, constructor

Types
+++++

IDP-Z3 has the following built-in types:  ``bool``, ``int``, ``real``, ```Symbols``.

Custom types can be defined by specifying a range of numeric literals, or a list of constructors (of arity 0).

.. code-block::

    type side = {1..4}
    type color constructed from {red, blue, green}

.. _function:
.. index:: function

Functions
+++++++++

A function with name ``MyFunc``, input types ``T1``, ``T2``, ``T3`` and output type ``T``, is declared by:

.. code-block::
    
    MyFunc(T1, T2, T3) : T

IDP-Z3 does not support partial functions.

.. _predicate:
.. index:: predicate

Predicates
++++++++++

A predicate with name ``MyPred`` and argument types ``T1``, ``T2``, ``T3`` is declared by:

.. code-block::
    
    MyPred(T1, T2, T3)

.. _constant:
.. index:: constant, proposition

Propositions and Constants
++++++++++++++++++++++++++

A proposition is a predicate of arity 0; a constant is a function of arity 0.

.. code-block::
    
    MyProp1 MyProp2.
    MyConstant: int

.. _symbol:
.. index:: symbol

Symbols type
++++++++++++

The type ```Symbols`` has one constructor for each function/predicate/constant declared in the vocabulary.
For the above example, the constructors of ```Symbols`` are : ```MyFunc``, ```MyPred``, ```MyProp1``, ```MyProp1``, ```MyConst``.

.. index:: annotation (vocabulary)

Vocabulary annotations
++++++++++++++++++++++

To improve the display of functions and predicates in the :ref:`Interactive Consultant <Consultant>`, 
they can be annotated with their intended meaning, a short comment, or a long comment.
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

.. _extern:
.. index:: include vocabulary

Include another vocabulary
+++++++++++++++++++++++++++

A vocabulary W may include a previously defined vocabulary V:

.. code-block::

    vocabulary W {
        extern vocabulary V
        // here comes the vocabulary named V
    }


