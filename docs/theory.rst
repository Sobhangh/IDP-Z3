Theory
------

A *theory* is a set of constraints and definitions to be satisfied.
Before explaining their syntax, we need to introduce simpler concepts. 

Mathematical expressions and Terms
++++++++++++++++++++++++++++++++++

A *term* is inductively defined as follows:

    * a constant is a term;
    * if :math:`F` is a function symbol of arity :math:`n`, and :math:`t_1, t_2,.., t_n` are terms, then :math:`F(t_1, t_2,.., t_n)` is a term;
    * if :math:`t_1` is a numerical term, then :math:`- t_1, (t_1)` are numerical terms;
    * if :math:`t_1, t_2` are two numerical terms, then :math:`t_1 ꕕ t_2` is a numerical term, where :math:`ꕕ` is one of the following math operators :math:`+, -, *, /, \hat{}, \%`;
    * a variable is a term.

In the first two cases, the type of the term is derived from its declaration in the vocabulary.
In the latter case, the type of a variable is derived from the quantifier expression that declares it (see below).  

In a function application, each argument must be of the appropriate type.  
Mathematical operators can be chained as customary (e.g. :math:`x+y+z`).
The usual order of binding is used.

Sentences and constraints
+++++++++++++++++++++++++

A *sentence* is inductively defined as follows:

    * ``true`` and ``false`` are sentences;
    * if :math:`P` is a predicate symbol of arity :math:`n`, and :math:`t_1, t_2,.., t_n` are terms, then :math:`P(t_1, t_2,.., t_n)` is a sentence;
    * if :math:`t_1, t_2` are two numerical terms, then :math:`t_1 ꕕ t_2` is a sentence, where :math:`ꕕ` is one of the following comparison operators :math:`<, ≤, =, ≥, >, ≠` (or using ascii characters: :math:`=<, >=, \sim=`);
    * if :math:`\phi` is a sentence, then :math:`\lnot \phi, (\phi)` are sentences (or using ascii characters: :math:`\sim`);
    * if :math:`\phi_1, \phi_2` are two sentences, then :math:`\phi_1 ꕕ \phi_2` is a sentence, where :math:`ꕕ` is one of the following logic connectives :math:`\lor, \land, \Rightarrow, \Leftarrow, \Leftrightarrow` (or using ascii characters: :math:`|, \&, =>, <=, <=>` respectively);
    * if :math:`\phi` is a sentence, then :math:`\exists x[typeOfX]: \phi` and :math:`\forall x[typeOfX]: \phi` are *quantifier formulas* with variable :math:`x` (or using ascii characters: :math:`?, !` respectively).

In a predicate application, each argument must be of the appropriate type.
Comparison operators and logic connectives can be chained as customary.
A variable may only occur in the scope of a quantifier for that variable.

A *constraint* is a sentence followed by ``.``.