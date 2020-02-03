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
from enum import IntFlag
import sys
from z3 import Constructor, Not, BoolVal, is_true, is_false


import Idp
from Idp.Expression import TRUE, FALSE, AComparison, NumberConstant
from utils import *


class Truth(IntFlag):
    FALSE       = 0
    TRUE        = 1
    UNKNOWN     = 3
    GIVEN       = 4
    UNIVERSAL   = 8
    ENV_CONSQ   = 16
    CONSEQUENCE = 32
    IRRELEVANT  = 255

    def Not(self): return (self & 252) | ((~self) & 1 if self.is_known() else Truth.UNKNOWN)
    def is_known(self): return self & Truth.UNKNOWN != Truth.UNKNOWN
    def is_true(self): return self & 3 == Truth.TRUE
    def to_bool(self): return bool(self & 1) # beware: UNKNOWN = True !
    def is_irrelevant(self): return self & 254 == 254


class Assignment(object):
    def __init__(self, truth : Truth, sentence):
        self.truth = truth
        self.sentence = sentence
        self.is_environmental = not sentence.has_environmental(False)

    def __hash__(self):
        return hash((self.truth & 3, str(self.sentence)))

    def __eq__(self, other):
        # ignores the modality of truth !
        return self.truth & 3 == other.truth & 3 \
            and type(self.sentence) == type (other.sentence) \
            and str(self.sentence) == str(other.sentence)

    def __repr__(self):
        return ( f"{'' if self.truth.is_true() else '~'}"
                 f"{str(self.sentence.code)}" )

    def __str__(self):
        if self.is_irrelevant():
            return ""
        return ("" if self.truth.is_true() else \
                "? " if not self.truth.is_known() \
                else "Not ") \
             + self.sentence.reading

    def Not           (self): return Assignment(self.truth.Not()              , self.sentence)
    def mk_given      (self): return Assignment(self.truth | Truth.GIVEN      , self.sentence)
    def mk_universal  (self): return Assignment(self.truth | Truth.UNIVERSAL  , self.sentence)
    def mk_env_consq  (self): return Assignment(self.truth | Truth.ENV_CONSQ  , self.sentence)
    def mk_consequence(self): 
        if self.is_env_consq(): return self
        return Assignment(self.truth | Truth.CONSEQUENCE, self.sentence)
    def mk_relevant   (self): 
        return Assignment(Truth.UNKNOWN, self.sentence) if self.is_irrelevant() \
                                     else self

    def is_given      (self): return not self.is_irrelevant() and self.truth & Truth.GIVEN
    def is_universal  (self): return not self.is_irrelevant() and self.truth & Truth.UNIVERSAL
    def is_env_consq  (self): return not self.is_irrelevant() and self.truth & Truth.ENV_CONSQ
    def is_consequence(self): return not self.is_irrelevant() and self.truth & Truth.CONSEQUENCE
    def is_irrelevant (self): return self.truth.is_irrelevant()

    def status(self):
        return ("GIVEN"      if self.is_given()       else
               "UNIVERSAL"   if self.is_universal()   else
               "ENV_CONSQ"   if self.is_env_consq()   else
               "CONSEQUENCE" if self.is_consequence() else
               "IRRELEVANT"  if self.is_irrelevant()  else 
               "UNKNOWN")

    def as_substitution(self, case):
        if self.truth.is_known():
            old = self.sentence
            new = TRUE if self.truth.is_true() else FALSE
            if self.truth.is_true():  # analyze equalities
                if isinstance(old, Equality) and type(self) != Term:
                    if is_number(old.value):
                        new = NumberConstant(number=str(old.value))
                        old = old.sentence
                    elif str(old.value) in case.idp.vocabulary.symbol_decls:
                        new = case.idp.vocabulary.symbol_decls[str(old.value)]
                        old = old.sentence
                elif isinstance(old, AComparison) and len(old.operator) == 1 and old.operator[0] == '=':
                    if type(old.sub_exprs[1]) in [Idp.Constructor, Idp.NumberConstant]:
                        new = old.sub_exprs[1]
                        old = old.sub_exprs[0]
                    elif isinstance(old.sub_exprs[0], Constructor):
                        new = old.sub_exprs[0]
                        old = old.sub_exprs[1]
            return old, new
        return None, None

    def to_json(self): return str(self)

    def translate(self):
        if self.truth == Truth.IRRELEVANT:
            return BoolVal(True)
        if self.sentence.type == 'bool':
            return self.sentence.translate() if self.truth & 1 else Not(self.sentence.translate())
        return self.sentence.translate()

class Term(Assignment):
    """ represents an applied symbol of unknown values """
    pass

class Equality(object):
    def __init__(self, sentence, value):
        self.sentence = sentence # an Expression
        self.value = value # a Z3 value or None
        if value is not None:
            self.type = 'bool'
            self.code = sys.intern(f"{sentence.code} = {str(value)}")
            self.translated = (sentence.translate() == value)
        else:
            self.type = 'int'
            self.code = sys.intern(sentence.code)
            self.translated = sentence.translated
        self.str = self.code
        self.reading = self.code #TODO find original code (parenthesis !)

    def __str__(self): return self.code

    def unknown_symbols(self):
        return self.sentence.unknown_symbols()

    def has_environmental(self, truth):
        return self.sentence.has_environmental(truth)

    def translate(self): 
        if self.value is not None:
            return self.sentence.translated == self.value
        else:
            return self.sentence.translate()

    def substitute(self, e0, e1):
        if self.sentence == e0:
            return Equality(self.sentence, e1.translate())
        return self

    def subtences(self):
        return {} #TODO ?

    def reified(self):
        return self.sentence.reified()

    
