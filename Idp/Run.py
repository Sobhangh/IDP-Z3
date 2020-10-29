"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""

Classes to execute the main block of an IDP program

"""

import types
from z3 import Solver, sat, unsat, unknown, ModelRef

from .Assignments import Assignment
from .Expression import TRUE, FALSE, Variable, AppliedSymbol
from .Parse import *

class Problem(object):
    """ A collection of theory and structure blocks """
    def __init__(self, blocks):
        self.clark = {} # {Declaration: Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()
        self.def_constraints = {}

        self._formula = None # the problem expressed in one logic formula
        self._todo = None # terms to be interpreted by expand, propagate

        for b in blocks:
            self.add(b)

    @classmethod
    def make(cls, theories, structures):
        """ polymorphic creation """
        problem = ( theories if type(theories)=='Problem' else 
                    cls([theories]) if isinstance(theories, Theory) else 
                    cls(theories) )

        structures = ( [] if structures is None else
                       [structures] if isinstance(structures, Structure) else
                       structures )
        for s in structures:
            problem.add(s)

        return problem

    def add(self, block):
        # TODO reprocess the definitions 
        self._formula = None # need to reapply the definitions
        if type(block) == Structure:
            self.assignments.extend(block.assignments)
        elif type(block) in [Theory, Problem]:
            for decl, rule in block.clark.items():
                new_rule = copy(rule)
                if decl in self.clark:
                    new_rule.body = AConjunction.make('∧', 
                        [self.clark[decl].body, new_rule.body])
                self.clark[decl] = new_rule
            self.constraints.extend(v.copy() for v in block.constraints)
            self.def_constraints.update(
                {k:v.copy() for k,v in block.def_constraints.items()})
            self.assignments.extend(block.assignments)
        else:
            assert False, "Cannot add to Problem"

    def formula(self):
        """ the formula encoding the knowledge base """
        if not self._formula:
            co_constraints = OrderedSet()
            for c in self.constraints:
                c.interpret(self)
                c.co_constraints(co_constraints)
            self._formula = AConjunction.make('∧',
                [a.formula() for a in self.assignments.values() 
                        if a.value is not None]
                + [s for s in self.constraints]
                + [c for c in co_constraints]
                + [s for s in self.def_constraints.values()]
                )

            self._todo = OrderedSet(a.sentence 
                for a in self.assignments.values() 
                if a.value is None
                and type(a.sentence) in [AppliedSymbol, Variable])
        return self._formula

    def simplify(self):
        """ simplify constraints using known assignments """
        # annotate self.constraints with questions
        for e in self.constraints:
            questions = OrderedSet()
            e.collect(questions, all_=True)
            e.questions = questions

        for ass in self.assignments.values():
            old, new = ass.sentence, ass.value
            if new is not None:
                # simplify constraints
                new_constraints: List[Expression] = []
                for constraint in self.constraints:
                    if old in constraint.questions: # for performance
                        self._formula = None # invalidates the formula
                        consequences = []
                        new_constraint = constraint.substitute(old, new, self.assignments, consequences)
                        del constraint.questions[old.code]
                        new_constraint.questions = constraint.questions
                        new_constraints.append(new_constraint)
                    else:
                        new_constraints.append(constraint)
                self.constraints = new_constraints
        return self

    def translate(self):
        """ translates to Z3 """
        return self.formula().translate()


def str_to_IDP(atom, val_string):
    if atom.type == 'bool':
        assert val_string in ['True', 'False'], \
            f"{atom.annotations['reading']} is not defined, and assumed false"
        out = ( TRUE if val_string == 'True' else 
               FALSE)
    elif ( atom.type in ['real', 'int']
    or type(atom.decl.out.decl) == RangeDeclaration): # could be a fraction
        out = NumberConstant(number=str(eval(val_string.replace('?', ''))))
    else: # constructor
        assert atom.decl.arity == 0, 'constant expected'
        out = atom.decl.out.decl.map[val_string]
    return out


def model_check(theories, structures=None):
    """ output: "sat", "unsat" or "unknown" """

    problem = Problem.make(theories, structures)
    z3_formula = problem.translate()

    solver = Solver()
    solver.add(z3_formula)
    yield str(solver.check())


def model_expand(theories, structures=None, max=10):
    """ output: a list of Z3 models, ending with a string """
    # this is a simplified version of Case.py/full_propagate

    problem = Problem.make(theories, structures)
    z3_formula = problem.translate()
    todo = problem._todo

    solver = Solver()
    solver.add(z3_formula)

    count = 0
    while count<max or max<=0:

        if solver.check() == sat:
            count += 1
            model = solver.model()
            yield model

            # exclude this model
            different = []
            for q in todo:
                different.append(q.translate() != model.eval(q.translate()))
            solver.add(Or(different))
        else:
            break

    if solver.check() == sat:
        yield f"{NEWL}More models are available."
    elif 0 < count:
        yield f"{NEWL}No more models."
    else:
        yield "No models."


def model_propagate(theories, structures=None):
    """ output: a list of Assignment """
    # this is a simplified version of Case.py/full_propagate

    problem = Problem.make(theories, structures)
    z3_formula = problem.translate()
    todo = problem._todo

    solver = Solver()
    solver.add(z3_formula)
    if solver.check() == sat:
        for q in todo:
            solver.push() # in case todo contains complex formula
            solver.add(q.reified()==q.translate())
            res1 = solver.check()
            if res1 == sat:
                val1 = solver.model().eval(q.reified())
                if str(val1) != str(q.reified()): # if not irrelevant
                    solver.push()
                    solver.add(Not(q.reified()==val1))
                    res2 = solver.check()
                    solver.pop()

                    if res2 == unsat:
                        val = str_to_IDP(q, str(val1))

                        yield problem.assignments.assert_(q, val,
                            Status.CONSEQUENCE, True)
                    elif res2 == unknown:
                        res1 = unknown
            solver.pop()
            if res1 == unknown:
                # yield(f"Unknown: {str(q)}")
                solver = Solver() # restart the solver
                solver.add(z3_formula)

        yield "No more consequences."
    else:
        yield "Not satisfiable."
        yield str(z3_formula)



def myprint(x=""):
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
    """ Execute the IDP program """
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