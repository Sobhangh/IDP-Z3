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

import time

from idp_engine.Assignments import Status
from idp_engine.Expression import AppliedSymbol, TRUE
from idp_engine.utils import OrderedSet, RELEVANT
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
           constraint.decl.name == RELEVANT:
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

        # only keep questions in self.assignments
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
    self.relevant_symbols = relevants


def explain(state, consequence):
    (facts, laws) = state.explain(consequence)
    out = Output(state, state.given)
    for ass in facts:
        out.addAtom(ass.sentence, ass.value, ass.status)
    out.m["*laws*"] = [l.annotations['reading'] for l in laws]

    # remove irrelevant atoms
    for symb, dictionary in out.m.items():
        if symb != "*laws*":
            out.m[symb] = {k: v for k, v in dictionary.items()
                            if type(v) == dict and v['status'] in
                               ['GIVEN', 'STRUCTURE']
                            and v.get('value', '') != ''}
    out.m = {k: v for k, v in out.m.items() if v or k =="*laws*"}
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
    out = {} # {heading : [Assignment]}

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
        f"Time out or more than {max_rows} models...Showing partial results")
    out["variable"] = [[ [symb] for symb in table.keys()
                        if symb in active_symbol ]]
    for i in range(len(models)):
        out["variable"] += [[ table[symb][i] for symb in table.keys()
                            if symb in active_symbol ]]
    return out



