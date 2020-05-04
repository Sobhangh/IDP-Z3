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
from copy import copy
from enum import IntFlag
import sys
from typing import Union, Optional, Dict, Tuple, cast
from z3 import Constructor, Not, BoolVal, BoolRef, is_true, is_false, is_bool, DatatypeRef

from Idp.Expression import Expression, TRUE, FALSE, AComparison, NumberConstant, Constructor, NumberConstant, AppliedSymbol, Variable, Fresh_Variable
from utils import *


class Status(IntFlag):
    UNKNOWN     = 1
    GIVEN       = 2
    ENV_UNIV    = 4
    UNIVERSAL   = 8
    ENV_CONSQ   = 16
    CONSEQUENCE = 32
    EXPANDED    = 64

class Assignment(object):
    def __init__(self, sentence: Expression, truth: Optional[Expression], status: Status):
        self.sentence = sentence
        self.truth = truth
        self.status = status
        self.relevant = False

    def update(self, sentence: Optional[Expression], 
                     truth: Optional[Expression], 
                     status: Optional[Status], 
                     case):
        """ make a copy, and save it in case.assignments """
        out = copy(self) # needed for explain of irrelevant symbols
        if sentence is not None: out.sentence = sentence
        if truth    is not None: out.truth    = truth
        if status   is not None: out.status   = status
        case.assignments[self.sentence.code] = out
        return out

    def __eq__(self, other):
        # ignores the modality of truth !
        return self.truth == other.truth \
            and type(self.sentence) == type (other.sentence) \
            and str(self.sentence) == str(other.sentence)

    def __hash__(self): #TODO remove. Used for sets in abstract
        return hash((str(self.sentence), str(self.truth)))

    def __repr__(self):
        out = str(self.sentence.code)
        if self.truth is None:
            return f"? {out}"
        if self.truth == TRUE:
            return out
        if self.truth == FALSE:
            return f"~{out}"
        return f"{out} -> {str(self.truth)}"

    def __str__(self):
        pre, post = '', ''
        if self.truth is None:
            pre = f"? "
        elif self.truth == TRUE:
            pre = ""
        elif self.truth == FALSE:
            pre = f"Not "
        else:
            post = f" -> {str(self.truth)}"
        return f"{pre}{self.sentence.annotations['reading']}{post}"
    

    def as_substitution(self, case) -> Tuple[Optional[Expression], Optional[Expression]]:
        if self.truth is not None:
            old = self.sentence
            new = self.truth
            return old, new
        return None, None

    def to_json(self) -> str: return str(self)

    def translate(self) -> BoolRef:
        if self.truth is None:
            raise Exception("can't translate unknown value")
        if self.sentence.type == 'bool':
            out = self.sentence.original.translate() if self.truth==TRUE else Not(self.sentence.original.translate())
        else:
            out = self.sentence.original.translate() == self.truth.translate()
        return out


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
    assignments: Dict[Expression, Optional[Assignment]] = {} # {atom : assignment} from the GUI (needed for propagate)
    if jsonstr:
        json_data = ast.literal_eval(jsonstr \
            .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
            .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃")
            .replace("\\\\u21d2", "⇒").replace("\\\\u21d4", "⇔").replace("\\\\u21d0", "⇐")
            .replace("\\\\u2228", "∨").replace("\\\\u2227", "∧"))

        assignment: Optional[Assignment]
        for sym in json_data:
            for atom in json_data[sym]:
                json_atom = json_data[sym][atom]
                assert "value" in json_atom
                if atom in idp.subtences:
                    atom = idp.subtences[atom].copy()
                else:
                    symbol = idp.vocabulary.symbol_decls[sym]
                    atom = symbol.instances[atom].copy()
                if json_atom["typ"] == "Bool":
                    u = atom.implicants(TRUE if json_atom["value"] else FALSE)
                    for sentence, truth in u:
                        assignment = Assignment(sentence, truth, Status.GIVEN)
                else:
                    assignment = Assignment(atom, str_to_IDP(idp, json_atom["value"]), Status.GIVEN)
                    assignment.relevant = True
                assignments[atom] = assignment
    return assignments


#################
# response to client
# see docs/REST.md
#################

def model_to_json(case, s, reify):
    model = s.model()
    out = Structure_(case)
    out.fill(case)
    
    for symb, d1 in out.m.items():
        if symb != ' Global':
            for atom_code, d2 in d1.items():
                if d2['status'] == 'UNKNOWN':
                    d2['status'] = 'EXPANDED'

                    atom = case.assignments[atom_code].sentence
                    if atom in reify:
                        atomZ3 = reify[atom]
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
                    else: #TODO check that value is numeric ?
                        try:
                            d2['value'] = str(eval(str(value).replace('?', '')))
                        except:
                            d2['value'] = str(value)
    return out.m


class Structure_(object):
    def __init__(self, case, structure={}):
        self.m = {} # [symbol.name][atom.code][attribute name] -> attribute value
        self.case = case

        self.m[' Global'] = {}
        self.m[' Global']['env_dec'] = bool(case.idp.decision)

        def initialise(atom):
            typ = atom.type
            key = atom.code
            for symb in atom.unknown_symbols().values():
                if not symb.name.startswith('_'):
                    s = self.m.setdefault(symb.name, {})

                    if typ == 'bool':
                        symbol = {"typ": 'Bool'}
                    elif 0 < len(symb.range):
                        typ = symb.out.decl.type.capitalize() if symb.out.decl.type in ['int', 'real'] else typ
                        symbol = { "typ": typ, "value": "" #TODO
                                , "values": [str(v) for v in symb.range]}
                    elif typ in ["real", "int"]:
                        symbol = {"typ": typ.capitalize(), "value": ""} # default
                    else:
                        symbol = None

                    if symbol:
                        if atom.code in case.assignments:
                            symbol["status"] = case.assignments[atom.code].status.name
                            symbol["relevant"] = case.assignments[atom.code].relevant
                        else:
                            symbol["status"] = "UNKNOWN" #TODO
                            symbol["relevant"] = True # unused symbol instance (Large(1))
                        symbol['reading'] = atom.annotations['reading']
                        symbol['normal'] = hasattr(atom, 'normal')
                        symbol['environmental'] = atom.has_environmental(True)
                        s.setdefault(key, symbol)
                        break

        for GuiLine in case.GUILines.values():
            initialise(GuiLine)
        for ass in structure.values(): # add numeric input for Explain
            initialise(ass.sentence)

    def fill(self, case):
        for key, l in case.assignments.items():
            if l.truth is not None and key in case.GUILines:
                if case.GUILines[key].is_visible:
                    self.addAtom(l.sentence, l.truth, l.status)


    def addAtom(self, atom, truth, status: Status):
        key = atom.code
        if key in self.case.GUILines:
            for symb in self.case.GUILines[key].unknown_symbols().keys():
                s = self.m.setdefault(symb, {})
                if key in s:
                    if truth is not None:
                        s[key]["value"] = True if truth==TRUE else False if truth==FALSE else str(truth)
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading']
                    #s[key]["status"] = status.name # for a click on Sides=3

