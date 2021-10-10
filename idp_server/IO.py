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
This module contains code to create and analyze messages to/from the
web client.
"""

import ast

from idp_engine import Problem, Status
from idp_engine.Expression import (TRUE, FALSE, Number)
from idp_engine.Parse import str_to_IDP
from idp_engine.Assignments import Status as S
from idp_engine.utils import BOOL, INT, REAL, DATE

def metaJSON(state):
    """
    Format a response to meta request.

    :arg idp: the response
    :returns out: a meta request

    """
    symbols = []
    for decl in state.assignments.symbols.values():
        if not decl.private:
            typ = decl.out.name
            symbol_type = "proposition" if typ == BOOL and decl.sorts == [] else "function"
            d = {
                "idpname": str(decl.name),
                "type": symbol_type,
                "priority": "core",
                "showOptimize": True,  # GUI is smart enough to show buttons appropriately
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
                if 'Slider' in decl.annotations:
                    d['slider'] = decl.annotations['Slider']

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


def load_json(state: Problem, jsonstr: str):
    """ Parse a json string and update assignments in a state accordingly.

    :arg state: a Problem object containing the concepts that appear in the json
    :arg jsonstr: the user's assignments in json
    :returns: the assignments
    :rtype: idp_engine.Assignments
    """
    if jsonstr:
        json_data = ast.literal_eval(jsonstr)
        assert json_data != {}, "Reset not expected here"

        for symbol in json_data:
            # tentative set of sentences to be cleared
            to_clear = set(atom.sentence for atom in state.assignments.values()
                           if (atom.symbol_decl.name == symbol
                           and atom.status in [S.GIVEN, S.DEFAULT, S.EXPANDED]))

            # processed json_data
            for key, json_atom in json_data[symbol].items():
                if key in state.assignments:
                    atom = state.assignments[key]
                    sentence = atom.sentence

                    # If the atom is unknown, set its value as normal.
                    if json_atom["value"] != '':
                        to_clear.discard(sentence)
                        if atom.status == S.UNKNOWN:
                            value = str_to_IDP(sentence, str(json_atom["value"]))
                            state.assert_(sentence.code, value, S.GIVEN)
                            if json_atom["typ"] != "Bool":
                                key2 = f"{sentence.code} = {str(value)}"
                                if key2 in state.assignments:
                                    state.assert_(key2, TRUE, S.GIVEN)

                        # If the atom was not already set in default struct, overwrite.
                        elif atom.status != S.DEFAULT:
                            value = str_to_IDP(sentence, str(json_atom["value"]))
                            state.assert_(sentence.code, value, S.GIVEN)

            # clear the remaining sentences
            for sentence in to_clear:
                state.assert_(sentence.code, None, S.UNKNOWN)


#################
# response to client
# see docs/zettlr/REST.md
#################


class Output(object):
    def __init__(self, state):
        self.m = {}  # [symbol.name][atom.code][attribute name] -> attribute value
        self.state = state

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = state.environment is not None
        self.m[' Global']['active'] = state.active

        for key, ass in state.assignments.items():
            atom = ass.sentence
            symb = state.assignments[key].symbol_decl
            if symb is not None and not symb.private:
                s = self.m.setdefault(symb.name, {})

                typ = atom.type
                if typ == BOOL:
                    symbol = {"typ": typ}
                elif typ in [REAL, INT, DATE]:
                    symbol = {"typ": typ, "value": ""}  # default
                elif 0 < len(symb.range):
                    # TODO: ugly string representation hack to get the range of a term
                    sep = " in {"
                    instring = [c.__str1__() for c in state.constraints]
                    instring = [s.split(sep)[1][:-1] for s in instring if s.startswith(ass.sentence.__str__()+sep)]
                    typ = symb.out.decl.type
                    if len(instring) == 1:
                        symbol = {"typ": typ, "value": "", "values": instring[0].split(', ')}
                    else:
                        symbol = {"typ": typ, "value": "", "values": []}
                else:
                    assert False, "dead code"
                    symbol = None

                if symb.name == key and 'reading' in symb.annotations:  #inherit reading
                    reading = symb.annotations['reading']
                else:
                    reading = atom.annotations['reading']

                if symbol:
                    symbol["status"] = ass.status.name
                    symbol["relevant"] = ass.relevant if ass.relevant is not None else True
                    symbol['reading'] = reading.replace("()","")
                    symbol['normal'] = not atom.is_reified()
                    symbol['environmental'] = symb.block.name == 'environment'
                    symbol['is_assignment'] = symbol['typ'] != BOOL \
                        or bool(ass.sentence.is_assignment())
                    s.setdefault(key, symbol)
                    s["__rank"] = self.state.relevant_symbols.get(symb.name, 9999)

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
                            s[key]["value"] = str(eval(str(value).replace('?', '')))
                        else:
                            s[key]["value"] = True if value.same_as(TRUE) else \
                                             False if value.same_as(FALSE) else \
                                             str(value)
                        if 0 < len(symb.range) and atom.type != BOOL:
                            # allow display of the value in drop box
                            s[key]["values"] = [s[key]["value"]]
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading'].replace("()", "")
                    #s[key]["status"] = status.name  # for a click on Sides=3
