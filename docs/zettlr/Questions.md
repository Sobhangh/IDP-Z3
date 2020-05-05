–-
title: Questions
tags: 
   ID: 20200504142301
–-
A question can be answered by assigning it a value: it's a sub-formula or term, without quantified variables.

There are different types of questions:
* sub-formulas: before or after quantifier expansion
* terms : ground terms vs nested terms (e.g. f(X), where X is a constant) 
* shown to user or not (depending on view, with or without underscore in front of name)
* relevant or not
* made by the program (.make()) or not, e.g. for definitions
* copy of an expression (by .copy())

Principles:
* Case.shown < Idp.showable < Case.questions
    * showable (= GUIlines)
        * all ground instances from vocabulary + quantified expressions + applied symbols and comparisons before expansion without quantified variables
    * shown ≤ showable
        * based on normal view vs expanded view → is_visible
    * questions (= Assignments)
        * shown + applied symbols and comparison after expansion
* Expr.questions: computed for each top expression in simplified + questions; reduced by 1 after each substitute
* we need to determine propagated value and relevance for all Case.questions

Todo:
- [ ] compute Expr.questions for each constraints
- [ ] add Questions to Assignments, and compute their expr.questions
- [ ] reduce Expr.questions after each substitute
- [ ] rename GUILines as showable, and reduce it per view