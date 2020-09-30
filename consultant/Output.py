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
import ast
import sys
from typing import Optional, Dict

from Idp.Expression import Expression, TRUE, FALSE, AComparison, NumberConstant
from Idp.Run import Status, Assignment, Assignments
from Idp.utils import *



#################
# load user's choices
# see docs/REST.md
#################

def str_to_IDP(idp, val1):
    if is_number(val1):
        return NumberConstant(number=val1)
    val1 = 'true' if str(val1) == 'True' else 'false' if str(val1) == 'False' else val1
    val = idp.vocabulary.symbol_decls[val1]
    return val

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

                value = str_to_IDP(idp, json_atom["value"])
                if json_atom["typ"] == "Bool":
                    assignments.assert_(idp_atom, value, Status.GIVEN, False)
                elif json_atom["value"]:
                    assignments.assert_(idp_atom, value, Status.GIVEN, True)

                    idp_atom = AComparison.make('=', [idp_atom, value])
                    assignments.assert_(idp_atom, TRUE, Status.GIVEN, True)
    return assignments


#################
# response to client
# see docs/REST.md
#################

def model_to_json(case, s, reify):
    model = s.model()
    out = Output(case)
    out.fill(case)
    
    for symb, d1 in out.m.items():
        if symb != ' Global':
            for atom_code, d2 in d1.items():
                if atom_code != '__rank' and d2['status'] == 'UNKNOWN':
                    d2['status'] = 'EXPANDED'

                    atom = case.assignments[atom_code].sentence
                    if atom.code in reify:
                        atomZ3 = reify[atom.code]
                    else:
                        atomZ3 = atom.reified()
                    value = model.eval(atomZ3, model_completion=True)
                    value = str_to_IDP(case.idp, str(value))

                    # atom might not have an interpretation in model (if "don't care")
                    if atom.type == 'bool':
                        if value not in [TRUE, FALSE]: 
                            #TODO value may be an expression, e.g. for quantified expression --> assert a value ?
                            print("*** ", atom.annotations['reading'], " is not defined, and assumed false")
                        d2['value']  = (value == TRUE)
                    else:
                        try:
                            d2['value'] = str(eval(str(value).replace('?', '')))
                        except:
                            d2['value'] = str(value)
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
                    symbol['normal']   = hasattr(atom, 'normal')
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
            if l.value is not None and key in case.GUILines:
                if case.GUILines[key].is_visible:
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

