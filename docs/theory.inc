.. |n|      replace:: :math:`n`
.. |not|    replace:: :math:`\lnot`
.. |phi|    replace:: :math:`\phi`
.. |t|      replace:: :math:`t`
.. |t1|     replace:: :math:`t_1`
.. |t2|     replace:: :math:`t_2`
.. |t3|     replace:: :math:`t_3`
.. |t1,tn|  replace:: :math:`t_1, t_2,.., t_n`
.. |v1,vn|  replace:: :math:`v_1  v_2 .. v_n`

.. index:: theory

Theory
------
.. code-block::

    theory T:V {
        // here comes the theory named T, on vocabulary named V
    }

A *theory* is a set of constraints and definitions to be satisfied.
If the names are omitted, the theory is named T, for vocabulary V.

Before explaining their syntax, we need to introduce the concept of term. 

.. _term:
.. index:: term

Mathematical expressions and Terms
++++++++++++++++++++++++++++++++++

A *term* is inductively defined as follows:

Numeric literal
    Numeric literals that follow the `Python conventions <https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals>`_ are numerical terms of type ``int`` or ``real``.

Constructor
    Each constructor of a type_ is a term having that type.

Constant
    a constant_ is a term whose type_ is derived from its declaration in the vocabulary_.

Variable
    a variable is a term. Its type_ is derived from the `quantifier expression`_ that declares it (see below).  

.. _function application:

Function application
    :math:`F(t_1, t_2,.., t_n)` is a term, when :math:`F` is a function_ symbol of arity |n|, and |t1,tn| are terms.
    Each term must be of the appropriate type_, as defined in the function declaration in the vocabulary.
    The resulting type of the function application is also defined in the function declaration.

Negation
    -|t| is a numerical term, when |t| is a numerical term.

Arithmetic
    :math:`t_1 ꕕ t_2` is a numerical term, when |t1|, |t2| are two numerical terms, and :math:`ꕕ` is one of the following math operators :math:`+, -, *, /, \hat{}, \%`.
    Mathematical operators can be chained as customary (e.g. :math:`x+y+z`).
    The usual order of binding is used.

Parenthesis
    (|t|) is a term, when |t| is a term

Cardinality aggregate
    :math:`\#\{v_1[typeOfV_1] .. v_n[typeOfV_n] : \phi\}` is a numerical term when |v1,vn| are variables, and |phi| is a sentence_ containing these variables.

    The term denotes the number of tuples of distinct values for |v1,vn| which make |phi| true.

Arithmetic aggregate
    :math:`ꕕ\{v_1[typeOfV_1] .. v_n[typeOfV_n] : \phi : t\}` is a numerical term when :math:`ꕕ` is :math:`sum`, |v1,vn| are variables, |phi| is a sentence_, and |t| is a term.

    The term denotes the sum of |t| for each distinct tuple of values for |v1,vn| which make |phi| true.

(if .. then .. else ..)
    :math:`(if\ t_1\ then\ t_2\ else\ t_3)` is a term when |t1| is a sentence, |t2| and |t3| are terms of the same type.


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
    Each term must be of the appropriate type_, as defined in the predicate declaration.
    If the arity of :math:`P` is 0, i.e., if :math:`P` is a proposition, then :math:`P` and :math:`P()` are sentences.
    
Comparison
    :math:`t_1 ꕕ t_2` is a sentence, when |t1|, |t2| are two numerical terms and :math:`ꕕ` is one of the following comparison operators :math:`<, ≤, =, ≥, >, ≠` (or,  using ascii characters: :math:`=<, >=, \sim=`).
    Comparison operators can be chained as customary.

Negation
    |not| |phi| is a sentence (or, using ascii characters: :math:`\sim \phi`) when |phi| is a sentence.

Logic connectives
    :math:`\phi_1 ꕕ \phi_2` is a sentence when :math:`\phi_1, \phi_2` are two sentences and :math:`ꕕ` is one of the following logic connectives :math:`\lor, \land, \Rightarrow, \Leftarrow, \Leftrightarrow` (or using ascii characters: :math:`|, \&, =>, <=, <=>` respectively).
    Logic connectives can be chained as customary.

Parenthesis
    (|phi|) is a sentence when |phi| is a sentence.
    
.. _quantifier expression:
.. index:: quantifier expression

Enumeration
    An enumeration (e.g. ``p = {1;2;3}``) is a sentence. 
    Enumerations follow the syntax described in `structure`_.

Quantified formulas
    *Quantified formulas* are sentences.
    They have one of these two forms, where :math:`v_1, .., v_n` are variables and |phi| is a sentence:

    .. math::

        \exists v_1[typeOfV_1] .. v_n[typeOfV_n]: \phi

        \forall v_1[typeOfV_1] .. v_n[typeOfV_n]: \phi

    Alternatively, ascii characters can be used: ``?``, ``!``, respectively.
    For example, ``!x[int] y[int]: f(x,y)=f(y,x).``
    A variable may only occur in the |phi| sentence of a quantifier declaring that variable.

    When quantifying a formula of type ```Symbols``, 
    the expression must contain a "guard" to prevent arity or type error.
    A guard is a predicate over ```Symbols`` that is defined by an enumeration in the same theory block.
    In the following example, ``symmetric`` must be defined by enumeration.

    .. code-block::

        !`p[`Symbols]: symmetric(`p) => (!x y : `p(x,y) => `p(y,x)).

"is (not) enumerated"
    :math:`f(a,b)\ is\ enumerated` and :math:`f(a,b)\ is\ not\ enumerated` are sentences, 
    where :math:`f` is a function defined by an enumeration and applied to arguments :math:`a` and :math:`b`.
    Its truth value reflects whether :math:`(a,b)` is enumerated in :math:`f`'s enumeration.
    If the enumeration has a default value, every tuple of arguments is enumerated.

"in {1,2,3,4}"
    :math:`f(args)\ in\ enumeration` is a sentence, where
    :math:`f` is a function applied to arguments :math:`args`
    and :math:`enumeration` is an enumeration.

if .. then .. else ..
    :math:`if\ t_1\ then\ t_2\ else\ t_3` is a sentence when |t1|, |t2| and |t3| are sentences.


.. _definition:
.. index:: definition

Definitions
+++++++++++

A *definition* defines concepts, i.e. predicate_\ s or function_\ s, in terms of other concepts.
A definition consists of a set of rules, enclosed by ``{`` and ``}``.

.. index:: rule

*Rules* have one of the following forms:

.. math::

    &\forall v_1[typeOfV_1] .. v_n[typeOfV_n] : P(t_1, .., t_n) \leftarrow \phi.

    &\forall v_1[typeOfV_1] .. v_n[typeOfV_n] : F(t_1, .., t_n)=t \leftarrow \phi.

where P is a predicate_ symbol, F is a function_ symbol, |t|, |t1,tn| are terms that may contain the variables |v1,vn| and |phi| is a formula that may contain these variables.
:math:`P(t_1, t_2,.., t_n)` is called the *head* of the rule and |phi| the *body*.
``<-`` can be used instead of ':math:`\leftarrow`'.
If the body is ``true``, the left arrow and body of the rule can be omitted.



