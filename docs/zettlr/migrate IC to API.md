–-
title: migrate IC to API
tags: #refactoring
   ID: 20201020095431
–-

Goal: use IDP API in Interactive Consultant code

See [[Non-linear equations in Z3]]

Interactive Code would become:
~~~~
self.environment = Problem(environment, environment_structure)
self.environment.symbolic_propagate(tag=Env_Univ)
self.decision = Problem([self.environment, decision, decision_structure])
self.decision.symbolic_propagate(tag=Universal)

self.environment.add(given)
# this is a hack: use the same set of assignments
self.environment.assignments = self.decision.assignments
self.environment.propagate(tag=Env_Consq)
self.decision.propagate(tag=Consequence)

self.decision.simplify()
self.decision.get_relevant()
~~~~

TODO:
X API: propage questions first, then terms ? does not matter if no simplification
X IC: do not restart propagation if model is unknown: it won't fix anything
- [x] IC abstract : use assignments, not guilines
- [x] IC: GUILines contains only the assignments shown to user
- [x] API propagate: consider all assignments without value
    - [x] API problem: fill assignments with all subtences
X API: restart solver if unknown (not needed ?)
- [ ] move definitions, constraints, assignments to Case.Problem just before get_relevant
- [ ] API: add simplify with one assignment
- [ ] IC: do not cascade propagate: full propagate will take care of it.  Use API.simplify instead
- [ ] API: add simplify option to propagate
- [ ] API: add tag argument to propagate
- [ ] use API for Case.propagate
- [ ] IC: remove Case.translate
- [ ] API: add symbolic_propagate