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
from typing import Iterable
from z3 import Solver, sat, unsat, unknown, Optimize

from .Assignments import Assignment
from .Expression import TRUE, FALSE, Variable, AppliedSymbol
from .Parse import *

class Problem(object):
    """ A collection of theory and structure blocks """
    def __init__(self, *blocks):
        self.clark = {} # {Declaration: Rule}
        self.constraints = OrderedSet()
        self.assignments = Assignments()
        self.def_constraints = {}
        self.interpretations = {}

        self._formula = None # the problem expressed in one logic formula
        self.co_constraints = None # Constraints attached to subformula. (see also docs/zettlr/Glossary.md)
        self.questions = None

        for b in blocks:
            self.add(b)

    @classmethod
    def make(cls, theories, structures):
        """ polymorphic creation """
        problem = ( theories if type(theories)=='Problem' else 
                    cls(*theories) if isinstance(theories, Iterable) else 
                    cls(theories))

        structures = ( [] if structures is None else
                       structures if isinstance(structures, Iterable) else
                       [structures] )
        for s in structures:
            problem.add(s)

        return problem

    def copy(self):
        out = copy(self)
        out.assignments = self.assignments.copy()
        out.constraints = [c.copy() for c in self.constraints]
        out.def_constraints = self.def_constraints.copy()
        # copy() is called before making substitutions => invalidate derived fields
        out._formula = None
        out.co_constraints, out.questions = None, None
        return out

    def add(self, block):
        self._formula = None # need to reapply the definitions
        self.interpretations.update(block.interpretations) #TODO detect conflicts
        if type(block) == Structure:
            self.assignments.extend(block.assignments)
        elif isinstance(block, Theory) or isinstance(block, Problem):
            self.co_constraints, self.questions = None, None
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
        return self

    def _interpret(self):
        """ re-apply the definitions to the constraints """
        if self.questions is None:
            self.co_constraints, self.questions = OrderedSet(), OrderedSet()
            for c in self.constraints:
                c.interpret(self)
                c.co_constraints(self.co_constraints)
                c.collect(self.questions, all_=False)
            for s in list(self.questions.values()):
                if s.is_reified():
                    self.assignments.assert_(s, None, Status.UNKNOWN, False)

    def formula(self):
        """ the formula encoding the knowledge base """
        if not self._formula:
            self._interpret()
            self._formula = AConjunction.make('∧',
                [a.formula() for a in self.assignments.values() 
                        if a.value is not None]
                + [s for s in self.constraints]
                + [c for c in self.co_constraints]
                + [s for s in self.def_constraints.values()]
                + [TRUE]  # so that it is not empty
                )
        return self._formula

    def _todo(self, extended):
        return OrderedSet(a.sentence 
            for a in self.assignments.values() 
            if a.value is None
            and a.symbol_decl is not None
            and (not a.sentence.is_reified() or extended))

    def _from_model(self, solver, todo, complete, extended):
        """ returns Assignments from model in solver """
        ass = self.assignments.copy()
        for q in todo:
            val1 = solver.model().eval(q.translate(), model_completion=complete)
            if str(val1) != str(q.translate()): # otherwise, unknown
                val = str_to_IDP(q, str(val1))
                ass.assert_(q, val, Status.EXPANDED, None)
        return ass

    def expand(self, max=10, complete=False, extended=False):
        """ output: a list of Assignments, ending with a string """
        z3_formula = self.formula().translate()
        todo = self._todo(extended)

        solver = Solver()
        solver.add(z3_formula)

        count = 0
        while count<max or max<=0:

            if solver.check() == sat:
                count += 1
                model = solver.model()
                ass = self._from_model(solver, todo, complete, extended)
                yield ass 

                # exclude this model
                different = []
                for a in ass.values():
                    if a.status == Status.EXPANDED:
                        q = a.sentence
                        different.append(q.translate() != a.value.translate())
                solver.add(Or(different))
            else:
                break

        if solver.check() == sat:
            yield f"{NEWL}More models are available."
        elif 0 < count:
            yield f"{NEWL}No more models."
        else:
            yield "No models."

    def optimize(self, term, minimize=True, complete=False, extended=False):
        assert term in self.assignments, "Internal error"
        s = self.assignments[term].sentence.translate()

        solver = Optimize()
        solver.add(self.formula().translate())
        if minimize:
            solver.minimize(s)
        else:
            solver.maximize(s)
        solver.check()

        # deal with strict inequalities, e.g. min(0<x)
        solver.push()
        for i in range(0,10):
            val = solver.model().eval(s)
            if minimize:
                solver.add(s < val)
            else:
                solver.add(val < s)
            if solver.check()!=sat:
                solver.pop() # get the last good one
                solver.check()
                break  
        self.assignments = self._from_model(solver, self._todo(extended), 
            complete, extended)
        return self 


    def symbolic_propagate(self, tag=Status.UNIVERSAL):
        """ determine the immediate consequences of the constraints """
        self._interpret()
        for c in self.constraints:
            # determine consequences, including from co-constraints
            consequences = []
            new_constraint = c.substitute(TRUE, TRUE, 
                self.assignments, consequences)
            consequences.extend(new_constraint.implicants(self.assignments))
            if consequences:
                for sentence, value in consequences:
                    self.assignments.assert_(sentence, value, tag, False)
        return self

    def _propagate(self, tag, extended):
        z3_formula = self.formula().translate()
        todo = self._todo(extended)

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
                            yield self.assignments.assert_(q, val, tag, True)
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

    def propagate(self, tag=Status.CONSEQUENCE, extended=False):
        """ determine all the consequences of the constraints """
        out = list(self._propagate(tag, extended))
        assert out[0] != "Not satisfiable.", "Not satisfiable."
        return self

    def simplify(self):
        """ simplify constraints using known assignments """
        self._interpret()

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
                        new_constraint = constraint.substitute(old, new, 
                            self.assignments, consequences)
                        del constraint.questions[old.code]
                        new_constraint.questions = constraint.questions
                        new_constraints.append(new_constraint)
                    else:
                        new_constraints.append(constraint)
                self.constraints = new_constraints
        return self


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
        out = atom.decl.out.decl.map[val_string]
    return out


def model_check(theories, structures=None):
    """ output: "sat", "unsat" or "unknown" """

    problem = Problem.make(theories, structures)
    z3_formula = problem.formula().translate()

    solver = Solver()
    solver.add(z3_formula)
    yield str(solver.check())


def model_expand(theories, structures=None, max=10, complete=False, 
        extended=False):
    """ output: a list of Assignments, ending with a string """
    problem = Problem.make(theories, structures)
    yield from problem.expand(max=max, complete=complete, extended=extended)

def model_propagate(theories, structures=None):
    """ output: a list of Assignment """
    problem = Problem.make(theories, structures)
    yield from problem._propagate(tag=Status.CONSEQUENCE, extended=False)

def myprint(x=""):
    if isinstance(x, types.GeneratorType):
        for i, xi in enumerate(x):
            if isinstance(xi, Assignments):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                print(xi)
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