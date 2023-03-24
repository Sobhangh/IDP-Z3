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

from idp_engine.Assignments import Status as S
from idp_engine.Expression import (AppliedSymbol, TRUE, Expression, AQuantification,
                                   AConjunction, Brackets)
from idp_engine.utils import OrderedSet
from .IO import Output


def explain(state, consequence=None):
    (facts, laws) = state.explain(consequence)
    out = Output(state)
    for ass in facts:
        out.addAtom(ass.sentence, ass.value, ass.status)
    def en(law):
        reading = law.annotations.get('reading', law.code)
        return reading if reading != law.code else law.EN()
    out.m['*laws*'] = [(law.code, en(law)) for law in laws]

    # remove irrelevant atoms
    for symb, dictionary in out.m.items():
        if symb != '*laws*':
            out.m[symb] = {k: v for k, v in dictionary.items()
                            if type(v) == dict and v['status'] in
                               ['GIVEN', 'STRUCTURE', 'DEFAULT', 'EXPANDED']
                            and v.get('value', '') != ''}

    out.m = {k: v for k, v in out.m.items() if v or k == '*laws*'}
    return out.m


def abstract(state, given_json):
    timeout_seconds, max_rows = 20, 50
    max_time = time.time()+timeout_seconds
    models, timeout = state.decision_table(goal_string="",
                                           timeout_seconds=timeout_seconds,
                                           max_rows=max_rows,
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
                            if l.status == S.UNIVERSAL)
    out["given"    ] = list(l for l in state.assignments.values()
                            if l.status in [S.GIVEN, S.DEFAULT, S.EXPANDED])
    # TODO: separate field for S.DEFAULT or S.EXPANDED?
    out["fixed"    ] = list(l for l in state.assignments.values()
                            if l.status in [S.ENV_CONSQ, S.CONSEQUENCE])
    out["irrelevant"]= list(l for l in state.assignments.values()
                            if l.status not in [S.ENV_CONSQ, S.CONSEQUENCE]
                            and not l.relevant)

    out["models"] = ("" if len(models) < max_rows and time.time()<max_time else
        f"Time out or more than {max_rows} models...Showing partial results")
    out["variable"] = [[ [symb] for symb in table.keys()
                        if symb in active_symbol ]]
    for i in range(len(models)):
        out["variable"] += [[ table[symb][i] for symb in table.keys()
                            if symb in active_symbol ]]
    return out



