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

"""

Translates AST tree to Z3
TODO: vocabulary

"""


from utils import Log, nl
from z3 import DatatypeRef, FreshConst, Or, Not, And, ForAll, Exists, Z3Exception, Sum, If, Const, BoolSort, Q

from typing import List, Tuple
from Idp.Expression import use_value, Constructor, Expression, IfExpr, AQuantification, BinaryOperator, \
                    ARImplication, AEquivalence, AImplication, ADisjunction, AConjunction,  \
                    AComparison, ASumMinus, AMultDiv, APower, AUnary, AAggregate, \
                    AppliedSymbol, Variable, Symbol, NumberConstant, Brackets, Arguments, \
                    Fresh_Variable, TRUE, FALSE, ZERO


# class Constructor ############################################################


def translate(self): 
    return self.translated
Constructor.translate = translate



# Class IfExpr ################################################################

@use_value
def translate(self):
    return If(self.sub_exprs[IfExpr.IF  ].translate()
            , self.sub_exprs[IfExpr.THEN].translate()
            , self.sub_exprs[IfExpr.ELSE].translate())
IfExpr.translate = translate



# Class AQuantification #######################################################

@use_value
def translate(self):
    for v in self.q_vars.values():
        v.translate()
    if not self.vars:
        return self.sub_exprs[0].translate()
    else:
        finalvars, forms = self.vars, [f.translate() for f in self.sub_exprs]

        if self.q == '∀':
            forms = And(forms) if 1<len(forms) else forms[0]
            if len(finalvars) > 0: # not fully expanded !
                forms = ForAll(finalvars, forms)
        else:
            forms = Or(forms) if 1<len(forms) else forms[0]
            if len(finalvars) > 0: # not fully expanded !
                forms = Exists(finalvars, forms)
        return forms
AQuantification.translate = translate



# Class BinaryOperator #######################################################

BinaryOperator.MAP = { '∧': lambda x, y: And(x, y),
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

@use_value
def translate(self):
    out = self.sub_exprs[0].translate()

    for i in range(1, len(self.sub_exprs)):
        function = BinaryOperator.MAP[self.operator[i - 1]]
        out = function(out, self.sub_exprs[i].translate())
    return out
BinaryOperator.translate = translate



# Class ADisjunction #######################################################

@use_value
def translate(self):
    if len(self.sub_exprs) == 1:
        out = self.sub_exprs[0].translate()
    else:
        out = Or ([e.translate() for e in self.sub_exprs])
    return out
ADisjunction.translate = translate



# Class AConjunction #######################################################

@use_value
def translate(self):
    if len(self.sub_exprs) == 1:
        out = self.sub_exprs[0].translate()
    else:
        out = And([e.translate() for e in self.sub_exprs])
    return out
AConjunction.translate = translate


# Class AComparison #######################################################

@use_value
def translate(self):
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
        except Z3Exception as E:
            raise DSLException("{}{}{}".format(str(x), self.operator[i - 1], str(y)))
    if 1 < len(out):
        return And(out)
    else:
        return out[0]
AComparison.translate = translate



# Class AUnary #######################################################

AUnary.MAP = {'-': lambda x: 0 - x,
           '~': lambda x: Not(x)
          }
          
@use_value
def translate(self):
    out = self.sub_exprs[0].translate()
    function = AUnary.MAP[self.operator]
    return function(out)
AUnary.translate = translate


# Class AAggregate #######################################################

@use_value
def translate(self):
    return Sum([f.translate() for f in self.sub_exprs])
AAggregate.translate = translate



# Class AppliedSymbol, Variable #######################################################

@use_value
def translate(self):
    if self.s.name == 'abs':
        arg = self.sub_exprs[0].translate()
        return If(arg >= 0, arg, -arg)
    else:
        if len(self.sub_exprs) == 0:
            return self.decl.translated
        else:
            arg = [x.translate() for x in self.sub_exprs]
            #assert  all(a != None for a in arg)
            return (self.decl.translate())(arg)
AppliedSymbol.translate = translate



# Class AppliedSymbol, Variable #######################################################

@use_value
def translate(self):
    return self.decl.translated
Variable.translate = translate



# Class Fresh_Variable #######################################################

def translate(self):
    return self.translated
Fresh_Variable.translate = translate



# Class NumberConstant #######################################################
     
def translate(self):
    return self.translated
NumberConstant.translate = translate



# Class Brackets #######################################################

@use_value
def translate(self):
    return self.sub_exprs[0].translate()
Brackets.translate = translate