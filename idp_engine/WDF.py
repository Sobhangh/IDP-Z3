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

from .utils import CONCEPT


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
    e.check((r1 == r2 for r1, r2 in zip (s1.root_set, s2.root_set)), msg)  # not disjoint
    if len(s1.root_set) == 0:  #  --> s2(), i.e., () is in s2
        symbol = SymbolExpr.make(s2.decl)
        return AppliedSymbol.make(symbol, [])
    if type(s1.decl) == TypeDeclaration:
        # must be two numeric predicates --> s2(e), i.e., e is in s2
        symbol = SymbolExpr.make(s2.decl)
        return AppliedSymbol.make(symbol, [e])
    if s1.name == CONCEPT:  # Concept[sig] <: Concept
        e.check(s2.name == CONCEPT and len(s2.concept_domains) == 0, msg)
        return TRUE
    e.check(len(s1.decl.domains) > 0, msg)  # s1 = {()} = s2 = {()}
    # go up the hierarchy
    if len(s1.decl.domains) == 1:  #
        return is_subset_of(e, s1.decl.domains[0], s2)
    s1.check(False, f"can't compare cross-product of sets")
    return FALSE  # dead code for mypy


# Class Expression  #######################################################

def fill_WDF(self):
    for e in self.sub_exprs:
        e.fill_WDF()
    self.merge_WDFs()
Expression.fill_WDF = fill_WDF

def merge_WDFs(self):
    wdfs = [e.WDF if e.WDF else TRUE for e in self.sub_exprs]
    self.WDF = AND(wdfs)
    return self
Expression.merge_WDFs = merge_WDFs


# Class AIfExpr  #######################################################

def merge_WDFs(self):
    if all(e.WDF for e in self.sub_exprs):
        self.WDF = AND([
            self.sub_exprs[0].WDF,
            resimplify(IF(self.sub_exprs[0], self.sub_exprs[1].WDF,
                                  self.sub_exprs[2].WDF))])
    else:
        self.WDF = None
    return self
AIfExpr.merge_WDFs = merge_WDFs


# Class AQuantification  #######################################################

def merge_WDFs(self):
    assert len(self.sub_exprs) == 1, "Internal error"
    if self.sub_exprs[0].WDF:
        forall = FORALL(self.quantees, self.sub_exprs[0].WDF).simplify1()
        self.WDF = AND([q.WDF for q in self.quantees] + [forall])
    else:
        self.WDF = None
    return self
AQuantification.merge_WDFs = merge_WDFs


# Class ADisjunction  #######################################################

def merge_WDFs(self):
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
            out = AND([e.WDF, resimplify(OR([e, out]))])  #
    self.WDF = out
    return self
ADisjunction.merge_WDFs = merge_WDFs

def resimplify(expr: Expression) -> Expression:
    """Simplifies a disjunction by returning TRUE when it has p or not p."""
    if not isinstance(expr, ADisjunction):
        return expr
    positive, negative = set(), set()
    for e in expr.sub_exprs:
        if isinstance(e, AUnary):
            negative.add(e.sub_exprs[0].code)
        else:
            positive.add(e.code)
    exclude = positive.intersection(negative)
    if exclude:
        return TRUE
    else:
        out = OR([e for e in expr.sub_exprs
                if not (e.code in exclude
                        or (isinstance(e, AUnary) and e.sub_exprs[0].code in exclude))])
        return out


# Class AImplication, AConjunction  #######################################################

def merge_WDFs(self):
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
            out = AND([e.WDF, resimplify(OR([NOT(e), out]))])  #
    self.WDF = out
    return self
AConjunction.merge_WDFs = merge_WDFs
AImplication.merge_WDFs = merge_WDFs


# Class AppliedSymbol  #######################################################

def merge_WDFs(self):
    wdfs = [e.WDF if e.WDF else TRUE for e in self.sub_exprs]
    if self.symbol.decl:  # known symbol
        self.WDF = AND(wdfs)
        if type(self.symbol.decl) != TypeDeclaration:
            if self.sub_exprs:
                wdf2 = AND([self.WDF]+[is_subset_of(e, e.type, d)
                            for e, d in zip(self.sub_exprs, self.symbol.decl.domains)])
            else:  # constant c()
                wdf2 = TRUE
            self.WDF = AND([self.WDF, wdf2])
        self.WDF.original = self
    elif self.symbol.WDF:  # $(.)(..)
        self.WDF = AND([self.symbol.WDF] + wdfs)
    else:
        self.WDF = AND(wdfs)
    return self
AppliedSymbol.merge_WDFs = merge_WDFs


Done = True
