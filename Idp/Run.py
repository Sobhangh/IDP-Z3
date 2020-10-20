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
from z3 import Solver, sat, unsat, ModelRef

from .Assignments import Assignment
from .Expression import TRUE, FALSE
from .Parse import *

class Problem(object):
    """ A combination of theory and structure blocks
    """
    def __init__(self, blocks):
        self.definitions = []
        self.clark = {} # {Declaration: Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()
        self.def_constraints = {}

        self._formula = None # the problem expressed in one logic formula
        self.questions = None # occurrences in the _formula

        for b in blocks:
            self.add(b)

    @classmethod
    def make(cls, theories, structures):
        problem = theories if type(theories)=='Problem' else \
                  cls([theories]) if isinstance(theories, Theory) else \
                  cls(theories)

        structures = [] if structures is None else \
                     [structures] if isinstance(structures, Structure) else \
                     structures
        for s in structures:
            problem.add(s)

        return problem

    def add(self, block):
        self._formula = None # need to reapply the definitions
        if type(block) == Structure:
            self.assignments.extend(block.assignments)
        elif type(block) == Theory:
            self.definitions.extend(block.definitions)
            for decl, rule in block.clark.items():
                if decl not in block.clark:
                    self.clark[decl] = rule
                else:
                    new_rule = copy(rule)  # not elegant, but rare
                    new_rule.body = AConjunction.make('∧', [block.clark[decl].body, rule.body])
                    self.clark[decl] = new_rule
            self.constraints.extend(block.constraints)
            self.def_constraints.update(block.def_constraints)
        else:
            assert False, "Cannot add to Problem"

    def formula(self):
        if not self._formula:
            co_constraints = OrderedSet()
            for c in self.constraints:
                c.co_constraints(co_constraints)
            self._formula = AConjunction.make('∧',
                [s for s in self.def_constraints.values()]
                + [a.formula() for a in self.assignments.values() 
                        if a.value is not None]
                + [s for s in self.constraints.values()]
                + [c for c in co_constraints.values()]
                )
        return self._formula

    def translate(self):
        return self.formula().translate()


def model_check(theories, structures=None):
    """ output: "sat", "unsat" or "unknown" 
    """

    problem = Problem.make(theories, structures)
    z3_formula = problem.translate()

    solver = Solver()
    solver.add(z3_formula)
    yield str(solver.check())


def model_expand(theories, structures=None, max=10):
    """ output: a list of Z3 models, ending with a string
    """
    # this is a simplified version of Case.py/full_propagate

    problem = Problem.make(theories, structures)
    z3_formula = problem.translate()

    solver = Solver()
    solver.add(z3_formula)

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


def model_propagate(theories, structures=None):
    """ output: a list of Assignment
    """
    # this is a simplified version of Case.py/full_propagate

    problem = Problem.make(theories, structures)
    z3_formula = problem.translate()
    problem.questions = OrderedSet()
    problem._formula.collect(problem.questions, all_=True)

    solver = Solver()
    solver.add(z3_formula)
    if solver.check() == sat:
        for q in problem.questions:
            solver.check()
            val1 = solver.model().eval(q.reified())
            if str(val1) != str(q.reified()): # if not irrelevant
                solver.push()
                solver.add(Not(q.reified()==val1))
                res2 = solver.check()
                solver.pop()

                if res2 == unsat:
                    if q.type == 'bool':
                        val = TRUE if str(val1) == 'True' else FALSE
                    elif q.type in ['real', 'int'] or type(q.decl.out.decl) == RangeDeclaration:
                        val = NumberConstant(number=str(val1).replace('?', ''))
                    else: # constructor
                        val = q.decl.out.decl.map[str(val1)]
                    assert str(val.translate()) == str(val1).replace('?', ''), str(val.translate()) + " is not the same as " + str(val1)

                    yield Assignment(q, val, Status.CONSEQUENCE, True)
    yield "No more consequences."

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
    mylocals['model_check'] = model_check
    mylocals['model_expand'] = model_expand
    mylocals['model_propagate'] = model_propagate
    mylocals['Problem'] = Problem

    exec(main, mybuiltins, mylocals)
Idp.execute = execute





Done = True