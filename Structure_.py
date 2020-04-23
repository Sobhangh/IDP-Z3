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
    UNIVERSAL   = 4
    ENV_CONSQ   = 8
    CONSEQUENCE = 16
    EXPANDED    = 32

class Assignment(object):
    def __init__(self, sentence: Expression, truth: Optional[Expression], status: Status):
        self.sentence = sentence
        self.truth = truth
        self.status = status
        self.relevant = False
        self.is_environmental = not sentence.has_environmental(False)

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

    def __hash__(self):
        return hash((str(self.sentence), str(self.truth)))

    def __eq__(self, other):
        # ignores the modality of truth !
        return self.truth == other.truth \
            and type(self.sentence) == type (other.sentence) \
            and str(self.sentence) == str(other.sentence)

    def __repr__(self):
        out = str(self.sentence.code)
        if self.truth is None:
            return f"? {out}"
        if self.truth == TRUE:
            return out
        if self.truth == FALSE:
            return f"~{out}"
        return f"{out} -> {str(truth)}"

    def __str__(self):
        out = str(self.sentence.code)
        if self.truth is None:
            out = f"? {out}"
        elif self.truth == TRUE:
            pass
        elif self.truth == FALSE:
            out = f"Not {out}"
        else:
            out = f"{out} -> {str(truth)}"
        return f"{out}{self.sentence.annotations['reading']}"
    

    def as_substitution(self, case) -> Tuple[Optional[Expression], Optional[Expression]]:
        if self.truth is not None:
            old = self.sentence
            new = self.truth
            if self.truth == TRUE:  # analyze true equalities
                if isinstance(old, Equality):
                    if is_number(old.valueZ3):
                        new = NumberConstant(number=str(old.valueZ3))
                        old = old.variable
                    elif str(old.valueZ3) in case.idp.vocabulary.symbol_decls:
                        new = case.idp.vocabulary.symbol_decls[str(old.valueZ3)]
                        old = old.variable
                elif isinstance(old, AComparison) and old.operator == ['=']:
                    if   type(old.sub_exprs[1]) in [Constructor, NumberConstant]:
                        new = old.sub_exprs[1]
                        old = old.sub_exprs[0]
                    elif type(old.sub_exprs[0]) in [Constructor, NumberConstant]:
                        new = old.sub_exprs[0]
                        old = old.sub_exprs[1]
                    else:
                        operands1 = [e.as_ground() for e in old.sub_exprs]
                        if   operands1[1] is not None:
                            new = operands1[1]
                            old = old.sub_exprs[0]
                        elif operands1[0] is not None:
                            new = operands1[0]
                            old = old.sub_exprs[1]
            return old, new
        return None, None

    def to_json(self) -> str: return str(self)

    def translate(self) -> BoolRef:
        if self.truth is None:
            raise Exception("can't translate unknown value")
        if self.sentence.type == 'bool':
            return self.sentence.translate() if self.truth==TRUE else Not(self.sentence.translate())
        return self.sentence.translate()

class Term(Assignment):
    """ represents an applied symbol of unknown values """

    def as_substitution(self, case):
        return None, None

    def assign(self, value: DatatypeRef, case, CONSQ: Status):
        self.sentence = cast (Equality, self.sentence)
        ass = Assignment(Equality(self.sentence.variable, value), TRUE, CONSQ)
        ass.relevant = True
        case.assignments[self.sentence.code] = ass
        return ass


class Equality(Expression):
    def __init__(self, variable: Union[AppliedSymbol, Variable, Fresh_Variable], value):
        self.variable = variable # an Expression
        self.valueZ3 = value # a Z3 value or None
        self.value = None
        self.status = None
        self.simpler = None
        if value is not None:
            self.type = 'bool'
            self.code = sys.intern(f"{variable.code} = {str(value)}")
            self.translated = (variable.translate() == value)
        else:
            self.type = 'int' #TODO float ?
            self.code = sys.intern(variable.code)
            self.translated = variable.translate()
        self.str = self.code
        self.annotations = {'reading': self.code} #TODO find original code (parenthesis !)
        self.is_subtence = True

    def __str__(self): return self.code

    def unknown_symbols(self):
        return self.variable.unknown_symbols()

    def has_environmental(self, truth: bool):
        return self.variable.has_environmental(truth)

    def translate(self) -> DatatypeRef:
        if self.valueZ3 is not None:
            return self.variable.translate() == self.valueZ3
        else:
            return self.variable.translate()

    def substitute(self, e0: Expression, e1: Expression, todo=None, case=None) -> 'Equality':
        if self.variable == e0:
            return Equality(self.variable, e1.translate())
        return self

    def subtences(self):
        return {} #TODO ?

    def reified(self) -> DatatypeRef:
        return self.variable.reified()


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
                if atom in idp.subtences:
                    atom = idp.subtences[atom].copy()
                else:
                    symbol = idp.vocabulary.symbol_decls[sym]
                    atom = symbol.instances[atom].copy()
                if json_atom["typ"] == "Bool":
                    if "value" in json_atom:
                        assignment = Assignment(atom, str_to_IDP(idp, json_atom["value"]), Status.GIVEN)
                        assignments[atom] = assignment
                    else:
                        assignment = None  #TODO error ?
                elif json_atom["value"]:
                    if json_atom["typ"] in ["Int", "Real"]:
                        value = eval(json_atom["value"])
                    else:
                        value = idp.vocabulary.symbol_decls[json_atom["value"]].translated
                    assignment = Assignment(Equality(atom, value), TRUE, Status.GIVEN)
                    assignment.relevant = True
                    assignments[atom] = assignment
                else:
                    assignment = None #TODO error ?
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
                        if type(atom) != Equality:
                            print(atom)
                        atomZ3 = atom.reified()
                    value = model.eval(atomZ3, model_completion=True)

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
            atomZ3 = atom.translate() #TODO
            key = atom.code
            if type(atomZ3) != bool:
                typ = atomZ3.sort().name()
                for symb in atom.unknown_symbols().values():
                    if not symb.name.startswith('_'):
                        s = self.m.setdefault(symb.name, {})

                        if typ == 'Bool':
                            symbol = {"typ": typ}
                        elif 0 < len(symb.range):
                            symbol = { "typ": typ, "value": "" #TODO
                                    , "values": [str(v) for v in symb.range]}
                        elif typ in ["Real", "Int"]:
                            symbol = {"typ": typ, "value": ""} # default
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
        if truth and type(atom) == Equality:
            symbol = atom.variable.translate()
            key = atom.variable.code
            typ = symbol.sort().name()
            for name, symb in atom.unknown_symbols().items():
                if not symb.name.startswith('_'):
                    s = self.m.setdefault(name, {})
                    if key in s:
                        if typ in ["Real", "Int"]:
                            s[key]["value"] = str(eval(str(atom.valueZ3).replace('?', ''))) # compute fraction
                        elif 0 < len(symb.range): #TODO and type(atom) != IfExpr:
                            s[key]["value"] = str(atom.valueZ3)
                        s[key]["status"] = status.name
        if atom.type != 'bool': return
        key = atom.code
        if key in self.case.GUILines:
            for symb in self.case.GUILines[key].unknown_symbols().keys():
                s = self.m.setdefault(symb, {})
                if key in s:
                    if truth is not None:
                        s[key]["value"] = True if truth==TRUE else False if truth==FALSE else truth
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading']
                    #s[key]["status"] = status.name # for a click on Sides=3

