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

super.init()
self.add(self.environment)
self.add(decision)
self.add(decision_structure)
self.symbolic_propagate(tag=Universal)

self.environemnt.add(given)
self.environment.propagate(tag=Env_Consq)
copy assignments from environment to self
self.propagate(tag=Consequence)

self.simplify()
self.get_relevant()
~~~~

TODO:
X API: propage questions first, then terms ? does not matter if no simplification
X IC: do not restart propagation if model is unknown: it won't fix anything
- [x] IC abstract : use assignments, not guilines
- [x] IC: case.GUILines is the same as case.assignments
- [x] API propagate: consider all assignments without value
    - [x] API problem: fill assignments with all subtences
X API: restart solver if unknown (not needed ?)
- [ ] move definitions, constraints, assignments to Case.Problem just before get_relevant
- [X] API: add simplify
- [X] IC: do not cascade propagate: full propagate will take care of it.  Use API.simplify instead
- [ ] API: add tag argument to propagate
- [ ] use API for Case.propagate
- [ ] IC: remove Case.translate
- [ ] API: add symbolic_propagate