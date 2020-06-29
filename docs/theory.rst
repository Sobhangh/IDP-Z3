Theory
------

A *theory* is a set of constraints and definitions to be satisfied.
Before explaining their syntax, we need to introduce simpler concepts. 

.. _term:

Mathematical expressions and Terms
++++++++++++++++++++++++++++++++++

A *term* is inductively defined as follows:

Constant
    a constant_ is a term.

Function application
    :math:`F(t_1, t_2,.., t_n)` is a term, when :math:`F` is a function_ symbol of arity :math:`n`, and :math:`t_1, t_2,.., t_n` are terms.

Constructor
    a constructor for a type_ is a term.

Parenthesis
    :math:`(t_1)` is a term, when :math:`t_1` is a term

Numeric literal
    Numeric literals that follow the `Python conventions <https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals>`_ are terms.

Negation
    :math:`- t_1` is a numerical term, when :math:`t_1` is a numerical term.

Arithmetic
    :math:`t_1 ꕕ t_2` is a numerical term, when :math:`t_1, t_2` are two numerical terms, and :math:`ꕕ` is one of the following math operators :math:`+, -, *, /, \hat{}, \%`.

Cardinality aggregate
    :math:`\#\{v_1, v_2,.., v_n: \phi\}` is a term when :math:`v_1, v_2,.., v_n` are variables, and :math:`\phi` is a sentence_.

Arithmetic aggregate
    :math:`ꕕ\{v_1, v_2,.., v_n: \phi : t\}` is a term when :math:`ꕕ` is :math:`sum`, :math:`v_1, v_2,.., v_n` are variables, :math:`\phi` is a sentence_, and :math:`t` is a term.

Variable
    a variable is a term.

In the first two cases, the type_ of the term is derived from its declaration in the vocabulary_.
In the latter case, the type_ of a variable is derived from the `quantifier expression`_ that declares it (see below).  

In a function application, each argument must be of the appropriate type_.  
Mathematical operators can be chained as customary (e.g. :math:`x+y+z`).
The usual order of binding is used.

.. _sentence:
.. _constraint:

Sentences and constraints
+++++++++++++++++++++++++

A *sentence* is inductively defined as follows:

true and false
    ``true`` and ``false`` are sentences.

Predicate application
    :math:`P(t_1, t_2,.., t_n)` is a sentence, when :math:`P` is a predicate_ symbol of arity :math:`n`, and :math:`t_1, t_2,.., t_n` are terms.
    
Parenthesis
    :math:`(\phi)` is a sentence when :math:`\phi` is a sentence.
    
Comparison
    :math:`t_1 ꕕ t_2` is a sentence, when :math:`t_1, t_2` are two numerical terms and :math:`ꕕ` is one of the following comparison operators :math:`<, ≤, =, ≥, >, ≠` (or,  using ascii characters: :math:`=<, >=, \sim=`).

Negation
    :math:`\lnot \phi` is a sentence (or,  using ascii characters: :math:`\sim \phi`) when :math:`\phi` is a sentence.

Logic connectives
    :math:`\phi_1 ꕕ \phi_2` is a sentence when :math:`\phi_1, \phi_2` are two sentences and :math:`ꕕ` is one of the following logic connectives :math:`\lor, \land, \Rightarrow, \Leftarrow, \Leftrightarrow` (or using ascii characters: :math:`|, \&, =>, <=, <=>` respectively).

.. _quantifier expression:

Quantified formulas
    :math:`\exists x[typeOfX]: \phi` and :math:`\forall x[typeOfX]: \phi`  (or, using ascii characters: :math:`?, !` respectively) are *quantifier formulas* with variable :math:`x`, when :math:`\phi` is a sentence.

In a predicate application, each argument must be of the appropriate type_.
Comparison operators and logic connectives can be chained as customary.
A variable may only occur in the scope of a quantifier for that variable.

A *constraint* is a sentence followed by ``.``.