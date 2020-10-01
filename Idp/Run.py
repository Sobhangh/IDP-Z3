"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""

"""

Classes to execute the main block of an IDP program

"""

import types
from z3 import Solver, sat, ModelRef

from .Parse import *

class Problem(object):
    """ A combination of theories and structures
    """
    def __init__(self, theories):
        self.definitions = []
        self.clark = {} # {Declaration: Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()

        for t in theories:
            t.addTo(self)

    def translate(self):
        co_constraints = OrderedSet()
        for c in self.constraints:
            c.co_constraints(co_constraints)
        return And(
            sum((d.translate() for d in self.definitions), [])
            + [l.translate() for k, l in self.assignments.items() 
                    if l.value is not None]
            + [s.translate() for s in self.constraints]
            + [c.translate() for c in co_constraints]
            )

def addTo(self, problem):
    problem.definitions.extend(self.definitions)
    for decl, rule in self.clark.items():
        if decl not in problem.clark:
            problem.clark[decl] = rule
        else:
            new_rule = copy(rule)  # not elegant, but rare
            new_rule.body = AConjunction.make('∧', [problem.clark[decl].body, rule.body])
            problem.clark[decl] = new_rule
    problem.constraints.extend(self.constraints)
    problem.assignments.extend(self.assignments)
    #TODO apply definitions across theory blocks
Theory.addTo = addTo

def addTo(self, problem):
    problem.assignments.extend(self.assignments)
Structure.addTo = addTo


def model_expand(theories, structures, max=10):
    """ output: a list of Z3 models, ending with a string
    """
    theories = theories if not isinstance(theories, Theory) else [theories]
    structures = structures if not isinstance(structures, Structure) else [structures]

    problem = Problem(theories + structures)
    formula = problem.translate()

    solver = Solver()
    solver.add(formula)

    count = 0
    while count<max or max<=0:

        if solver.check() == sat:
            count += 1
            model = solver.model()
            yield model

            # exclude this model
            block = []
            for z3_decl in model: # FuncDeclRef
                arg_domains = []
                for i in range(z3_decl.arity()):
                    domain, arg_domain = z3_decl.domain(i), []
                    for j in range(domain.num_constructors()):
                        arg_domain.append( domain.constructor(j) () )
                    arg_domains.append(arg_domain)
                for args in itertools.product(*arg_domains):
                    block.append(z3_decl(*args) != model.eval(z3_decl(*args)))
            solver.add(Or(block))
        else:
            break

    if solver.check() == sat:
        yield f"{NEWL}More models are available."
    elif 0 < count:
        yield f"{NEWL}No more models."
    else:
        yield "No models."


def myprint(x):
    if isinstance(x, types.GeneratorType):
        for i, xi in enumerate(x):
            if isinstance(xi, ModelRef):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                myprint(xi)
            else:
                print(xi)
    else:
        print(x)

def execute(self):
    """ 
    Execute the IDP program
    """

    main = str(self.procedures['main'])
    mybuiltins = {'print': myprint}
    mylocals = {**self.vocabularies, **self.theories, **self.structures}
    mylocals['model_expand'] = model_expand
    exec(main, mybuiltins, mylocals)
Idp.execute = execute





Done = True