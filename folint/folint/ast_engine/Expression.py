# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
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

from idp_engine.Expression import *


### class ASTNode(object):

def SCA_Check(self,detections):
    return
    # print("SCA check:"+type(self).__name__+": ",self)
ASTNode.SCA_Check = SCA_Check


## class Annotations(ASTNode):
## class Constructor(ASTNode):
## class Accessor(ASTNode):

## class Expression(ASTNode):

def SCA_Check(self,detections):
    for sub in self.sub_exprs:
        sub.SCA_Check(detections)
Expression.SCA_Check = SCA_Check

## class SetName(Expression):

##  class AIfExpr(Expression):

## class Quantee(Expression):
## class AQuantification(Expression):

def SCA_Check(self, detections):
    vars = set()
    # First, get all variables in quantification. (E.g. 'x' for !x in Type)
    for q in self.quantees:
        for q2 in q.vars:
            vars.add(q2[0].str)
    if self.f.variables != vars and self.f.variables is not None:
        # Detect unused variables.
        set3 = vars - set(self.f.variables)
        while len(set3) > 0:
            # Search all unused variables.
            a = set3.pop()
            for q in self.quantees:
                for q2 in q.vars:
                    if q2[0].str == a:
                        detections.append((q2[0],f"Unused variable {q2[0].str}","Warning"))
                        break

    if self.q == '∀':
        # Check for a common mistake.
        if (isinstance(self.f, AConjunction) or isinstance(self.f,Brackets) and isinstance(self.f.f,AConjunction)):
            detections.append((self.f,f"Common mistake, use an implication after a universal quantor instead of a conjuction ","Warning"))
    if self.q == '∃':
        # Check for a common mistake.
        if (isinstance(self.f, AImplication) or isinstance(self.f,Brackets) and isinstance(self.f.f,AImplication)):
            detections.append((self.f,f"Common mistake, use a conjuction after an existential quantor instead of an implication ","Warning"))
    if isinstance(self.f, AEquivalence):
        # Check for variables only occurring on one side of an equivalence.
        links = self.f.sub_exprs[0]
        rechts = self.f.sub_exprs[1]
        if len(links.variables) < len(vars):   #check if all vars in left part van AEquivalence
            set3 = vars - links.variables
            detections.append((self.f,f"Common mistake, variable {set3.pop()} only occuring on one side of equivalence","Warning"))
        elif len(rechts.variables) < len(vars):    #check if all vars in right part van AEquivalence
            set3 = vars - links.variables
            detections.append((self.f,f"Common mistake, variable {set3.pop()} only occuring on one side of equivalence","Warning"))

    Expression.SCA_Check(self, detections)
AQuantification.SCA_Check = SCA_Check


## class Operator(Expression):
## class AImplication(Operator):
## class AEquivalence(Operator):
## class ADisjunction(Operator):
## class AConjunction(Operator):
## class AComparison(Operator):

## class ASumMinus(Operator):
## class AMultDiv(Operator):
## class APower(Operator):


# class AUnary(Expression):

def SCA_Check(self,detections):
    # style regel: Gebruik van haakjes bij een negated in-statement
    if (isinstance(self.f, AppliedSymbol) and self.f.is_enumeration=='in'):
        if hasattr(self,"parent"):
            detections.append((self,f"Style guide check, place brackets around negated in-statement ","Warning"))

    Expression.SCA_Check(self, detections)
AUnary.SCA_Check = SCA_Check


## class AAggregate(Expression):

def SCA_Check(self,detections):
    assert self.aggtype in ["sum", "#"], "Internal error"  # min aggregates are changed by Annotate !
    if self.lambda_ == "lambda":
        detections.append((self,f"Please use the new syntax for aggregates","Warning"))
    Expression.SCA_Check(self, detections)
AAggregate.SCA_Check = SCA_Check

## class AppliedSymbol(Expression):
## class SymbolExpr(Expression)
## class UnappliedSymbol(Expression):
## class Variable(Expression):
## class Number(Expression):
## class Date(Expression):

## class Brackets(Expression):

def SCA_Check(self, detections):
    # style regel: Vermijd onnodige haakje
    if isinstance(self.f,Brackets):
        detections.append((self,f"Style guide, redundant brackets","Warning"))
    return Expression.SCA_Check(self, detections)
Brackets.SCA_Check = SCA_Check
