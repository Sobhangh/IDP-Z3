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
"""

Methods to compute the Well-definedness condition of an Expression.

"""
from __future__ import annotations
from copy import copy
from typing import List

from .Parse import TypeDeclaration
from .Expression import (ASTNode, Expression, SETNAME, SetName,
                         BOOL_SETNAME, INT_SETNAME, REAL_SETNAME, DATE_SETNAME,
                         Constructor, CONSTRUCTOR, AIfExpr, IF,
                         AQuantification, Quantee, ARImplication, AImplication,
                         AEquivalence, AConjunction, ADisjunction,
                         Operator, AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol, Variable,
                         VARIABLE, Brackets, SymbolExpr, Number, NOT,
                         EQUALS, AND, OR, TRUE, FALSE, ZERO, IMPLIES, FORALL, EXISTS)
from .utils import CONCEPT, OrderedSet, flatten


def is_subset_of(e: Expression,
                 s1: SetName,
                 s2: SetName
                 ) -> Expression:
    """ Returns a formula that is true when Expression e (of type s1) is necessarily in the set s2.

    Essentially, it goes up the hierarchy of s1 until s2 is found.
    It raises an error if the formula is FALSE.
    """
    if s1 == s2:
        return TRUE
    msg = f"Not in domain: {e} (of type {s1.name}) is not in {s2.name}"
    e.check(all(r1 == r2 for r1, r2 in zip (s1.root_set, s2.root_set)), msg)  # not disjoint
    if len(s1.root_set) == 0:  #  --> s2(), i.e., () is in s2
        symbol = SymbolExpr.make(s2.decl)
        app = AppliedSymbol.make(symbol, []).fill_WDF()
        return And([app.WDF, app])
    if type(s1.decl) == TypeDeclaration:
        # must be two numeric predicates --> s2(e), i.e., e is in s2
        symbol = SymbolExpr.make(s2.decl)
        app = AppliedSymbol.make(symbol, [e]).fill_WDF()
        return And([app.WDF, app])
    if s1.name == CONCEPT:  # Concept[sig] <: Concept
        e.check(s2.name == CONCEPT and len(s2.concept_domains) == 0, msg)
        return TRUE
    e.check(len(s1.decl.domains) > 0, msg)  # s1 = {()} = s2 = {()}
    # go up the hierarchy
    if len(s1.decl.domains) == 1:  #
        return is_subset_of(e, s1.decl.domains[0], s2)
    s1.check(False, f"can't compare cross-product of sets")
    return FALSE  # dead code for mypy


# WDF constructors  #######################################################

def If(if_: Expression, then_: Expression, else_: Expression) -> Expression:
    """ Create a simplified If"""
    out = IF(if_, then_, else_)
    if isinstance(out, ADisjunction):
        return Or(out.sub_exprs)
    return out


def And(sub_exprs: List[Expression]) -> Expression:
    """ Create a simplified conjunction"""
    out = OrderedSet()  # remove duplicates
    for e in sub_exprs:
        if isinstance(e, AConjunction):  # flatten p & (q & r)
            for ee in e.sub_exprs:
                out.append(ee)
        else:
            out.append(e)
    return AND([e for e in out.values()])


def Or(sub_exprs: List[Expression]) -> Expression:
    """ Create a simplified disjunction"""
    exprs = OrderedSet()  # remove duplicates
    if isinstance(sub_exprs[-1], AConjunction): # a|(b&c) -> (a|b) & (a|c)
        return And( Or(sub_exprs[:-1] + [e])
                   for e in sub_exprs[-1].sub_exprs)
    for e in sub_exprs:
        if isinstance(e, ADisjunction):  # flatten p | (q | r)
            for ee in e.sub_exprs:
                exprs.append(ee)
        else:
            exprs.append(e)
    # remove p | ~p
    positive, negative = set(), set()
    for e in exprs.values():
        if isinstance(e, AUnary):
            negative.add(e.sub_exprs[0].code)
        else:
            positive.add(e.code)
    exclude = positive.intersection(negative)
    if exclude:
        return TRUE
    else:
        out = OR([e for e in exprs.values()
                if not (e.code in exclude
                        or (isinstance(e, AUnary) and e.sub_exprs[0].code in exclude))])
        return out

def Forall(qs: List[Quantee], expr: Expression) -> Expression:
    # move quantifications upward
    # !x: a&(!y:b)&c   --> !x: !y: a&b&..
    if isinstance(expr, Operator):
        for i, e in enumerate(expr.sub_exprs):
            if type(e) == AQuantification and e.q == "∀":  # e = (!y:b)
                inner_vars = set(*flatten((q.vars for q in e.quantees)))
                if inner_vars.isdisjoint(expr.variables):  # x != y
                    new_expr = copy(expr.sub_exprs)  # new_exprs = a&b&c
                    new_expr[i] = e.sub_exprs[0]
                    if type(expr) == AConjunction:
                        new_expr = And(new_expr)
                    elif type(expr) == ADisjunction:
                        new_expr = Or(new_expr)
                    expr = Forall(e.quantees, new_expr)  # !y: a&b&c
                    break
    return FORALL(qs, expr).simplify1()

def Not(e: Expression) -> Expression:
    """ Create a simplified negation"""
    if isinstance(e, AConjunction):  # ~(p & q)  -->  ~p | ~q
        return Or([Not(ee) for ee in e.sub_exprs])
    if isinstance(e, ADisjunction):  # ~(p | q)  -->  ~p & ~q
        return And([Not(ee) for ee in e.sub_exprs])
    if isinstance(e, AUnary):  # ~(~p))  -->  p
        return e.sub_exprs[0]
    return NOT(e)


