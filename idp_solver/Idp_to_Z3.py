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


from z3 import Or, Not, And, ForAll, Exists, Z3Exception, Sum, If

from idp_solver.Expression import Constructor, Expression, IfExpr, AQuantification, \
                    BinaryOperator, ADisjunction, AConjunction, \
                    AComparison, AUnary, AAggregate, \
                    AppliedSymbol, Variable, NumberConstant, Brackets, \
                    Fresh_Variable, TRUE, DSLException


# class Expression  ###########################################################

def translate(self):
    if self.value is not None:
        return self.value.translate()
    if self.simpler is not None:
        return self.simpler.translate()
    return self.translate1()

Expression.translate = translate


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
    for v in self.q_vars.values():
        v.translate()
    if not self.vars:
        return self.sub_exprs[0].translate()
    else:
        finalvars, forms = self.vars, [f.translate() for f in self.sub_exprs]

        if self.q == '∀':
            forms = And(forms) if 1 < len(forms) else forms[0]
            if len(finalvars) > 0:  # not fully expanded !
                forms = ForAll([v.translate() for v in finalvars], forms)
        else:
            forms = Or(forms) if 1 < len(forms) else forms[0]
            if len(finalvars) > 0:  # not fully expanded !
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
            raise DSLException("{}{}{}".format(str(x),
                               self.operator[i - 1], str(y)))
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
    out = self.sub_exprs[0].translate()
    function = AUnary.MAP[self.operator]
    return function(out)


AUnary.translate1 = translate1


# Class AAggregate  #######################################################

def translate1(self):
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
        assert len(self.sub_exprs) == self.decl.arity, \
            f"Incorrect number of arguments for {self.s.name}"
        if len(self.sub_exprs) == 0:
            return self.decl.translate()
        else:
            arg = [x.translate() for x in self.sub_exprs]
            # assert  all(a != None for a in arg)
            return (self.decl.translate())(arg)


AppliedSymbol.translate1 = translate1


# Class Variable  #######################################################

def translate1(self):
    return self.decl.translate()


Variable.translate1 = translate1


# Class Fresh_Variable  #######################################################

def translate(self):
    return self.translated


Fresh_Variable.translate = translate


# Class NumberConstant  #######################################################

def translate(self):
    return self.translated


NumberConstant.translate = translate


# Class Brackets  #######################################################

def translate1(self):
    return self.sub_exprs[0].translate()


Brackets.translate1 = translate1


Done = True
