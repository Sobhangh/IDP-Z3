–-
title: Expression.value
tags: #refactoring
   ID: 20200415204633
–-

Idea: add a `.value` attribute to expressions, containing the truth value of a proposition, or the computed value of a term.
include also a `.status` attribute, to indicate the phase of computation
→ no need to change the tree structure !  No separate data structure for proofs !

Principle: a node must always contain:
* .code : the original source code in text
* relevant sub_exprs, and definition (don't lose info ! the value should always be computable)
* possibly a value, with status

TODO for relevance: in branch Pierre
- [ ] remove proof
- [ ] substitute(self, exprs, \*consequences) where exprs is a list of expr that contain a value and status
	and consequences {code: expression}
    - [ ] compute .value in update_exprs
    - [ ] test equal to True/False/ground-value using .value
    - [ ] Expression.copy()
    - [ ] eliminate replace_by(), \_change()
    - [ ] cut unnecessary branches from the justification tree by removing them in sub_exprs → get_subtences will work unchanged
        - or replacing them with bare TRUE/FALSE, e.g. for if-then-else
    - [ ] catch satisfied definitions in substitute, before they may disappear; generate 2 substitutions for equality
- [ ] implicants(self)
    - [ ] compute implicants by traversing the tree, searching for subtences, AppliedSymbols without values
    - [ ] generate 2 substitutions for equality (x→a, and (x=a) → true)  (only 1 if the equality is false)
    - [ ] rewrite Case.propagate
- [ ] other
    - [ ] batch substitute
    - [ ] remove dead code

Todo for explain
- [ ] Inference
    - [ ] generate explanation at each node

Issues:
* how to bypass nodes that are not subtences ?
    * get_subtences: easy
    * pretty printing ? Explain ? to be done

