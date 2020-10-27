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
self.problem.add(env_given, simplify=True) // need to separate the given !
self.problem.propagate(todo=self.GUILines, tag=Env_Consq, simplify=True)

self.problem.add(decision)
self.problem.add(decision_structure)
self.problem.symbolic_propagate(tag=Universal, simplify=True)
self.problem.add(dec_given, simplify=True)
self.problem.propagate(todo=self.GUILines, tag=Consequence, simplify=True)
self.problem.get_relevant()
~~~~

TODO:
X API: propage questions first, then terms ? does not matter if no simplification
X IC: do not restart propagation if model is unknown: it won't fix anything
- [x] IC abstract : use assignments, not guilines
- [x] IC: GUILines contains only the assignments shown to user
- [x] API propagate: consider all assignments without value
    - [x] API problem: fill assignments with all subtences
X API: restart solver if unknown (not needed ?)
- [ ] API: add simplify with one assignment
- [ ] move definitions, constraints, assignments to Case.Problem just before get_relevant
- [ ] IC: do not cascade propagate: full propagate will take care of it.  Use API.simplify instead
- [ ] API: add simplify option to propagate
- [ ] API: add tag argument to propagate
- [ ] use API for Case.propagate
- [ ] IC: remove Case.translate
- [ ] API: add symbolic_propagate