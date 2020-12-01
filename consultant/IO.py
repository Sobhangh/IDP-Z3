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
import ast
import sys
from typing import Optional, Dict
from z3 import sat

from Idp.Expression import Expression, TRUE, FALSE, AComparison, NumberConstant, AppliedSymbol, Variable
from Idp.Run import Status, Assignment, Assignments, str_to_IDP
from Idp.utils import *


def metaJSON(state):
    """
    Format a response to meta request.

    :arg idp: the response
    :returns out: a meta request

    """
    symbols = []
    for decl in state.assignments.symbols.values():
        typ = decl.out.name
        symbol_type = "proposition" if typ == 'bool' and decl.sorts==[] else "function"
        d = {
            "idpname": str(decl.name),
            "type": symbol_type,
            "priority": "core",
            "showOptimize": True,  # GUI is smart enough to show buttons appropriately
            "view": decl.view.value,
            "environmental": decl.block.name=='environment'
        }
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


def decode_UTF(json_str: str) -> str:
    """ Convert all Python unicode to actual unicode characters.

    :arg json_str: the string to convert
    :returns: the converted string
    :rtype: str
    """
    decode_dict = {'\\\\u2264': '≤', '\\\\u2265': '≥', '\\\\u2260': '≠',
                   '\\\\u2200': "∀", '\\\\u2203': '∃', '\\\\u21d2': '⇒',
                   '\\\\u21d4': '⇔', '\\\\u21d0': '⇐', '\\\\u2228': '∨',
                   '\\\\u2227': '∧', '\\\\u00ac': '¬'}
    for source, char in decode_dict.items():
        json_str = json_str.replace(source, char)
    return json_str


def json_to_literals(state, jsonstr: str):
    """ Parse a json string and create assignments in a state accordingly.
    This function can also overwrite assignments that have already been set as
    a default assignment, effectively overriding the default.

    :arg state: a State object containing the concepts that appear in the json
    :arg jsonstr: the user's assignments in json
    :returns: the assignments
    :rtype: Idp.Assignments
    """
    out = Assignments()
    if jsonstr:
        json_data = ast.literal_eval(decode_UTF(jsonstr))
        for symbol in json_data:
            # If no value was given for a symbol, we still check to see if we
            # need to unset a default value.
            if (len(json_data[symbol]) == 0 or
               (symbol in json_data[symbol] and
               json_data[symbol][symbol]['value'] == '')):
                # Override default value.
                if symbol in state.assignments:
                    state.assignments[symbol].value = None
                    state.assignments[symbol].status = Status.UNKNOWN
                continue

            for atom, json_atom in json_data[symbol].items():
                if atom in state.assignments:
                    idp_atom = state.assignments[atom].sentence
                    if state.assignments[atom].value == '':
                        if json_atom["value"] != '':
                            value = str_to_IDP(idp_atom, str(json_atom["value"]))
                            if json_atom["typ"] == "Bool":
                                state.assignments.assert_(idp_atom, value, Status.GIVEN, False)
                            elif json_atom["value"]:
                                state.assignments.assert_(idp_atom, value, Status.GIVEN, True)

                                idp_atom = AComparison.make('=', [idp_atom, value])
                                state.assignments.assert_(idp_atom, TRUE, Status.GIVEN, True)
                            out[atom] = state.assignments[atom]
                    else:
                        # Override default value.
                        value = str_to_IDP(idp_atom, str(json_atom["value"]))
                        state.assignments[atom].value = value
                        state.assignments[atom].status = Status.GIVEN
    return out


#################
# response to client
# see docs/zettlr/REST.md
#################


class Output(object):
    def __init__(self, state, structure={}):
        self.m = {} # [symbol.name][atom.code][attribute name] -> attribute value
        self.state = state

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = state.environment is not None

        for key, ass in state.assignments.items():
            atom = ass.sentence
            symb = state.assignments[key].symbol_decl
            if symb is not None:
                s = self.m.setdefault(symb.name, {})

                typ = atom.type
                if typ == 'bool':
                    symbol = {"typ": 'Bool'}
                elif 0 < len(symb.range):
                    typ = symb.out.decl.type.capitalize() if symb.out.decl.type in ['int', 'real'] else typ
                    symbol = {"typ": typ, "value": ""  #TODO
                              , "values": [str(v) for v in symb.range]}
                elif typ in ["real", "int"]:
                    symbol = {"typ": typ.capitalize(), "value": ""} # default
                else:
                    assert False, "dead code"
                    symbol = None

                if symb.name == key and 'reading' in symb.annotations: #inherit reading
                    reading = symb.annotations['reading']
                else:
                    reading = atom.annotations['reading']

                if symbol:
                    symbol["status"]   = ass.status.name
                    symbol["relevant"] = ass.relevant
                    symbol['reading']  = reading
                    symbol['normal']   = not atom.is_reified()
                    symbol['environmental'] = symb.block.name=='environment'
                    symbol['is_assignment'] = symbol['typ'] != 'Bool' \
                        or bool(ass.sentence.is_assignment)
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
        for key, l in state.assignments.items():
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
                        if type(value) == NumberConstant:
                            s[key]["value"] = str(eval(str(value).replace('?', '')))
                        else:
                            s[key]["value"] = True if value.same_as(TRUE) else \
                                             False if value.same_as(FALSE) else str(value)
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading']
                    #s[key]["status"] = status.name # for a click on Sides=3

