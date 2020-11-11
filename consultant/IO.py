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


def metaJSON(idp):
    """
    Format a response to meta request.

    :arg idp: the response
    :returns out: a meta request

    """
    symbols = []
    for decl in idp.theory.assignments.symbols.values():
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
    optionalPropagation = idp.display.optionalPropagation

    # Create the output dictionary.
    out = {"title": "Interactive Consultant", "symbols": symbols,
        "optionalPropagation": optionalPropagation}
    return out



#################
# load user's choices
# see docs/zettlr/REST.md
#################

def decode_UTF(json_str):
    return (json_str
        .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
        .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃")
        .replace("\\\\u21d2", "⇒").replace("\\\\u21d4", "⇔").replace("\\\\u21d0", "⇐")
        .replace("\\\\u2228", "∨").replace("\\\\u2227", "∧"))

def json_to_literals(case, jsonstr: str):
    """ returns Assignments corresponding to jsonstr """
    assignments = Assignments() # {atom : assignment} from the GUI (needed for propagate)
    if jsonstr:
        json_data = ast.literal_eval(decode_UTF(jsonstr))

        for symbol in json_data:
            idp_symbol = case.idp.vocabulary.symbol_decls[symbol]
            for atom, json_atom in json_data[symbol].items():
                idp_atom = case.assignments[atom].sentence.copy()

                if json_atom["value"]!='':
                    value = str_to_IDP(idp_atom, str(json_atom["value"]))
                    if json_atom["typ"] == "Bool":
                        assignments.assert_(idp_atom, value, Status.GIVEN, False)
                    elif json_atom["value"]:
                        assignments.assert_(idp_atom, value, Status.GIVEN, True)

                        idp_atom = AComparison.make('=', [idp_atom, value])
                        assignments.assert_(idp_atom, TRUE, Status.GIVEN, True)
    return assignments


#################
# response to client
# see docs/zettlr/REST.md
#################


class Output(object):
    def __init__(self, case, structure={}):
        self.m = {} # [symbol.name][atom.code][attribute name] -> attribute value
        self.case = case

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = bool(len(case.idp.vocabularies)==2)

        def initialise(atom):
            typ = atom.type
            key = atom.code
            if ( key in case.assignments 
            and case.assignments[key].symbol_decl is not None):
                symb = case.assignments[key].symbol_decl
                s = self.m.setdefault(symb.name, {})

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
                    assert atom.code in case.assignments
                    symbol["status"]   = case.assignments[atom.code].status.name
                    symbol["relevant"] = case.assignments[atom.code].relevant
                    symbol['reading']  = reading
                    symbol['normal']   = type(atom) in [AppliedSymbol, Variable]
                    symbol['environmental'] = symb.block.name=='environment'
                    symbol['is_assignment'] = symbol['typ'] != 'Bool' \
                        or bool(case.assignments[atom.code].sentence.is_assignment)
                    s.setdefault(key, symbol)
                    s["__rank"] = self.case.relevant_symbols.get(symb.name, 9999)

        for GuiLine in case.assignments.values():
            initialise(GuiLine.sentence)
        for ass in structure.values(): # add numeric input for Explain
            initialise(ass.sentence)

    def fill(self, case):
        for key, l in case.assignments.items():
            if l.value is not None:
                if l.status == Status.STRUCTURE:
                    key = l.sentence.code
                    symb = self.case.assignments[key].symbol_decl
                    if symb.name in self.m:
                        del self.m[symb.name]
                self.addAtom(l.sentence, l.value, l.status)
        return self.m


    def addAtom(self, atom, value, status: Status):
        key = atom.code
        if key in self.case.assignments:
            symb = self.case.assignments[key].symbol_decl
            if symb is not None:
                s = self.m.setdefault(symb.name, {})
                if key in s:
                    if value is not None:
                        if type(value)==NumberConstant:
                            s[key]["value"] = str(eval(str(value).replace('?', '')))
                        else:
                            s[key]["value"] = True if value.same_as(TRUE) else \
                                             False if value.same_as(FALSE) else str(value)
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading']
                    #s[key]["status"] = status.name # for a click on Sides=3

