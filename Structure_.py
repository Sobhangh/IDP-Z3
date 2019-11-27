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
from z3 import *
import ast

class LiteralQ(object):
    def __init__(self, truth, subtence):
        self.truth = truth # Bool, "irrelevant", None = unknown, 
        self.subtence = subtence

    def __hash__(self):
        return hash((self.truth, str(self.subtence)))

    def __eq__(self, other):
        return self.truth == other.truth \
            and type(self.subtence) == type (other.subtence) \
            and str(self.subtence) == str(other.subtence)

    def __repr__(self):
        return str(self.truth) + self.subtence.reading

    def __str__(self):
        if self.truth == "irrelevant":
            return ""
        return ("" if self.truth else "? " if self.truth is None else "Not ") \
             + self.subtence.reading

    def to_json(self): return str(self)

    def asZ3(self):
        if self.truth == "irrelevant":
            return BoolVal(True)
        return self.subtence.translated if self.truth else Not(self.subtence.translated)

class Equality(object):
    def __init__(self, subtence, value):
        self.subtence = subtence # an Expression
        self.value = value # a Z3 value
        self.code = f"{subtence.code} = {str(value)}"
        self.type = 'bool'
        self.translated = (subtence.translated == value)
        self.reading = "" #TODO

    def __str__(self): return self.code

    def unknown_symbols(self):
        return self.subtence.unknown_symbols()

    
#################
# load user's choices
# see docs/REST.md
#################

def json_to_literals(idp, jsonstr):
    literals = {} # {literalQ : atomZ3} from the GUI (needed for propagate)
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
                        literalQ = LiteralQ(True, atom)
                    if "cf" in json_atom and json_atom["cf"]:
                        literalQ = LiteralQ(False, atom)
                elif json_atom["value"]:
                    if json_atom["typ"] in ["Int", "Real"]:
                        value = eval(json_atom["value"])
                    else:
                        value = idp.vocabulary.symbol_decls[json_atom["value"]].translated
                    literalQ = LiteralQ(True, Equality(atom, value))
                else:
                    literalQ = None #TODO error ?
                if literalQ is not None:
                    literals[literalQ] = literalQ.asZ3()
    return literals


#################
# response to client
# see docs/REST.md
#################

def model_to_json(idp, s, reify):
    m = s.model()
    out = Structure_(idp)
    for atom in idp.atoms.values():
        # atom might not have an interpretation in model (if "don't care")
        value = m.eval(reify[atom], model_completion=True)
        if atom.type == 'bool':
            if not (is_true(value) or is_false(value)):
                #TODO value may be an expression, e.g. for quantified expression --> assert a value ?
                print("*** ", atom.reading, " is not defined, and assumed false")
            out.addAtom(atom, True if is_true(value) else False)
        else: #TODO check that value is numeric ?
            out.addAtom(Equality(atom, value), True)
    return out.m


class Structure_(object):
    def __init__(self, idp, structure=[]):
        self.m = {}

        def initialise(atom, ct_true, ct_false, value=""):
            atomZ3 = atom.translated #TODO
            key = atom.code
            typ = atomZ3.sort().name()
            for symb in atom.unknown_symbols().values():
                s = self.m.setdefault(symb.name, {})
                if typ == 'Bool':
                    symbol = {"typ": typ, "ct": ct_true, "cf": ct_false}
                elif 0 < len(symb.range):
                    symbol = { "typ": typ, "value": str(value)
                            , "values": [str(v) for v in symb.range]}
                elif typ in ["Real", "Int"]:
                    symbol = {"typ": typ, "value": str(value)} # default
                else:
                    symbol = None
                if symbol: 
                    symbol['reading'] = atom.reading
                    symbol['normal'] = hasattr(atom, 'normal')
                    s.setdefault(key, symbol)
                    break

        for atom in idp.atoms.values():
            initialise(atom, False, False, "")
        for ass in structure: # add numeric input for Explain
            initialise(ass.subtence, False, False, "")  


    def addAtom(self, atom, truth):
        if truth and type(atom) == Equality:
            symbol = atom.subtence.translated
            key = atom.subtence.code
            typ = symbol.sort().name()
            for name, symb in atom.subtence.unknown_symbols().items():
                s = self.m.setdefault(name, {})
                if key in s:
                    if typ in ["Real", "Int"]:
                        s[key]["value"] = str(eval(str(atom.value).replace('?', ''))) # compute fraction
                    elif 0 < len(symb.range): #TODO and type(atom) != IfExpr:
                        s[key]["value"] = str(atom.value)
        if atom.type != 'bool': return
        key = atom.code
        for symb in atom.unknown_symbols().keys():
            s = self.m.setdefault(symb, {})
            if key in s:
                if truth is None: s[key]["unknown"] = True
                else:
                    s[key]["ct" if truth else "cf"] = True
                s[key]['reading'] = atom.reading