#################
# load user's choices
# see docs/REST.md
#################

def json_to_literals(idp, jsonstr):
    assignments = {} # {literalQ : atomZ3} from the GUI (needed for propagate)
    if jsonstr:
        json_data = ast.literal_eval(jsonstr \
            .replace("\\\\u2264", "≤").replace("\\\\u2265", "≥").replace("\\\\u2260", "≠")
            .replace("\\\\u2200", "∀").replace("\\\\u2203", "∃")
            .replace("\\\\u21d2", "⇒").replace("\\\\u21d4", "⇔").replace("\\\\u21d0", "⇐")
            .replace("\\\\u2228", "∨").replace("\\\\u2227", "∧"))

        for sym in json_data:
            for atom in json_data[sym]:
                json_atom = json_data[sym][atom]
                if atom in idp.theory.subtences:
                    atom = idp.theory.subtences[atom]
                else:
                    symbol = idp.vocabulary.symbol_decls[sym]
                    atom = symbol.instances[atom]
                if json_atom["typ"] == "Bool":
                    if "ct" in json_atom and json_atom["ct"]:
                        literalQ = Assignment(Truth.TRUE, atom).mk_given()
                    if "cf" in json_atom and json_atom["cf"]:
                        literalQ = Assignment(Truth.FALSE, atom).mk_given()
                elif json_atom["value"]:
                    if json_atom["typ"] in ["Int", "Real"]:
                        value = eval(json_atom["value"])
                    else:
                        value = idp.vocabulary.symbol_decls[json_atom["value"]].translated
                    literalQ = Assignment(Truth.TRUE, Equality(atom, value)).mk_given()
                else:
                    literalQ = None #TODO error ?
                if literalQ is not None:
                    assignments[literalQ] = literalQ.translate()
    return assignments


#################
# response to client
# see docs/REST.md
#################

def model_to_json(case, s, reify):
    m = s.model()
    out = Structure_(case)
    for atom in case.GUILines.values():
        # atom might not have an interpretation in model (if "don't care")
        value = m.eval(reify[atom], model_completion=True)
        if atom.type == 'bool':
            if not (is_true(value) or is_false(value)):
                #TODO value may be an expression, e.g. for quantified expression --> assert a value ?
                print("*** ", atom.reading, " is not defined, and assumed false")
            out.addAtom(atom, Truth.TRUE if is_true(value) else Truth.FALSE)
        else: #TODO check that value is numeric ?
            out.addAtom(Equality(atom, value), Truth.TRUE)
    return out.m


class Structure_(object):
    def __init__(self, case, structure=[]):
        self.m = {}
        self.case = case

        def initialise(atom):
            atomZ3 = atom.translate() #TODO
            key = atom.code
            typ = atomZ3.sort().name()
            for symb in atom.unknown_symbols().values():
                if not symb.name.startswith('_'):
                    s = self.m.setdefault(symb.name, {})

                    if typ == 'Bool':
                        symbol = {"typ": typ, "ct": False, "cf": False}
                    elif 0 < len(symb.range):
                        symbol = { "typ": typ, "value": ""
                                , "values": [str(v) for v in symb.range]}
                    elif typ in ["Real", "Int"]:
                        symbol = {"typ": typ, "value": ""} # default
                    else:
                        symbol = None
                        
                    if symbol: 
                        if atom.code in case.assignments:
                            symbol["status"] = case.assignments[atom.code].status()
                            symbol["irrelevant"] = case.assignments[atom.code].is_irrelevant()
                        else:
                            symbol["status"] = "UNKNOWN" #TODO 
                            symbol["irrelevant"] = False # unused symbol instance (Large(1))
                        symbol['reading'] = atom.reading
                        symbol['normal'] = hasattr(atom, 'normal')
                        symbol['environmental'] = atom.has_environmental(True)
                        s.setdefault(key, symbol)
                        break

        for GuiLine in case.GUILines.values():
            initialise(GuiLine)
        for ass in structure: # add numeric input for Explain
            initialise(ass.sentence)  


    def addAtom(self, atom, truth):
        if truth.is_true() and type(atom) == Equality:
            symbol = atom.sentence.translated
            key = atom.sentence.code
            typ = symbol.sort().name()
            for name, symb in atom.unknown_symbols().items():
                if not symb.name.startswith('_'):
                    s = self.m.setdefault(name, {})
                    if key in s:
                        if typ in ["Real", "Int"]:
                            s[key]["value"] = str(eval(str(atom.value).replace('?', ''))) # compute fraction
                        elif 0 < len(symb.range): #TODO and type(atom) != IfExpr:
                            s[key]["value"] = str(atom.value)
                        s[key]["status"] = Assignment(truth, atom).status() #TODO simplify
        if atom.type != 'bool': return
        key = atom.code
        if key in self.case.GUILines:
            for symb in self.case.GUILines[key].unknown_symbols().keys():
                s = self.m.setdefault(symb, {})
                if key in s:
                    if truth.is_known():
                        s[key]["value"] = truth.to_bool()
                        s[key]["ct" if truth.is_true() else "cf"] = True
                    else:
                        s[key]["unknown"] = True
                    s[key]['reading'] = atom.reading

