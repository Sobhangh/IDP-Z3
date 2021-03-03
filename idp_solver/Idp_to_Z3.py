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

Translates AST tree to Z3

TODO: vocabulary

"""


from fractions import Fraction
from z3 import (Or, Not, And, ForAll, Exists, Z3Exception, Sum, If, FreshConst,
                Q, DatatypeRef, Const, BoolSort, IntSort, RealSort, Function,
                EnumSort, BoolVal)

from idp_solver.Parse import ConstructedTypeDeclaration, RangeDeclaration, SymbolDeclaration
from idp_solver.Expression import (Constructor, Expression, IfExpr,
                                   AQuantification, BinaryOperator,
                                   ADisjunction, AConjunction, AComparison,
                                   AUnary, AAggregate, AppliedSymbol,
                                   UnappliedSymbol, Number, Brackets,
                                   Variable, TRUE)
from idp_solver.utils import BOOL, INT, REAL


# class ConstructedTypeDeclaration  ###########################################################

def translate(self):
    if self.translated is None:
        if self.name == BOOL:
            self.translated = BoolSort()
            self.constructors[0].type = BOOL
            self.constructors[1].type = BOOL
            self.constructors[0].translated = BoolVal(True)
            self.constructors[1].translated = BoolVal(False)
            self.constructors[0].py_value = True
            self.constructors[1].py_value = False
        else:
            self.translated, cstrs = EnumSort(self.name, [c.name for c in
                                                        self.constructors])
            self.check(len(self.constructors) == len(cstrs), "Internal error")
            for c, c3 in zip(self.constructors, cstrs):
                c.translated = c3
                c.py_value = c3
                self.map[str(c)] = c
    return self.translated
ConstructedTypeDeclaration.translate = translate


# class RangeDeclaration  ###########################################################

def translate(self):
    if self.translated is None:
        if self.type == INT:
            self.translated = IntSort()
        else:
            self.translated = RealSort()
    return self.translated
RangeDeclaration.translate = translate


# class SymbolDeclaration  ###########################################################

def translate(self):
    if self.translated is None:
        if len(self.sorts) == 0:
            self.translated = Const(self.name, self.out.translate())
        else:

            if self.out.name == BOOL:
                types = [x.translate() for x in self.sorts]
                self.translated = Function(self.name, types + [BoolSort()])
            else:
                types = [x.translate() for x in self.sorts] + [self.out.translate()]
                self.translated = Function(self.name, types)
    return self.translated
SymbolDeclaration.translate = translate


# class Expression  ###########################################################

def translate(self):
    if self.value is not None:
        return self.value.translate()
    if self.simpler is not None:
        return self.simpler.translate()
    return self.translate1()
Expression.translate = translate

def reified(self) -> DatatypeRef:
    if self._reified is None:
        self._reified = Const(b'*'+self.code.encode(), BoolSort())
        Expression.COUNT += 1
    return self._reified
Expression.reified = reified


# class Constructor  ##########################################################

def translate(self):
    return self.translated
Constructor.translate = translate


# Class IfExpr  ###############################################################

def translate1(self):
    return If(self.sub_exprs[IfExpr.IF].translate(),
              self.sub_exprs[IfExpr.THEN].translate(),
              self.sub_exprs[IfExpr.ELSE].translate())
IfExpr.translate1 = translate1


# Class AQuantification  ######################################################


def translate1(self):
    if not self.q_vars:
        return self.sub_exprs[0].translate()
    else:
        for v in self.q_vars.values():
            v.translated = FreshConst(v.sort.decl.translate())
        finalvars = [v.translated for v in self.q_vars.values()]
        forms = [f.translate() for f in self.sub_exprs]

        if self.q == '∀':
            forms = And(forms) if 1 < len(forms) else forms[0]
            forms = ForAll(finalvars, forms)
        else:
            forms = Or(forms) if 1 < len(forms) else forms[0]
            forms = Exists(finalvars, forms)
        return forms
AQuantification.translate1 = translate1


# Class BinaryOperator  #######################################################

BinaryOperator.MAP = {'∧': lambda x, y: And(x, y),
                      '∨': lambda x, y: Or(x, y),
                      '⇒': lambda x, y: Or(Not(x), y),
                      '⇐': lambda x, y: Or(x, Not(y)),
                      '⇔': lambda x, y: x == y,
                      '+': lambda x, y: x + y,
                      '-': lambda x, y: x - y,
                      '*': lambda x, y: x * y,
                      '/': lambda x, y: x / y,
                      '%': lambda x, y: x % y,
                      '^': lambda x, y: x ** y,
                      '=': lambda x, y: x == y,
                      '<': lambda x, y: x < y,
                      '>': lambda x, y: x > y,
                      '≤': lambda x, y: x <= y,
                      '≥': lambda x, y: x >= y,
                      '≠': lambda x, y: x != y
                      }


def translate1(self):
    out = self.sub_exprs[0].translate()

    for i in range(1, len(self.sub_exprs)):
        function = BinaryOperator.MAP[self.operator[i - 1]]
        try:
            out = function(out, self.sub_exprs[i].translate())
        except Exception as e:
            raise e
    return out
BinaryOperator.translate1 = translate1


# Class ADisjunction  #######################################################

def translate1(self):
    if len(self.sub_exprs) == 1:
        out = self.sub_exprs[0].translate()
    else:
        out = Or([e.translate() for e in self.sub_exprs])
    return out
ADisjunction.translate1 = translate1


# Class AConjunction  #######################################################

def translate1(self):
    if len(self.sub_exprs) == 1:
        out = self.sub_exprs[0].translate()
    else:
        out = And([e.translate() for e in self.sub_exprs])
    return out
AConjunction.translate1 = translate1


# Class AComparison  #######################################################

def translate1(self):
    assert not self.operator == ['≠']
    # chained comparisons -> And()
    out = []
    for i in range(1, len(self.sub_exprs)):
        x = self.sub_exprs[i-1].translate()
        assert x is not None
        function = BinaryOperator.MAP[self.operator[i - 1]]
        y = self.sub_exprs[i].translate()
        assert y is not None
        try:
            out = out + [function(x, y)]
        except Z3Exception:
            self.check(False,
                       "{}{}{}".format(str(x), self.operator[i - 1], str(y)))
    if 1 < len(out):
        return And(out)
    else:
        return out[0]
AComparison.translate1 = translate1


# Class AUnary  #######################################################

AUnary.MAP = {'-': lambda x: 0 - x,
              '¬': lambda x: Not(x)
              }

def translate1(self):
    try:
        out = self.sub_exprs[0].translate()
        function = AUnary.MAP[self.operator]
        return function(out)
    except:
        self.check(False, f"Incorrect syntax {self}")
AUnary.translate1 = translate1


# Class AAggregate  #######################################################

def translate1(self):
    assert self.quantifier_is_expanded, f"Cannot expand {self.code}"
    return Sum([f.translate() for f in self.sub_exprs])
AAggregate.translate1 = translate1


# Class AppliedSymbol  #######################################################

def translate1(self):
    if self.s.name == '__relevant':
        return TRUE.translated
    if self.s.name == 'abs':
        arg = self.sub_exprs[0].translate()
        return If(arg >= 0, arg, -arg)
    else:
        try:
            self.check(len(self.sub_exprs) == self.decl.arity,
                       f"Incorrect number of arguments for {self}")
            if len(self.sub_exprs) == 0:
                return self.decl.translate()
            else:
                arg = [x.translate() for x in self.sub_exprs]
                # assert  all(a != None for a in arg)
                return (self.decl.translate())(arg)
        except AttributeError as e:
            # Using argument on symbol that has no arity.
            if str(e) == "'RangeDeclaration' object has no attribute 'arity'":
                self.check(False,
                           f"Symbol {self} does not accept an argument")
            # Unknown error.
            else:
                raise AttributeError(e)
AppliedSymbol.translate1 = translate1


# Class UnappliedSymbol  #######################################################

def translate1(self):
    assert False, "Internal error"
UnappliedSymbol.translate1 = translate


# Class Variable  #######################################################

def translate(self):
    return self.translated
Variable.translate = translate


# Class Number  #######################################################

def translate(self):
    if self.translated is None:
        ops = self.number.split("/")
        if len(ops) == 2:  # possible with str_to_IDP on Z3 value
            self.py_value = Fraction(self.number)
            self.translated = Q(self.py_value.numerator, self.py_value.denominator)
            self.type = REAL
        elif '.' in self.number:
            v = self.number if not self.number.endswith('?') else self.number[:-1]
            if "e" in v:
                self.py_value = float(eval(v))
                self.translated = self.py_value
            else:
                self.py_value = Fraction(v)
                self.translated = Q(self.py_value.numerator, self.py_value.denominator)
            self.type = REAL
        else:
            self.py_value = int(self.number)
            self.translated = self.py_value
            self.type = INT
    return self.translated
Number.translate = translate


# Class Brackets  #######################################################

def translate1(self):
    return self.sub_exprs[0].translate()
Brackets.translate1 = translate1


Done = True
