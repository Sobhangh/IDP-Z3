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
from z3 import And, Not, sat, unsat, unknown, is_true

from Idp.Expression import Brackets, AUnary, TRUE, FALSE, AppliedSymbol, Variable, AConjunction, ADisjunction
from Solver import mk_solver
from Structure_ import json_to_literals, Equality, Assignment, Term, Status
from utils import *

class Case:
    """
    Contains a state of problem solving
    """
    cache = {}

    def __init__(self, idp, jsonstr, expanded):

        self.idp = idp # Idp vocabulary and theory
        self.given = json_to_literals(idp, jsonstr) # {Assignment : atomZ3} from the user interface
        self.expanded_symbols = set(expanded)

        # initialisation

        # Lines in the GUI
        self.GUILines = {**idp.vocabulary.terms, **idp.theory.subtences} # DEPRECATED use self.assignments instead # {atom_string: Expression}
        self.typeConstraints = self.idp.vocabulary
        self.definitions = self.idp.theory.definitions # [Definition]
        self.simplified =  [] # [Expression]

        self.assignments = {} # {sentence.code: Assignment}, atoms + given, with simplified formula and truth value

        if DEBUG: invariant = ".".join(str(e) for e in self.idp.theory.constraints)

        for GuiLine in self.GUILines.values():
            GuiLine.is_visible = type(GuiLine) in [AppliedSymbol, Variable] \
                or any(s in self.expanded_symbols for s in GuiLine.unknown_symbols().keys())

        # initialize .assignments
        self.assignments = {s.code : Assignment(s, None, Status.UNKNOWN) for s in self.idp.theory.subtences.values()}
        self.assignments.update({ l.sentence.code : l for l in self.given })

        # find immediate universals
        for i, c in enumerate(self.idp.theory.constraints):
            u = self.expr_to_literal(c)
            if u:
                for l in u:
                    l.update(None, None, Status.UNIVERSAL, self)
            else:
                self.simplified.append(c)

        self.assignments.update({ k : Term(Equality(t, None), None, Status.UNKNOWN) 
            for k, t in idp.vocabulary.terms.items()
            if k not in self.assignments })

        if idp.decision: # if there is a decision vocabulary
            # first, consider only environmental facts and theory (exclude any statement containing decisions)
            self.full_propagate(all_=False)
        self.full_propagate(all_=True) # now consider all facts and theories

        if DEBUG: assert invariant == ".".join(str(e) for e in self.idp.theory.constraints)

    def __str__(self):
        return (f"Type:        {indented}{indented.join(repr(d) for d in self.typeConstraints.translated)}{nl}"
                f"Definitions: {indented}{indented.join(repr(d) for d in self.definitions)}{nl}"
                f"Universals:  {indented}{indented.join(repr(c) for c in self.assignments.values() if c.status == Status.UNIVERSAL)}{nl}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.CONSEQUENCE, Status.ENV_CONSQ])}{nl}"
                f"Simplified:  {indented}{indented.join(str(c)  for c in self.simplified)}{nl}"
                f"Irrelevant:  {indented}{indented.join(str(c.sentence) for c in self.assignments.values() if not c.relevant and type(c) != Term)}{nl}"
        )
        
    def get_relevant_subtences(self, all_):
        #TODO performance.  This method is called many times !  use expr.contains(expr, symbols)
        if self.definitions: #TODO definitions ?
            return {}
        constraints = ( self.simplified
            + [l.sentence for k, l in self.assignments.items() 
                    if l.truth is not None and (all_ or l.is_environmental) 
                    and not type(l) == Term])

        # determine relevant symbols (including defined ones)
        symbols = mergeDicts( e.unknown_symbols() for e in constraints )
        if self.idp.goal.decl is not None:
            symbols.update({self.idp.goal.decl.name : self.idp.goal.decl})

        # remove irrelevant domain conditions
        self.simplified = list(filter(lambda e: e.if_symbol is None or e.if_symbol in symbols
                                     , self.simplified))

        # determine relevant subtences
        relevant_subtences = mergeDicts( e.subtences() for e in constraints )
        relevant_subtences.update(mergeDicts(s.instances for s in symbols.values()))
        return relevant_subtences

    def full_propagate(self, all_):
        CONSQ = Status.CONSEQUENCE if all_ else Status.ENV_CONSQ

        # simplify all using given and universals
        to_propagate = list(l for l in self.assignments.values() 
            if l.truth is not None and (all_ or l.is_environmental))
        self.propagate(to_propagate, all_)

        # determine relevant symbols
        if all_:
            relevant_subtences = self.get_relevant_subtences(all_=True)

            for k, l in self.assignments.items():
                if k in relevant_subtences or self.definitions: #TODO support for definitions
                    l.relevant = True

        solver, _, _ = mk_solver(self.translate(all_), {})
        result = solver.check()
        if result == sat:
            todo = self.assignments.keys()

            # determine consequences on expanded symbols only (for speed)
            for key in todo:
                l = self.assignments[key]
                if ( l.truth is None
                and (all_ or l.is_environmental)
                # and key in self.get_relevant_subtences(all_) 
                and self.GUILines[key].is_visible):
                    atom = l.sentence
                    solver.push()
                    solver.add(atom.reified()==atom.translate())
                    res1 = solver.check()
                    if res1 == sat:
                        val1 = solver.model().eval(atom.reified())
                        if str(val1) != str(atom.reified()): # if not irrelevant
                            solver.push()
                            solver.add(Not(atom.reified()==val1))
                            res2 = solver.check()
                            solver.pop()

                            if res2 == unsat:
                                if type(l) == Term:
                                    # need to convert Term into Assignment
                                    if atom.variable.decl.out.code == 'bool':
                                        ass = Assignment(atom.variable, is_true(val1), CONSQ)
                                    else:
                                        ass = Assignment(Equality(atom.variable, val1), True, CONSQ)
                                    ass.relevant = True
                                    self.assignments[key] = ass
                                else:
                                    ass = l.update(None, is_true(val1), CONSQ, self)
                                self.propagate([ass], all_)
                            elif res2 == unknown:
                                res1 = unknown
                    solver.pop()
                    if res1 == unknown: # restart solver
                        solver, _, _ = mk_solver(self.translate(all_), {})
                        result = solver.check()
        elif result == unsat:
            print(self.translate(all_))
            raise Exception("Not satisfiable !")

    def propagate(self, to_propagate, all_):
        CONSQ = Status.CONSEQUENCE if all_ else Status.ENV_CONSQ
        while to_propagate:
            ass = to_propagate.pop(0)
            old, new = ass.as_substitution(self)

            if new is not None:
                # simplify constraints
                l1 = []
                for constraint in self.simplified:
                    new_constraint = constraint.substitute(old, new)
                    consequences = self.expr_to_literal(new_constraint)
                    if consequences:
                        for consequence in consequences:
                            assignment = self.assignments[consequence.sentence.code]
                            if assignment.truth is None:
                                out = assignment.update(None, consequence.truth, CONSQ, self)
                                if (all_ or assignment.is_environmental):
                                    to_propagate.append(out)
                            elif assignment.truth != consequence.truth:
                                l1.append(FALSE) # inconsistent !
                    elif not new_constraint == TRUE:
                        l1.append(new_constraint)

                self.simplified = l1

                # simplify assignments
                for assignment in self.assignments.values():
                    if assignment != ass and (all_ or assignment.is_environmental):
                        new_constraint = assignment.sentence.substitute(old, new)
                        if new_constraint != assignment.sentence: # changed !
                            if type(assignment) == Term:
                                out = assignment.assign(new_constraint.value, self, CONSQ)
                                to_propagate.append(out)
                            elif new_constraint in [TRUE, FALSE]:
                                if assignment.truth is None:
                                    out = assignment.update(new_constraint, (new_constraint == TRUE), CONSQ, self)
                                    to_propagate.append(out)
                                elif (new_constraint==TRUE  and not assignment.truth) \
                                or   (new_constraint==FALSE and     assignment.truth):
                                    self.simplified = [FALSE] # inconsistent
                                else:
                                    pass # no change
                            else:
                                assignment.update(new_constraint, None, None, self)


    def expr_to_literal(self, expr, truth=True):
        # returns an assignment for the matching atom in self.GUILines, or []
        if expr.code in self.GUILines: # found it !
            return [Assignment(expr, truth, Status.UNKNOWN)]
        if isinstance(expr, Brackets):
            return self.expr_to_literal(expr.sub_exprs[0], truth)
        if isinstance(expr, AUnary) and expr.operator == '~':
            return self.expr_to_literal(expr.sub_exprs[0], not truth )
        if truth and isinstance(expr, AConjunction):
            return [l for e in expr.sub_exprs for l in self.expr_to_literal(e, truth)]
        if not truth and isinstance(expr, ADisjunction):
            return [l for e in expr.sub_exprs for l in self.expr_to_literal(e, truth)]
        return []

    def translate(self, all_=True):
        self.translated = And(
            self.typeConstraints.translated
            + sum((d.translate(self.idp) for d in self.definitions), [])
            + [l.translate() for k, l in self.assignments.items() 
                    if l.truth is not None and (all_ or l.is_environmental) 
                    and not type(l) == Term]
            + [c.translate() for c in self.simplified]
            )
        return self.translated

def make_case(idp, jsonstr, expanded):

        if (idp, jsonstr, expanded) in Case.cache:
            return Case.cache[(idp, jsonstr, expanded)]

        case = Case(idp, jsonstr, expanded)

        if 100<len(Case.cache):
            # remove oldest entry, to prevent memory overflow
            Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
        Case.cache[(idp, jsonstr, expanded)] = case
        return case