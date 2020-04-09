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
    def __init__(self, sentence: Expression, truth: Optional[bool], status: Status):
        self.sentence = sentence
        self.truth = truth
        self.proof = None
        self.status = status
        self.relevant = False
        self.is_environmental = not sentence.has_environmental(False)

    def update(self, sentence: Optional[Expression], 
                     truth: Optional[bool], 
                     proof,
                     status: Optional[Status], 
                     case):
        """ make a copy, and save it in case.assignments """
        out = copy(self) # needed for explain of irrelevant symbols
        if sentence is not None: out.sentence = sentence
        if truth    is not None: out.truth    = truth
        if status   is not None: out.status   = status
        out.proof = proof
        case.assignments[self.sentence.code] = out
        return out

    def __hash__(self):
        return hash((str(self.sentence), self.truth))

    def __eq__(self, other):
        # ignores the modality of truth !
        return self.truth == other.truth \
            and type(self.sentence) == type (other.sentence) \
            and str(self.sentence) == str(other.sentence)

    def __repr__(self):
        return ( f"{'' if self.truth else '~'}"
                 f"{str(self.sentence.code)}" 
                 f"{' <= '+str(self.proof) if self.proof else ''}")

    def __str__(self):
        return ( f"{'' if self.truth else '? ' if self.truth is None else 'Not '}"
                 f"{self.sentence.annotations['reading']}")
    

    def as_substitution(self, case) -> Tuple[Optional[Expression], Optional[Expression]]:
        if self.truth is not None:
            old = self.sentence
            new = cast(Expression, TRUE if self.truth else FALSE)
            if self.truth:  # analyze true equalities
                if isinstance(old, Equality):
                    if is_number(old.value):
                        new = NumberConstant(number=str(old.value))
                        old = old.variable
                    elif str(old.value) in case.idp.vocabulary.symbol_decls:
                        new = case.idp.vocabulary.symbol_decls[str(old.value)]
                        old = old.variable
                elif isinstance(old, AComparison) and old.operator == ['=']:
                    if   type(old.sub_exprs[1]) in [Constructor, NumberConstant]:
                        new = old.sub_exprs[1]
                        old = old.sub_exprs[0]
                    elif type(old.sub_exprs[0]) in [Constructor, NumberConstant]:
                        new = old.sub_exprs[0]
                        old = old.sub_exprs[1]
            return old, new
        return None, None

    def to_json(self) -> str: return str(self)

    def translate(self) -> BoolRef:
        if self.truth is None:
            raise Exception("can't translate unknown value")
        if self.sentence.type == 'bool':
            return self.sentence.translate() if self.truth else Not(self.sentence.translate())
        return self.sentence.translate()

class Term(Assignment):
    """ represents an applied symbol of unknown values """

    def as_substitution(self, case):
        return None, None

    def assign(self, value: DatatypeRef, case, CONSQ: Status):
        self.sentence = cast (Equality, self.sentence)
        ass = Assignment(Equality(self.sentence.variable, value), True, CONSQ)
        ass.relevant = True
        case.assignments[self.sentence.code] = ass
        return ass


class Equality(Expression):
    def __init__(self, variable: Union[AppliedSymbol, Variable, Fresh_Variable], value):
        self.variable = variable # an Expression
        self.value = value # a Z3 value or None
        if value is not None:
            self.type = 'bool'
            self.code = sys.intern(f"{variable.code} = {str(value)}")
            self.translated = (variable.translate() == value)
        else:
            self.type = 'int'
            self.code = sys.intern(variable.code)
            self.translated = variable.translated
        self.str = self.code
        self.annotations = {'reading': self.code} #TODO find original code (parenthesis !)
        self.proof = None

    def __str__(self): return self.code

    def unknown_symbols(self):
        return self.variable.unknown_symbols()

    def has_environmental(self, truth: bool):
        return self.variable.has_environmental(truth)

    def translate(self) -> DatatypeRef:
        if self.value is not None:
            return self.variable.translated == self.value
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
                    atom = idp.subtences[atom]
                else:
                    symbol = idp.vocabulary.symbol_decls[sym]
                    atom = symbol.instances[atom]
                if json_atom["typ"] == "Bool":
                    if "value" in json_atom:
                        assignment = Assignment(atom, json_atom["value"], Status.GIVEN)
                        assignments[atom] = assignment
                    else:
                        assignment = None  #TODO error ?
                elif json_atom["value"]:
                    if json_atom["typ"] in ["Int", "Real"]:
                        value = eval(json_atom["value"])
                    else:
                        value = idp.vocabulary.symbol_decls[json_atom["value"]].translated
                    assignment = Assignment(Equality(atom, value), True, Status.GIVEN)
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
                        if not (is_true(value) or is_false(value)):
                            #TODO value may be an expression, e.g. for quantified expression --> assert a value ?
                            print("*** ", atom.annotations['reading'], " is not defined, and assumed false")
                        d2['value']  = is_true(value)
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
            symbol = atom.variable.translated
            key = atom.variable.code
            typ = symbol.sort().name()
            for name, symb in atom.unknown_symbols().items():
                if not symb.name.startswith('_'):
                    s = self.m.setdefault(name, {})
                    if key in s:
                        if typ in ["Real", "Int"]:
                            s[key]["value"] = str(eval(str(atom.value).replace('?', ''))) # compute fraction
                        elif 0 < len(symb.range): #TODO and type(atom) != IfExpr:
                            s[key]["value"] = str(atom.value)
                        s[key]["status"] = status.name
        if atom.type != 'bool': return
        key = atom.code
        if key in self.case.GUILines:
            for symb in self.case.GUILines[key].unknown_symbols().keys():
                s = self.m.setdefault(symb, {})
                if key in s:
                    if truth is not None:
                        s[key]["value"] = truth
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.annotations['reading']
                    #s[key]["status"] = status.name # for a click on Sides=3

