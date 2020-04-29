–-
title: Relevance and consequences
tags: #abandoned
   ID: 20200403111308
–-

Problem:consequences may or may not be relevant: how to make the difference ?

Solution: Keep track of 'justifiers', i.e. of the atoms in the proof of the simplification
* when simplifying an expression
* when propagating
The relevant atoms are those remaining in the simplified expressions **+ the justifiers in it**.
This can also be used to explain consequences !

TODO:
- [x] replace justification by just_branch
- [x] add Expression.proof = OrderedSet[Expression] the proof of an atom = assignments + constraint
- [ ] _change:(proof, …) : add proof → no Brackets anymore → Expression.eq
- [ ] getsubtences: add subtences of a proof
- [ ] Case: get relevant after propagation, no need to compute relevant_symbols
- [ ] Explain

When are consequences relevant ?
* consequences obtained by syntactic simplification (including definitions )
* consequences that are instance assignments

what is a (partial) proof ?
* a list of [[subtences]] that are known to be True or False, and of variable changes to ground
    * more precise than a list of changes
* that contribute to proving a subtence
* not: expand_quantifiers (instantiate), fresh-variable substitutions (instantiate)

problem with p & q => s. p. q.
* after p is injected, we have (q) => s.
* when q is injected, the proof of p&q is lost
    * root causes / options:
        * __eq__ compares str ⇒ the implication (not the conjunction) is replaced → change __eq__
            * require identical types ? 
                * not fool proof as you may have a mix of conjunct/disjunct ? no, because replace by value or bool
            * keep AST tree unchanged, but attach a value to each node ?
            * [[substitute]] and update_exprs have their own equality condition ?
        * reify subtences with just_branch, to avoid nested comparisons ?
        * the implication does not know that p is part of the proof → propagate proofs to top: expensive ??
        * pass the subtence being changed; add it as a reason to the proof when an expression is impacted
            * will not work with conjuctions, disjunctions (won't simplify)

Do I need 2 proofs ?  of true and of false ? for conjunctions / disjunctions

equalities:
* = true/false for simplification
* substitution of variables
* 



#analysis