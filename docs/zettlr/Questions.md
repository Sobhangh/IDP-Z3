–-
title: Questions
tags: #analysis
   ID: 20200504142301
–-
A question can be answered by giving it a value: it's a sub-formula or term, without quantified variables.

There are different types of assignments:
* quantified formula: before or after quantifier expansion
* free vs bound expressions (i.e. with quantified variable)
* terms : ground terms vs nested terms (e.g. f(X), where X is a constant) 
* shown to user or not (depending on view, with or without underscore in front of name)
* relevant or not
* made by the program (.make()) or not, e.g. for definitions
* copy of an expression (by .copy())

What do we need ?
* for display : all applied symbols + comparisons + quantified expressions
* for propagate: don't care (Z3 will do what's needed)
* for relevance: same as for display (Z3 consequences will reduce the other expressions anyway)
* for explain: all free comparisons and predicates, to be as explicit as possible over the steps

Principles:
* Case.viewed < Idp.viewable < Case.assignments
    * viewable (= GUIlines)
        * all ground instances + quantified expressions + free applied symbols and free comparisons before expansion
    * shown ≤ showable
        * based on normal view vs expanded view → is_visible
    * all (→ Assignments)
        * shown + questionables after expansion
* Expr.questions: computed for each top expression in simplified + questions; reduced by 1 after each substitute
* we need to determine propagated value and relevance for all Case.assignments

Todo:
- [ ] compute Expr.questions for each constraints
- [ ] reduce Expr.questions after each substitute
- [ ] rename GUILines as showable, and reduce it per view