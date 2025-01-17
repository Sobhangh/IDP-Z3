.. |n|      replace:: ``n``
.. |phi|    replace:: ``ϕ``
.. |t|      replace:: ``t``
.. |t1|     replace:: ``t_1``
.. |t2|     replace:: ``t_2``
.. |t3|     replace:: ``t_3``
.. |t1,tn|  replace:: ``t_1, t_2,.., t_n``
.. |v1,vn|  replace:: ``v_1  v_2 .. v_n``

.. index:: theory

Theory
------
.. code::

    theory T:V {
        // here comes the theory named T, on vocabulary named V
    }

A *theory* is a set of axioms and definitions to be satisfied, and of symbol interpretations.
If the names are omitted, the theory is named T, for vocabulary V.

Symbol interpretations are described in the Section on :ref:`Structure<Structure>`.
Before explaining the syntax of axioms and definitions, we need to introduce the concept of term.

.. _term:
.. index:: term

Mathematical expressions and Terms
++++++++++++++++++++++++++++++++++

A *term* is inductively defined as follows:

Boolean, Numeric and Date literals

    ``true`` and ``false`` are boolean terms.

    Numeric literals that follow the `Python conventions <https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals>`_
    are numerical terms of type ``Int`` or ``Real``.

    Date literals are terms.  They follow ISO 8601 conventions, prefixed with ``#`` (i.e., ``#yyyy-mm-dd``).
    ``#TODAY`` is also a Date literal representing today's date.
    ``#TODAY(y, m, d)`` is a Date literal representing today shifted by ``y`` years, ``m`` months and ``d`` days,
    where ``y``, ``m`` and ``d`` are integer literals (e.g., ``#TODAY(-18, 0, 0)`` is today 18 years ago).

Constructor
    Each constructor of a type_ is a term having that type.

Variable
    A variable is a term. Its type_ is derived from the `quantifier expression`_ that declares it (see below).

.. _function application:

Function application
    ``F(t_1, t_2,.., t_n)`` is a term, when ``F`` is a function_ symbol of arity |n|, and |t1,tn| are terms.
    Each term must be of the appropriate type_, and in the domain of the function,
    as defined in the function declaration in the vocabulary.
    The resulting type and range of the function application is also defined in the function declaration.
    If the arity of ``F`` is 0, i.e., if ``F`` is a constant_, then ``F()`` is a term.

    .. warning::
        The knowledge engineer must use appropriate if-then-else guards
        to ensure that the value of a function outside of its domain
        has no influence on the truth value of a statement.

        For example: ``if y = 0 then 0 else x/y``.

    ``$(s)(t_1, t_2,.., t_n)`` is a term, when ``s`` is an expression of type Concept
    that denotes a function of arity |n|, and |t1,tn| are terms.

    Please note that there are built-in function_\ s (see :ref:`built-in functions`).

Negation
    -|t| is a numerical term, when |t| is a numerical term.

Arithmetic
    ``t_1 ꕕ t_2`` is a numerical term, when |t1|, |t2| are two numerical terms,
    and ``ꕕ`` is one of the following math operators ``+, -, * (or ⨯), /, ^, %``.
    Mathematical operators can be chained as customary (e.g. ``x+y+z``).
    The usual order of binding is used.

Parenthesis
    (|t|) is a term, when |t| is a term

Cardinality aggregate
    ``#{v_1 in typeOfV_1, .., v_n in typeOfV_n : ϕ}`` is a numerical term when |v1,vn| are variables, and |phi| is a sentence_ containing these variables.
    If ``: ϕ`` is omitted, |phi| is presumed to be ``true``.

    The term denotes the number of tuples of distinct values for |v1,vn| which make |phi| true.

Aggregate over sets
    ``agg{ t | v_1 in typeOfV_1, .., v_n in typeOfV_n : p}`` is
    a numerical term where ``agg`` can be ``min`` or ``max``,
    |v1,vn| are variables, |t| is a term and ``p`` is a boolean expression.
    The variables declared by the aggregate can occur in ``t`` and ``p``.
    If ``: p`` is omitted, ``p`` is presumed to be ``true``.

    This aggregate denotes the minimum (resp. maximum) of term ``t``
    for each value of the variables that satisfies ``p``.
    Note that the set must be non-empty.

Aggregate over multisets
    The term ``agg{{ t | v_1 in typeOfV_1, .., v_n in typeOfV_n : p}}``
    where ``agg`` can be ``sum``, ``min`` or ``max``,  denotes
    the aggregate of the term ``t`` for each value of the variables that satisfies boolean expression ``p``.
    The variables declared by the aggregate can occur in ``t`` and ``p``.
    If ``: p`` is omitted, ``p`` is presumed to be ``true``.
    Note that the set must be non-empty, or the aggregate must be ``sum''.

(if .. then .. else ..)
    ``(if t_1 then t_2 else t_3)`` is a term when |t1| is a formula, |t2| and |t3| are terms of the same type.


.. _formula:
.. _sentence:
.. _axiom:
.. index:: formula, sentence, axiom

Sentences and axioms
+++++++++++++++++++++++++

An *axiom* is a sentence followed by ``.``.
A *sentence* is a well-formed formula without free variables
(i.e., in which every variable appear in the scope of a quantifier that declares it).
A *formula* is inductively defined as follows:

true and false
    ``true`` and ``false`` are formulae.

.. _predicate application:

Predicate application
    ``P(t_1, t_2,.., t_n)`` is a formula, when ``P`` is a predicate_ symbol of arity |n|, and |t1,tn| are terms.
    Each term must be of the appropriate type_, as defined in the predicate declaration.
    If the arity of ``P`` is 0, i.e., if ``P`` is a proposition, then ``P()`` is a formula.

    ``$(s)(t_1, t_2,.., t_n)`` is a formula, when ``s`` is an expression of type Concept that denotes a predicate of arity |n|, and |t1,tn| are terms.

Comparison
    ``t_1 ꕕ t_2`` is a formula, when |t1|, |t2| are two numerical terms and ``ꕕ`` is one of the following comparison operators ``<, ≤, =, ≥, >, ≠`` (or,  using ascii characters: ``=<, >=, ~=``).
    Comparison operators can be chained as customary.

Negation
    ``¬ϕ`` is a formula (or, using ascii characters: ``~ϕ``) when |phi| is a formula.

Logic connectives
    ``ϕ_1 ꕕ ϕ_2`` is a formula when ``ϕ_1, ϕ_2`` are two formulae and ``ꕕ`` is one of the following logic connectives ``∨,∧,⇒,⇐,⇔`` (or using ascii characters: ``|, \&, =>, <=, <=>`` respectively).
    Logic connectives can be chained as customary.

    Connectives can be written in English, e.g. ``and``.
    See full list of English connectives in  :ref:`Syntax summary <English>`.

Parenthesis
    (|phi|) is a formula when |phi| is a formula.

.. _quantifier expression:
.. index:: quantifier expression

Enumeration
    An enumeration (e.g. ``p := {1;2;3}``) is a formula.
    Enumerations follow the syntax described in `structure`_.

Quantified formulas
    *Quantified formulas* are formulae.
    They have one of the following forms, where ``v_1, .., v_n`` are variables,
    ``p, p_1, .., p_n`` are types or predicates,
    and |phi| is a formula involving those variables:

    .. code::

        ∀ v_1, v_n: ϕ(v_1, v_n).

        ∀ v_1, v_n ∈ p: ϕ(v_1, v_n).

        ∀ (v_1, v_n) ∈ p: ϕ(v_1, v_n).

        ∀ v_1 ∈ p_1, v_n ∈ p_n: ϕ(v_1, v_n).

    Alternatively, the existential quantifier, ``∃``, can be used.
    Ascii characters can also be used: ``?``, ``!``, respectively.
    For example, ``! x, y in Int: f(x,y)=f(y,x).``

    A variable may only occur in the |phi| formula of a quantifier declaring that variable.
    In the first form above, the type of each variable is inferred
    from their declaration or from their use in |phi|.


"is enumerated"
    ``f(a,b) is enumerated`` is a formula,
    where ``f`` is a function defined by a (partial) enumeration and applied to arguments ``a`` and ``b``.
    Its truth value reflects whether ``(a,b)`` is enumerated in ``f``'s (partial) enumeration.
    If the enumeration has a default value, every tuple of arguments is enumerated.

"in {1,2,3,4}"
    ``f(args) in enum`` is a formula, where
    ``f`` is a function applied to arguments ``args``
    and ``enum`` is an enumeration.
    This can also be written using Unicode: ``f() ∈ {1,2,3}``.

if .. then .. else ..
    ``if t_1 then t_2 else t_3`` is a formula when |t1|, |t2| and |t3| are formulae.


.. _definition:
.. index:: definition

Definitions
+++++++++++

A *definition* defines concepts, i.e. predicate_\ s or function_\ s, in terms of other concepts.
A definition consists of a set of rules, enclosed by ``{`` and ``}``.

If a predicate is inductively defined in terms of itself,
the definition employs the *well-founded* mode of interpretation by default.
The other possible modes of interpretation are ``completion``, ``Kripke-Kleene``,
``co-induction``, ``stable'' and ``recursive`` (for :ref:`recursive datatypes<recursive_datatypes>`).
They can be selected by placing the keyword in parenthesis at the beginning of the definition,
e.g., ``{ (completion) ...}``.

.. index:: rule

*Rules* have one of the following forms:

.. code::

    ∀ v_1 ∈ T_1, v_n ∈ T_n: P(t_1, .., t_n) ← |phi|.

    ∀ v_1 ∈ T_1, v_n ∈ T_n: F(t_1, .., t_n) = t ← |phi|.

where P is a predicate_ symbol, F is a function_ symbol,
|t|, |t1,tn| are terms that may contain the variables |v1,vn|
and |phi| is a formula that may contain these variables.
``P(t_1, t_2,.., t_n)`` is called the *head* of the rule and |phi| the *body*.
``<-`` can be used instead of ``←``, and ``≜`` instead of ``=``.
If the body is ``true``, the left arrow and body of the rule can be omitted.



.. _annotation:
.. index:: annotation

Annotations
+++++++++++

Some expressions can be annotated with their informal meaning, between brackets.
For example, ``[age is a positive number] 0 =< age()``.
Such annotations are used in the `Interactive Consultant <interactive_consultant.html>`_.

The following expressions can be annotated:

* Definitions
* Rules
* Constraints
* Quantified formula
* Comparisons
* Membership in an enumeration
* Brackets

When necessary, use parenthesis to avoid ambiguity, e.g. ``[Positive or p] ( [Positive] x()<0 ) | p().``.