# Class Expression  #######################################################

def fill_WDF(self: Expression) -> Expression:
    for e in self.sub_exprs:
        e.fill_WDF()
    return self.merge_WDFs()
Expression.fill_WDF = fill_WDF

def merge_WDFs(self: Expression) -> Expression:
    wdfs = [e.WDF if e.WDF else TRUE for e in self.sub_exprs]
    self.WDF = And(wdfs)
    return self
Expression.merge_WDFs = merge_WDFs


# Class AIfExpr  #######################################################

def merge_WDFs(self):
    # WDF(if(a,b,c)) is WDF(a) & if(a, WDF(b), WDF(c))
    if all(e.WDF for e in self.sub_exprs):
        self.WDF = And([self.sub_exprs[0].WDF,
                        If(self.sub_exprs[0], self.sub_exprs[1].WDF,
                                            self.sub_exprs[2].WDF)])
    else:
        self.WDF = None
    return self
AIfExpr.merge_WDFs = merge_WDFs


# Class AQuantification, AAggregate  #######################################################

def merge_WDFs(self):
    if len(self.sub_exprs) == 1:  # not a min/max aggregate
        # WDF(!x in p: phi)  = WDF(p) & !x in p: WDF(phi)
        if self.sub_exprs[0].WDF:
            forall = Forall(self.quantees, self.sub_exprs[0].WDF)
            self.WDF = And([q.WDF for q in self.quantees] + [forall])
        else:
            self.WDF = None
    else:
        # WDF(min{f|x in p: phi}) = WDF(p) & !x in p: WDF(phi) & (~phi | WDF(f))
        wdfs = [e.WDF if e.WDF else TRUE for e in self.sub_exprs]
        condition = And([wdfs[1], Or([Not(self.sub_exprs[1]), wdfs[0]])])
        forall = Forall(self.quantees, condition)
        self.WDF = And([q.WDF for q in self.quantees] + [forall])
    return self
AQuantification.merge_WDFs = merge_WDFs
AAggregate.merge_WDFs = merge_WDFs


# Class ADisjunction  #######################################################

def merge_WDFs(self):
    # WDF(p | q) = (WDF(p) & p) | (WDF(p) & WDF(q))
    # if WDF(q) is true, this becomes WDF(p)
    out, testing = TRUE, False
    for e in reversed(self.sub_exprs):
        if not e.WDF:
            continue
        if not testing:
            if e.WDF.same_as(TRUE):
                continue
            else:
                out, testing = e.WDF, True
        else:
            out = Or([And([e.WDF, e]), And([e.WDF, out])])
    self.WDF = out
    return self
ADisjunction.merge_WDFs = merge_WDFs


# Class AImplication, AConjunction  #######################################################

def merge_WDFs(self):
    # WDF(p & q) = (WDF(p) & ~p) | (WDF(p) & WDF(q))
    # if WDF(q) is true, this becomes WDF(p)
    out, testing = TRUE, False
    for e in reversed(self.sub_exprs):
        if not e.WDF:
            continue
        if not testing:
            if e.WDF.same_as(TRUE):
                continue
            else:
                out, testing = e.WDF, True
        else:
            out = Or([And([e.WDF, Not(e)]), And([e.WDF, out])])  #
    self.WDF = out
    return self
AConjunction.merge_WDFs = merge_WDFs
AImplication.merge_WDFs = merge_WDFs


# Class AMultDiv  #######################################################

def merge_WDFs(self):
    # WDF(f*g/h) = WDF(f) & WDF(g) & WDF(h) & h ~= 0
    wdfs = [e.WDF if e.WDF else TRUE for e in self.sub_exprs]
    self.WDF = And(wdfs)
    for i, op in enumerate(self.operator):
        self.check(op != "/" or i == len(self.sub_exprs)-2,
                   f"Division must be the last operation in {self.code}")
    if self.operator[-1] == "/":
        self.WDF = And([NOT(EQUALS([self.sub_exprs[-1], ZERO])), self.WDF])
    return self
AMultDiv.merge_WDFs = merge_WDFs


# Class AppliedSymbol  #######################################################

def merge_WDFs(self):
    # WDF(p(a, b)) = WDF(p) & WDF(a) & WDF(b) & dom(p)(a,b)
    wdfs = [e.WDF or TRUE for e in self.sub_exprs]
    wdf1 = self.symbol.WDF or TRUE

    #  wdf2 = WDF for the domain of self
    if self.symbol.decl:  # known symbol
        domains = self.symbol.decl.domains
    else:  # $(..)
        domains = self.symbol.sub_exprs[0].type.concept_domains
    if not self.symbol.decl or type(self.symbol.decl) != TypeDeclaration:
        if self.sub_exprs:
            wdf2 = And([is_subset_of(e, e.type, d)
                        for e, d in zip(self.sub_exprs, domains)])
        elif domains:  #  partial constant
            symbol = SymbolExpr.make(domains[0].decl)
            wdf2 = AppliedSymbol.make(symbol, [])
        else:  # constant c()
            wdf2 = TRUE
    else:
        wdf2 = TRUE
    self.WDF = AND([wdf1, wdf2]+wdfs)
    return self
AppliedSymbol.merge_WDFs = merge_WDFs


Done = True
