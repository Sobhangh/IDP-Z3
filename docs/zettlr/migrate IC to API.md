–-
title: migrate IC to API
tags: #refactoring
   ID: 20201020095431
–-

Goal: use IDP API in Interactive Consultant code

See [[Non-linear equations in Z3]]

Interactive Code would become:
~~~~
self.problem = Problem(environment, environment_structure)
self.problem.symbolic_propagate(tag=Env_Univ, simplify=True)
self.problem.add(nv_given, simplify=True) // need to separate ?
self.problem.propagate(tag=Env_Consq)

self.problem.add(decision, decision_structure)
self.problem.symbolic_propagate(tag=Universal, simplify=True)
self.problem.add(dec_given, simplify=True)
self.problem.propagate(tag=Consequence, simplify=True)
self.problem.get_relevant()
~~~~

TODO:
X API: propage questions first, then terms ? does not matter if no simplification
- [ ] IC: do not restart propagation if model is unknown: it won't fix anything
- [ ] IC: do not cascade propagate: full propagate will take care of it
- [ ] move definitions, constraints, assignments to Case.Problem just before get_relevant
- [ ] API: add simplify with one assignment
- [ ] API: add simplify option to propagate
- [ ] API: add tag argument to propagate
- [ ] use API for Case.propagate
- [ ] API: add symbolic_propagate