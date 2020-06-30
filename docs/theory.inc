.. |n|      replace:: :math:`n`
.. |not|    replace:: :math:`\lnot`
.. |phi|    replace:: :math:`\phi`
.. |t|      replace:: :math:`t`
.. |t1|     replace:: :math:`t_1`
.. |t2|     replace:: :math:`t_2`
.. |t1,tn|  replace:: :math:`t_1, t_2,.., t_n`
.. |v1,vn|  replace:: :math:`v_1, v_2,.., v_n`

.. index:: theory

Theory
------

A *theory* is a set of constraints and definitions to be satisfied.
Before explaining their syntax, we need to introduce the concept of term. 

.. _term:
.. index:: term

Mathematical expressions and Terms
++++++++++++++++++++++++++++++++++

A *term* is inductively defined as follows:

Constant
    a constant_ is a term.

.. _function application:

Function application
    :math:`F(t_1, t_2,.., t_n)` is a term, when :math:`F` is a function_ symbol of arity |n|, and |t1,tn| are terms.

Constructor
    a constructor for a type_ is a term.

Parenthesis
    (|t|) is a term, when |t| is a term

Numeric literal
    Numeric literals that follow the `Python conventions <https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals>`_ are terms.

Negation
    -|t| is a numerical term, when |t| is a numerical term.

Arithmetic
    :math:`t_1 ꕕ t_2` is a numerical term, when |t1|, |t2| are two numerical terms, and :math:`ꕕ` is one of the following math operators :math:`+, -, *, /, \hat{}, \%`.

Cardinality aggregate
    :math:`\#\{v_1, v_2,.., v_n: \phi\}` is a term when |v1,vn| are variables, and |phi| is a sentence_ containing these variables.

    The term denotes the number of tuples of distinct values for |v1,vn| which make |phi| true.

Arithmetic aggregate
    :math:`ꕕ\{v_1, v_2,.., v_n: \phi : t\}` is a term when :math:`ꕕ` is :math:`sum`, |v1,vn| are variables, |phi| is a sentence_, and |t| is a term.

    The term denotes the sum of |t| for each distinct tuple of values for |v1,vn| which make |phi| true.

Variable
    a variable is a term.

In the first two cases, the type_ of the term is derived from its declaration in the vocabulary_.
In the latter case, the type_ of a variable is derived from the `quantifier expression`_ that declares it (see below).  

In a function application, each argument must be of the appropriate type_.  
Mathematical operators can be chained as customary (e.g. :math:`x+y+z`).
The usual order of binding is used.

.. _sentence:
.. _constraint:
.. index:: sentence, constraint

Sentences and constraints
+++++++++++++++++++++++++

A *constraint* is a sentence followed by ``.``.
A *sentence* is inductively defined as follows:

true and false
    ``true`` and ``false`` are sentences.

.. _predicate application:

Predicate application
    :math:`P(t_1, t_2,.., t_n)` is a sentence, when :math:`P` is a predicate_ symbol of arity |n|, and |t1,tn| are terms.
    If the arity of :math:`P` is 0, i.e., if :math:`P` is a proposition, then :math:`P` and :math:`P()` are sentences.
    
Parenthesis
    (|phi|) is a sentence when |phi| is a sentence.
    
Comparison
    :math:`t_1 ꕕ t_2` is a sentence, when |t1|, |t2| are two numerical terms and :math:`ꕕ` is one of the following comparison operators :math:`<, ≤, =, ≥, >, ≠` (or,  using ascii characters: :math:`=<, >=, \sim=`).

Negation
    |not| |phi| is a sentence (or,  using ascii characters: :math:`\sim \phi`) when |phi| is a sentence.

Logic connectives
    :math:`\phi_1 ꕕ \phi_2` is a sentence when :math:`\phi_1, \phi_2` are two sentences and :math:`ꕕ` is one of the following logic connectives :math:`\lor, \land, \Rightarrow, \Leftarrow, \Leftrightarrow` (or using ascii characters: :math:`|, \&, =>, <=, <=>` respectively).

.. _quantifier expression:
.. index:: quantifier expression

Quantified formulas
    :math:`\exists x[typeOfX]: \phi` and :math:`\forall x[typeOfX]: \phi`  (or, using ascii characters: :math:`?, !` respectively) are *quantifier formulas* with variable :math:`x`, when |phi| is a sentence.

In a predicate application, each argument must be of the appropriate type_.
Comparison operators and logic connectives can be chained as customary.
A variable may only occur in the scope of a quantifier for that variable.

.. _definition:
.. index:: definition

Definitions
+++++++++++

A *definition* defines concepts, i.e. predicate_\ s or function_\ s, in terms of other concepts.
A definition consists of a set of rules, enclosed by ``{`` and ``}``.

.. index:: rule
*Rules* have the following form:

.. math::

    \forall v_1[typeOfX_1] .. v_n[typeOfX_n] : P(t_1, .., t_n) \leftarrow \phi.

where P is a predicate_ symbol, |t1,tn| are terms that may contain the variables |v1,vn| and |phi| is a formula that may contain these variables.
:math:`P(t_1, t_2,.., t_n)` is called the *head* of the rule and |phi| the body.
'<-' can be used instead of ':math:`\leftarrow`'.
If the body is ``true``, the left arrow and body of the rule can be omitted.



