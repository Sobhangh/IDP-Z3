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
    for i in idp.unknown_symbols().values():
        typ = i.out.name
        symbol_type = "proposition" if typ == 'bool' and i.sorts==[] else "function"
        d = {
            "idpname": str(i.name),
            "type": symbol_type,
            "priority": "core",
            "showOptimize": True,  # GUI is smart enough to show buttons appropriately
            "view": i.view.value,
            "environmental": i.block.name=='environment'
        }
        if i.annotations is not None:
            if 'reading' in i.annotations:
                d['guiname'] = i.annotations['reading']
            if 'short' in i.annotations:
                d['shortinfo'] = i.annotations['short']
            if 'long' in i.annotations:
                d['longinfo'] = i.annotations['long']
            if 'Slider' in i.annotations:
                d['slider'] = i.annotations['Slider']

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

def json_to_literals(idp, jsonstr: str):
    assignments = Assignments() # {atom : assignment} from the GUI (needed for propagate)
    if jsonstr:
        json_data = ast.literal_eval(jsonstr \
            .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
            .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃")
            .replace("\\\\u21d2", "⇒").replace("\\\\u21d4", "⇔").replace("\\\\u21d0", "⇐")
            .replace("\\\\u2228", "∨").replace("\\\\u2227", "∧"))

        for symbol in json_data:
            idp_symbol = idp.vocabulary.symbol_decls[symbol]
            for atom, json_atom in json_data[symbol].items():
                if atom in idp.subtences:
                    idp_atom = idp.subtences[atom].copy()
                else:
                    idp_atom = idp_symbol.instances[atom].copy()

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

def model_to_json(case, s):
    model = s.model()
    out = Output(case)
    out.fill(case)
    
    for symb, d1 in out.m.items():
        if symb != ' Global':
            for atom_code, d2 in d1.items():
                if atom_code != '__rank' and d2['status'] == 'UNKNOWN':
                    d2['status'] = 'EXPANDED'

                    atom = case.assignments[atom_code].sentence
                    s.push() # in case todo contains complex formula
                    s.add(atom.reified()==atom.translate())
                    if s.check() == sat:
                        value = s.model().eval(atom.reified(), model_completion=True)
                        value = str_to_IDP(atom, str(value))

                        # atom might not have an interpretation in model (if "don't care")
                        if atom.type == 'bool':
                            d2['value']  = (value == TRUE)
                        else:
                            d2['value'] = str(value)
                    s.pop()
    return out.m


class Output(object):
    def __init__(self, case, structure={}):
        self.m = {} # [symbol.name][atom.code][attribute name] -> attribute value
        self.case = case

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = bool(len(case.idp.vocabularies)==2)

        def initialise(atom):
            typ = atom.type
            key = atom.code
            for symb in atom.unknown_symbols().values():
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
                    break

        for GuiLine in case.GUILines.values():
            initialise(GuiLine)
        for ass in structure.values(): # add numeric input for Explain
            initialise(ass.sentence)

    def fill(self, case):
        for key, l in case.assignments.items():
            if l.value is not None:
                if l.status == Status.STRUCTURE:
                    key = l.sentence.code
                    for symb in self.case.GUILines[key].unknown_symbols():
                        del self.m[symb]
                        break
                if key in case.GUILines:
                    self.addAtom(l.sentence, l.value, l.status)


    def addAtom(self, atom, value, status: Status):
        key = atom.code
        if key in self.case.GUILines:
            for symb in self.case.GUILines[key].unknown_symbols():
                s = self.m.setdefault(symb, {})
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
                break

