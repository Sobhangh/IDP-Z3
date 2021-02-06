# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module contains the logic for inferences
that are specific for the Interactive Consultant.
"""

from itertools import chain
import time
from z3 import Solver, Implies,  Not

from idp_solver.Expression import AComparison, AUnary, AppliedSymbol, TRUE
from idp_solver.Assignments import Status, Assignment
from idp_solver.utils import OrderedSet, BOOL
from .IO import Output


# def get_relevant_subtences(self) -> Tuple[Dict[str, SymbolDeclaration], Dict[str, Expression]]:
#     """ causal interpretation of relevance """
#     #TODO performance.  This method is called many times !  use expr.contains(expr, symbols)
#     constraints = ( self.constraints )

#     # determine relevant symbols (including defined ones)
#     relevant_symbols = mergeDicts( e.unknown_symbols() for e in constraints )

#     # remove irrelevant domain conditions
#     self.constraints = list(filter(lambda e: e.is_type_constraint_for is None or e.is_type_constraint_for in relevant_symbols
#                                  , self.constraints))

#     # determine relevant subtences
#     relevant_subtences = mergeDicts( e.subtences() for e in constraints )
#     relevant_subtences.update(mergeDicts(s.instances for s in relevant_symbols.values()))

#     for k, l in self.assignments.items():
#         symbols = list(l.sentence.unknown_symbols().keys())
#         has_relevant_symbol = any(s in relevant_symbols for s in symbols)
#         if k in relevant_subtences and symbols and has_relevant_symbol:
#             l.relevant = True

def get_relevant_subtences(self):
    """
    sets 'relevant in self.assignments
    sets rank of symbols in self.relevant_symbols
    removes irrelevant constraints in self.constraints
    """
    # self is a State
    for a in self.assignments.values():
        a.relevant = False

    # collect (co-)constraints
    constraints = OrderedSet()
    for constraint in self.constraints:
        constraints.append(constraint)
        constraint.co_constraints(constraints)


    # initialize reachable with relevant, if any
    reachable = OrderedSet()
    for constraint in constraints:
        if type(constraint) == AppliedSymbol and \
           constraint.name == '__relevant':
            for e in constraint.sub_exprs:
                assert e.code in self.assignments, \
                    f"Invalid expression in relevant: {e.code}"
                reachable.append(e)

    # analyse given information
    given, hasGiven = OrderedSet(), False
    for q in self.assignments.values():
        if q.status == Status.GIVEN:
            hasGiven = True
            if not q.sentence.has_decision():
                given.append(q.sentence)

    # constraints have set of questions in self.assignments
    # set constraint.relevant, constraint.questions
    for constraint in constraints:
        constraint.relevant = False
        constraint.questions = OrderedSet()
        constraint.collect(constraint.questions,
                           all_=True, co_constraints=False)

        # add goals in constraint.original to constraint.questions
        # only keep questions in self.assignments
        qs = OrderedSet()
        constraint.original.collect(qs, all_=True, co_constraints=False)
        for q in qs:
            if q in reachable:  # a goal
                constraint.questions.append(q)
        constraint.questions = OrderedSet([q for q in constraint.questions
                                           if q.code in self.assignments])

    # nothing relevant --> make every question in a constraint relevant
    if len(reachable) == 0:
        for constraint in constraints:
            if constraint.is_type_constraint_for is None:
                for q in constraint.questions:
                    reachable.append(q)

    # find relevant symbols by depth-first propagation
    # relevants, rank = {}, 1
    # def dfs(question):
    #     nonlocal relevants, rank
    #     for constraint in constraints:
    #         # consider constraint not yet considered
    #         if ( not constraint.relevant
    #         # containing the question
    #         and question in constraint.questions):
    #             constraint.relevant = True
    #             for q in constraint.questions:
    #                 self.assignments[q.code].relevant = True
    #                 for s in q.unknown_symbols(co_constraints=False):
    #                     if s not in relevants:
    #                         relevants[s] = rank
    #                         rank = rank+1
    #                 if q.code != question.code \
    #                 and q.type == BOOL\
    #                 and not q in given:
    #                     print("==>", q)
    #                     reachable.add(q)
    #                     dfs(q)
    # for question in list(reachable.values()):
    #     dfs(question)

    # find relevant symbols by breadth-first propagation
    # input: reachable, given, constraints
    # output: self.assignments[].relevant, constraints[].relevant, relevants[].rank
    relevants = {}  # Dict[string: int]
    to_add, rank = reachable, 1
    while to_add:
        for q in to_add:
            self.assignments[q.code].relevant = True
            for s in q.unknown_symbols(co_constraints=False):
                if s not in relevants:
                    relevants[s] = rank
            if q not in given:
                reachable.append(q)

        to_add, rank = OrderedSet(), 2  # or rank+1
        for constraint in constraints:
            # consider constraint not yet considered
            if (not constraint.relevant
                # and with a question that is reachable but not given
                and any(q in reachable and q not in given
                        for q in constraint.questions)):
                constraint.relevant = True
                to_add.extend(constraint.questions)
    if not hasGiven or self.idp.display.moveSymbols:
        self.relevant_symbols = relevants


def explain(state, question):
    out = Output(state, state.given)

    negated = question.replace('~', '¬').startswith('¬')
    question = question[1:] if negated else question
    if question in state.assignments:
        to_explain = state.assignments[question].sentence

        # rules used in justification
        if to_explain.type != BOOL:  # recalculate numeric value
            val = state.assignments[question].value
            if val is None:  # can't explain an expanded value
                return out.m
            to_explain = AComparison.make("=", [to_explain, val])
        if negated:
            to_explain = AUnary.make('¬', to_explain)

        s = Solver()
        s.set(':core.minimize', True)
        ps = {}  # {reified: constraint}

        for ass in state.assignments.values():
            if ass.status in [Status.GIVEN, Status.STRUCTURE,
                              Status.UNIVERSAL]:
                p = ass.translate()
                ps[p] = ass
                #TODO use assert_and_track ?
                s.add(Implies(p, ass.translate()))
        todo = chain(state.constraints, state.def_constraints.values())
        for constraint in todo:
            p = constraint.reified()
            constraint.original = constraint.original.interpret(state)
            ps[p] = constraint.original.translate()
            s.add(Implies(p, constraint.original.translate()))

        s.add(Not(to_explain.translate()))
        s.check(list(ps.keys()))
        unsatcore = s.unsat_core()

        if unsatcore:
            for a1 in state.assignments.values():
                if a1.status in [Status.GIVEN, Status.STRUCTURE,
                                 Status.UNIVERSAL]:
                    for a2 in unsatcore:
                        if type(ps[a2]) == Assignment \
                        and a1.sentence.same_as(ps[a2].sentence):  #TODO we might miss some equality
                            out.addAtom(a1.sentence, a1.value, a1.status)

            # remove irrelevant atoms
            for symb, dictionary in out.m.items():
                out.m[symb] = {k: v for k, v in dictionary.items()
                               if type(v) == dict and v['status'] in
                               ['GIVEN', 'STRUCTURE', 'UNIVERSAL']
                               and v.get('value', '') != ''}
            out.m = {k: v for k, v in out.m.items() if v}

            out.m["*laws*"] = []
            for a1 in chain(state.def_constraints.values(), state.constraints):
                #TODO find the rule
                for a2 in unsatcore:
                    if str(a1.original.translate()) == str(ps[a2]):
                        out.m["*laws*"].append(a1.annotations['reading'])
    return out.m

def abstract(state, given_json):
    timeout, max_rows = 20, 50
    max_time = time.time()+timeout
    models = state.decision_table(goal_string="", timeout=timeout, max_rows=max_rows,
                        first_hit=False)

    # detect symbols with assignments
    table, active_symbol = {}, {}
    for i, model in enumerate(models):
        for ass in model:
            if (ass.sentence != TRUE
            and ass.symbol_decl is not None):
                active_symbol[ass.symbol_decl.name] = True
                if (ass.symbol_decl.name not in table):
                    table[ass.symbol_decl.name]= [ [] for i in range(len(models))]
                table[ass.symbol_decl.name][i].append(ass)

    # build table of models
    out = {} # {category : [Assignment]}

    out["universal"] = list(l for l in state.assignments.values()
                            if l.status == Status.UNIVERSAL)
    out["given"    ] = list(l for l in state.assignments.values()
                            if l.status == Status.GIVEN)
    out["fixed"    ] = list(l for l in state.assignments.values()
                            if l.status in [Status.ENV_CONSQ, Status.CONSEQUENCE])
    out["irrelevant"]= list(l for l in state.assignments.values()
                            if l.status not in [Status.ENV_CONSQ,
                                                Status.CONSEQUENCE]
                            and not l.relevant)

    out["models"] = ("" if len(models) < max_rows and time.time()<max_time else
        "Time out or more than {max_rows} models...Showing partial results")
    out["variable"] = [[ [symb] for symb in table.keys()
                        if symb in active_symbol ]]
    for i in range(len(models)):
        out["variable"] += [[ table[symb][i] for symb in table.keys()
                            if symb in active_symbol ]]
    return out



