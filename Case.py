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

from Idp.Expression import Brackets, AUnary, TRUE, FALSE, AppliedSymbol, Variable, AConjunction, ADisjunction, AComparison
from Solver import mk_solver
from Structure_ import json_to_literals, Assignment, Status, str_to_IDP
from utils import *

# Types
from Idp import Idp, SymbolDeclaration
from Idp.Expression import Expression
from typing import Any, Dict, List, Union, Tuple, cast
from z3.z3 import BoolRef

class Case:
    """
    Contains a state of problem solving
    """
    cache: Dict[Tuple[Idp, str, List[str]], 'Case'] = {}

    def __init__(self, idp: Idp, jsonstr: str, expanded: List[str]):

        self.idp = idp # Idp vocabulary and theory
        self.given = json_to_literals(idp, jsonstr) # {atom : assignment} from the user interface
        self.expanded_symbols = set(expanded)

        # initialisation

        # Lines in the GUI
        self.GUILines = {**idp.vocabulary.terms, **idp.subtences} # DEPRECATED use self.assignments instead # {atom_string: Expression}
        self.typeConstraints = self.idp.vocabulary
        self.definitions = self.idp.theory.definitions # [Definition]
        self.simplified: List[Expression] = []

        self.assignments: Dict[str, Assignment] = {} # atoms + given, with simplified formula and truth value

        if DEBUG: invariant = ".".join(str(e) for e in self.idp.theory.constraints)

        for GuiLine in self.GUILines.values():
            GuiLine.is_visible = type(GuiLine) in [AppliedSymbol, Variable] \
                or (type(GuiLine)==AComparison and GuiLine.is_assignment) \
                or any(s in self.expanded_symbols for s in GuiLine.unknown_symbols().keys())

        # initialize .assignments
        self.assignments = {s.code : Assignment(s.copy(), None, Status.UNKNOWN) for s in self.idp.subtences.values()}
        self.assignments.update({ atom.code : ass for atom, ass in self.given.items() })

        # find immediate universals
        for i, c in enumerate(self.idp.theory.constraints):
            c = c.copy()
            u = c.implicants()
            if u:
                for sentence, truth in u:
                    ass = Assignment(sentence, truth, Status.UNKNOWN)
                    status = Status.ENV_UNIV if not ass.sentence.has_environmental(False) else Status.UNIVERSAL
                    ass.update(None, None, status, self)
            self.simplified.append(c)

        self.assignments.update({ k : Assignment(t.copy(), None, Status.UNKNOWN) 
            for k, t in idp.vocabulary.terms.items()
            if k not in self.assignments })

        if idp.decision: # if there is a decision vocabulary
            # first, consider only environmental facts and theory (exclude any statement containing decisions)
            self.full_propagate(all_=False)
        self.full_propagate(all_=True) # now consider all facts and theories

        # determine relevant assignemnts
        relevant_symbols, relevant_subtences = self.get_relevant_subtences(all_=True)

        for k, l in self.assignments.items():
            symbols = list(l.sentence.unknown_symbols().keys())
            has_relevant_symbol = any(s in relevant_symbols for s in symbols)
            if k in relevant_subtences and symbols and has_relevant_symbol:
                l.relevant = True
        if DEBUG: assert invariant == ".".join(str(e) for e in self.idp.theory.constraints)

    def __str__(self) -> str:
        return (f"Type:        {indented}{indented.join(repr(d) for d in self.typeConstraints.translate(self.idp))}{nl}"
                f"Definitions: {indented}{indented.join(repr(d) for d in self.definitions)}{nl}"
                f"Universals:  {indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.UNIVERSAL, Status.ENV_UNIV])}{nl}"
                f"Consequences:{indented}{indented.join(repr(c) for c in self.assignments.values() if c.status in [Status.CONSEQUENCE, Status.ENV_CONSQ])}{nl}"
                f"Simplified:  {indented}{indented.join(str(c)  for c in self.simplified)}{nl}"
                f"Irrelevant:  {indented}{indented.join(repr(c) for c in self.assignments.values() if not c.relevant)}{nl}"
        )
        
    def get_relevant_subtences(self, all_: bool) -> Tuple[Dict[str, SymbolDeclaration], Dict[str, Expression]]:
        #TODO performance.  This method is called many times !  use expr.contains(expr, symbols)
        constraints = ( self.simplified
            + list(self.idp.goal.subtences().values()))

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
        return (symbols, relevant_subtences)

    def full_propagate(self, all_: bool) -> None:
        CONSQ = Status.CONSEQUENCE if all_ else Status.ENV_CONSQ

        # simplify all using given and universals
        to_propagate = list(l for l in self.assignments.values() 
            if l.truth is not None)
        self.propagate(to_propagate, all_)

        Log(f"{nl}Z3 propagation ********************************")

        theory = self.translate(all_)
        solver, _, _ = mk_solver(theory, {})
        result = solver.check()
        if result == sat:
            todo = self.assignments.keys()

            # determine consequences on expanded symbols only (for speed)
            for key in todo:
                l = self.assignments[key]
                if ( l.truth is None
                and (all_ or not l.sentence.has_environmental(False))
                # and key in self.get_relevant_subtences(all_) 
                and self.GUILines[key].is_visible):
                    atom = l.sentence
                    solver.push()
                    solver.add(atom.reified()==atom.translate())
                    res1 = solver.check()
                    if res1 == sat:
                        val1 = solver.model().eval(atom.reified())
                        if str(val1) != str(atom.reified()): # if not irrelevant
                        
                            val = str_to_IDP(self.idp, str(val1))
                            assert val.translate() == val1, str(val) + " is not the same as " + str(val1)

                            solver.push()
                            solver.add(Not(atom.reified()==val1))
                            res2 = solver.check()
                            solver.pop()

                            if res2 == unsat:
                                ass = l.update(atom, val, CONSQ, self)
                                #TODO ass.relevant = True
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

    def propagate(self, to_propagate: List[Assignment], all_: bool) -> None:
        CONSQ = Status.CONSEQUENCE if all_ else Status.ENV_CONSQ
        while to_propagate:
            ass = to_propagate.pop(0)
            old, new = ass.as_substitution(self)

            if new is not None:
                # simplify constraints and propagate consequences
                new_simplified: List[Expression] = []
                for constraint in self.simplified:
                    consequences = []
                    new_constraint = constraint.substitute(old, new, consequences)
                    consequences.extend(new_constraint.implicants())
                    if consequences:
                        for sentence, truth in consequences:
                            if sentence.code in self.assignments:
                                old_ass = self.assignments[sentence.code]
                                if old_ass.truth is None:
                                    if (all_ or not constraint.has_environmental(False)):
                                        new_ass = old_ass.update(sentence, truth, CONSQ, self)
                                        to_propagate.append(new_ass)
                                        new_constraint = new_constraint.substitute(sentence, truth)
                                elif old_ass.truth != truth:
                                    # test: theory{ x=4. x=5. }
                                    self.simplified = cast(List[Expression], [FALSE]) # inconsistent !
                                    return
                            else:
                                print("not found", str(sentence))
                    new_simplified.append(new_constraint)

                self.simplified = new_simplified

                # simplify assignments
                # e.g. 'Sides=4' becomes false when Sides becomes 3
                for old_ass in self.assignments.values():
                    before = str(old_ass.sentence)
                    new_constraint = old_ass.sentence.substitute(old, new)
                    if before != str(new_constraint) \
                    and (all_ or not new_constraint.has_environmental(False)): # is purely environmental
                        if new_constraint.code in self.assignments \
                        and self.assignments[new_constraint.code].truth is not None: # e.g. O(M) becomes O(e2)
                            new_constraint = self.assignments[new_constraint.code].sentence
                        if new_constraint.value is None: # not reduced to ground
                            old_ass.update(new_constraint, None, None, self)
                        elif old_ass.truth is not None: # has a value already
                            if not old_ass.truth == new_constraint.value: # different !
                                self.simplified = cast(List[Expression], [FALSE]) # inconsistent
                                return
                            else: # no change
                                pass
                        else: # accept new value
                            new_ass = old_ass.update(new_constraint, 
                                new_constraint.value, CONSQ, self)
                            to_propagate.append(new_ass)
                            

    def translate(self, all_: bool = True) -> BoolRef:
        self.translated = And(
            self.typeConstraints.translate(self.idp)
            + sum((d.translate(self.idp) for d in self.definitions), [])
            + [l.translate() for k, l in self.assignments.items() 
                    if l.truth is not None and (all_ or not l.sentence.has_environmental(False))]
            + [c.translate() for c in self.simplified
                    if all_ or not c.has_environmental(False)]
            )
        return self.translated

def make_case(idp: Idp, jsonstr: str, expanded: List[str]) -> Case:

        if (idp, jsonstr, expanded) in Case.cache:
            return Case.cache[(idp, jsonstr, expanded)]

        case = Case(idp, jsonstr, expanded)

        if 100<len(Case.cache):
            # remove oldest entry, to prevent memory overflow
            Case.cache = {k:v for k,v in list(Case.cache.items())[1:]}
        Case.cache[(idp, jsonstr, expanded)] = case
        return case
