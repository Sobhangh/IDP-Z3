# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
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
This module contains code to create and analyze messages to/from the
web client.
"""
from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from idp_engine import Theory, Status
from idp_engine.Expression import (TRUE, FALSE, Number, Date, BOOLT)
from idp_engine.Parse import str_to_IDP
from idp_engine.Assignments import Status as S
from idp_engine.utils import BOOL, INT, REAL, DATE

if TYPE_CHECKING:
    from .State import State

def metaJSON(state):
    """
    Format a response to meta request.

    :arg idp: the response
    :returns out: a meta request

    """
    symbols = []
    for decl in state.assignments.symbols.values():
        if not decl.private:
            typ = decl.codomain
            symbol_type = "proposition" if typ == BOOLT and decl.domains == [] else "function"
            d = {
                "idpname": str(decl.name),
                "type": symbol_type,
                "priority": "core",
                "showOptimize": decl.optimizable,
                "view": decl.view.value,
                "environmental": decl.block.name == 'environment',
            }
            if decl.unit:
                d["unit"] = decl.unit
            if decl.heading:
                d["category"] = decl.heading
            if decl.annotations is not None:
                if 'reading' in decl.annotations:
                    d['guiname'] = decl.annotations['reading']
                if 'short' in decl.annotations:
                    d['shortinfo'] = decl.annotations['short']
                if 'long' in decl.annotations:
                    d['longinfo'] = decl.annotations['long']
                if 'slider' in decl.annotations:
                    d['slider'] = decl.annotations['slider']
            symbols.append(d)

    optionalPropagation = state.idp.display.optionalPropagation
    manualPropagation = state.idp.display.manualPropagation
    optionalRelevance = state.idp.display.optionalRelevance
    manualRelevance = state.idp.display.manualRelevance

    # Create the output dictionary.
    out = {"title": "Interactive Consultant", "symbols": symbols,
           "optionalPropagation": optionalPropagation,
           "manualPropagation": manualPropagation,
           "optionalRelevance": optionalRelevance,
           "manualRelevance": manualRelevance}
    return out


#################
# load user's choices
# see docs/zettlr/REST.md
#################


def load_json(assignments, jsonstr: str, keep_defaults: bool):
    """ Parse a json string and update assignments in a state accordingly.

    :arg assignments: an assignments containing the concepts that appear in the json
    :arg jsonstr: assignments in json
    :arg keep_defaults: whether to not delete the default assignments
    :post: assignments is updated with information in json
    """

    if jsonstr:
        json_data = ast.literal_eval(jsonstr)

        # clear old choices, except for recent defaults, which should be kept after meta construction
        excluded = [S.STRUCTURE, S.UNIVERSAL] + ([S.DEFAULT] if keep_defaults else [])
        for atom in assignments.values():
            if atom.status not in excluded:
                assignments.assert__(atom.sentence, None, S.UNKNOWN)

        # set new choices
        status_map = {
            "UNKNOWN": S.UNKNOWN,
            "STRUCTURE": S.STRUCTURE,
            "UNIVERSAL": S.UNIVERSAL,
            "CONSEQUENCE": S.CONSEQUENCE,
            "ENV_CONSQ": S.ENV_CONSQ,
            "EXPANDED": S.EXPANDED,
            "DEFAULT": S.DEFAULT,
            "GIVEN": S.GIVEN
        }

        for symbol in json_data:
            # processed json_data
            for key, json_atom in json_data[symbol].items():
                if key in assignments:
                    atom = assignments[key]
                    sentence = atom.sentence

                    # If the atom is unknown, set its value as normal.
                    status = (S.GIVEN if json_atom["status"] == '' else
                            status_map[json_atom["status"]])

                    if json_atom["value"] != '' and atom.status == S.UNKNOWN:
                        value = str_to_IDP(str(json_atom["value"]), sentence.type)
                        assignments.assert__(sentence, value, status)
                        if json_atom["typ"] != "Bool":  # needed for default structure
                            code = f"{sentence.code} = {str(value)}"
                            if code in assignments:
                                atom = assignments[code].sentence
                                assignments.assert__(atom, TRUE, status)

#################
# response to client
# see docs/zettlr/REST.md
#################


class Output(object):
    def __init__(self, state: State):
        self.m = {}  # [symbol.name][atom.code][attribute name] -> attribute value
        self.state = state

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = state.environment is not None
        FROM = {BOOL: 'Bool', INT: 'Int', REAL: 'Real',
                '`'+BOOL: '`Bool', '`'+INT: '`Int', '`'+REAL: '`Real',}

        for key, ass in state.assignments.items():
            atom = ass.sentence
            symb = state.assignments[key].symbol_decl
            if symb is not None and not symb.private:
                s = self.m.setdefault(symb.name, {})

                typ = atom.type.name
                if typ == BOOL:
                    symbol = {"typ": "Bool"}
                elif 0 < len(symb.range):
                    if (isinstance(symb.range[0], Number)
                    or isinstance(symb.range[0], Date)):  # handle numeric ranges
                        typ = symb.range[0].type.name
                    symbol = {"typ": FROM.get(typ, typ),
                              "values": [str(v) for v in symb.range]}
                elif typ in [REAL, INT, DATE]:
                    symbol = {"typ": FROM.get(typ, typ), }
                else:
                    assert False, f"unknown type {typ} for {atom}"
                    symbol = None

                if symb.name == key and 'reading' in symb.annotations:  #inherit reading
                    reading = symb.annotations['reading']
                elif 'reading' in atom.annotations:
                    reading = atom.annotations['reading']
                else:
                    reading = atom.str
                    atom.annotations['reading'] = reading

                if symbol:
                    symbol["status"] = ass.status.name
                    symbol["relevant"] = ass.relevant if ass.relevant is not None else True
                    symbol['reading'] = reading.replace("()","")
                    symbol['normal'] = not atom.is_reified()
                    symbol['environmental'] = symb.block.name == 'environment'
                    symbol['is_assignment'] = symbol['typ'] != "Bool" \
                        or bool(ass.sentence.is_assignment())
                    s.setdefault(key, symbol)

        # Remove symbols that are in a structure.
        for key, l in state.assignments.items():
            if l.status == S.STRUCTURE:
                symb = self.state.assignments[key].symbol_decl
                if symb and symb.name in self.m:
                    # reassign sentences if possible
                    for k, data in self.m[symb.name].items():
                        if k in self.state.assignments:
                            for s in self.state.assignments[k].symbols:
                                if (not s.private
                                   and s.name in self.m
                                   and s.name != symb.name):
                                    self.state.assignments[k].symbol_decl = s
                                    self.m[s.name][k] = data
                                    break
                    self.m[symb.name] = {}

    def fill(self, state):
        for l in state.assignments.values():
            if l.value is not None:
                self.addAtom(l.sentence, l.value, l.status)
        return self.m

    def addAtom(self, atom, value, status: S):
        key = atom.code
        if key in self.state.assignments:
            symb = self.state.assignments[key].symbol_decl
            if symb is not None and not symb.private:
                s = self.m.setdefault(symb.name, {})
                if key in s:
                    if value is not None:
                        if type(value) == Number:
                            s[key]["value"] = str(value)
                        else:
                            s[key]["value"] = True if value.same_as(TRUE) else \
                                             False if value.same_as(FALSE) else \
                                             str(value)
                        if ((0 < len(symb.range) or hasattr(symb.codomain.decl, 'enumeration')) and atom.type != BOOLT):
                            # allow display of the value in drop box
                            s[key]["values"] = [s[key]["value"]]
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading'].replace("()", "")
                    #s[key]["status"] = status.name  # for a click on Sides=3
