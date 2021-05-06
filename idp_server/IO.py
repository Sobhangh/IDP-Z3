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

from idp_engine.Expression import (TRUE, FALSE, AComparison, Number)
from idp_engine.Parse import str_to_IDP
from idp_engine.Assignments import Assignments, Status
from idp_engine.utils import BOOL, INT, REAL, DATE

def metaJSON(state):
    """
    Format a response to meta request.

    :arg idp: the response
    :returns out: a meta request

    """
    symbols = []
    for decl in state.assignments.symbols.values():
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

    # Create the output dictionary.
    out = {"title": "Interactive Consultant", "symbols": symbols,
           "optionalPropagation": optionalPropagation}
    return out


#################
# load user's choices
# see docs/zettlr/REST.md
#################


def json_to_literals(state, jsonstr: str):
    """ Parse a json string and create assignments in a state accordingly.
    This function can also overwrite assignments that have already been set as
    a default assignment, effectively overriding the default.

    :arg state: a State object containing the concepts that appear in the json
    :arg jsonstr: the user's assignments in json
    :returns: the assignments
    :rtype: idp_engine.Assignments
    """
    out = Assignments()

    if jsonstr:
        json_data = ast.literal_eval(jsonstr)
        default = [x for x, v in state.assignments.items()
                   if v.status == Status.GIVEN]
        if json_data == {}:
            # If json_data was empty (e.g. at beginning), we need to check if
            # we can make more assertions.
            for symbol in default:
                idp_atom = state.assignments[symbol].sentence
                # We do not need to create comparisons for all types.
                if idp_atom.type in ["Real", "Bool", "Int"]:
                    continue
                value = state.assignments[symbol].value
                idp_atom = AComparison.make('=', [idp_atom, value])
                state.assignments.assert_(idp_atom, TRUE,
                                          Status.GIVEN, False)
            return out

        for symbol in default:
            # If a boolean is unset, it does not show up in the jsonstr.
            # If it is not in jsonstr we unset the default value.
            if symbol not in json_data:
                state.assignments[symbol].unset()

        for symbol in json_data:
            # If no value was given for a default symbol we unset it.
            if len(json_data[symbol]) == 0 and symbol in default:
                state.assignments[symbol].unset()
                continue

            for atom, json_atom in json_data[symbol].items():
                if atom in state.assignments:
                    idp_atom = state.assignments[atom].sentence

                    # If the atom is unknown, set its value as normal.
                    if (json_atom["value"] != ''
                        and state.assignments[atom].status == Status.UNKNOWN):
                        value = str_to_IDP(idp_atom, str(json_atom["value"]))
                        state.assignments.assert_(idp_atom, value,
                                                  Status.GIVEN, False)
                        if json_atom["typ"] != "Bool":
                            idp_atom = AComparison.make('=', [idp_atom, value])
                            state.assignments.assert_(idp_atom, TRUE,
                                                      Status.GIVEN, False)

                    # If the atom was already set in default struct, overwrite.
                    elif json_atom["value"] != '':
                        value = str_to_IDP(idp_atom, str(json_atom["value"]))
                        state.assignments[atom].value = value

                    else:
                        state.assignments[atom].value = None
                    out[atom] = state.assignments[atom]
    return out


#################
# response to client
# see docs/zettlr/REST.md
#################


class Output(object):
    def __init__(self, state, structure={}):
        self.m = {}  # [symbol.name][atom.code][attribute name] -> attribute value
        self.state = state

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = state.environment is not None

        for key, ass in state.assignments.items():
            atom = ass.sentence
            symb = state.assignments[key].symbol_decl
            if symb is not None:
                s = self.m.setdefault(symb.name, {})

                typ = atom.type
                if typ == BOOL:
                    symbol = {"typ": typ}
                elif 0 < len(symb.range):
                    typ = symb.out.decl.type
                    symbol = {"typ": typ, "value": ""  #TODO
                              , "values": [str(v) for v in symb.range]}
                elif typ in [REAL, INT, DATE]:
                    symbol = {"typ": typ, "value": ""}  # default
                else:
                    assert False, "dead code"
                    symbol = None

                if symb.name == key and 'reading' in symb.annotations:  #inherit reading
                    reading = symb.annotations['reading']
                else:
                    reading = atom.annotations['reading']

                if symbol:
                    symbol["status"] = ass.status.name
                    symbol["relevant"] = ass.relevant
                    symbol['reading'] = reading.replace("()","")
                    symbol['normal'] = not atom.is_reified()
                    symbol['environmental'] = symb.block.name == 'environment'
                    symbol['is_assignment'] = symbol['typ'] != BOOL \
                        or bool(ass.sentence.is_assignment())
                    s.setdefault(key, symbol)
                    s["__rank"] = self.state.relevant_symbols.get(symb.name, 9999)

        # Remove symbols that are in a structure.
        for key, l in state.assignments.items():
            if l.status == Status.STRUCTURE:
                symb = self.state.assignments[key].symbol_decl
                if symb and symb.name in self.m:
                    # reassign sentences if possible
                    for k, data in self.m[symb.name].items():
                        if k in self.state.assignments:
                            for s in self.state.assignments[k].symbols:
                                if (not s.name.startswith('_')
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

    def addAtom(self, atom, value, status: Status):
        key = atom.code
        if key in self.state.assignments:
            symb = self.state.assignments[key].symbol_decl
            if symb is not None:
                s = self.m.setdefault(symb.name, {})
                if key in s:
                    if value is not None:
                        if type(value) == Number:
                            s[key]["value"] = str(eval(str(value).replace('?', '')))
                        else:
                            s[key]["value"] = True if value.same_as(TRUE) else \
                                             False if value.same_as(FALSE) else \
                                             str(value)
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading'].replace("()", "")
                    #s[key]["status"] = status.name  # for a click on Sides=3
