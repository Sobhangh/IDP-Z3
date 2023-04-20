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

Classes to parse an IDP-Z3 theory.

"""
from idp_engine.Parse import *

from operator import truediv
from click import IntRange
from copy import copy
import itertools

from .Assignments import Assignments
from .Expression import (Annotations, ASTNode, Constructor, Accessor, Symbol, SymbolExpr,
                         Expression, AIfExpr, IF, AQuantification, Type, Quantee,
                         ARImplication, AEquivalence,
                         AImplication, ADisjunction, AConjunction,
                         AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol,
                         Number, Brackets, Date, Extension,
                         Variable, TRUEC, FALSEC, TRUE, FALSE, EQUALS, AND, OR, EQUIV)
from .utils import (RESERVED_SYMBOLS, OrderedSet, NEWL, BOOL, INT, REAL, DATE, CONCEPT,
                    GOAL_SYMBOL, EXPAND, RELEVANT, ABS, IDPZ3Error,
                    CO_CONSTR_RECURSION_DEPTH, MAX_QUANTIFIER_EXPANSION)


###############
# Helper function for SCA.
def builtIn_type(elem):
    """ Check if a given element belongs to a built-in type """
    listOfSbuildIn = ["ℤ", "𝔹", "ℝ", "Concept", "Int", "Bool", "Real", "Date"]
    return elem in listOfSbuildIn
################


# class IDP(ASTNode):

def blockNameCheck(self, a):
    if hasattr(a, 'name'):
        for t in self.theories:
            if a.name == t:
                return True
        for s in self.structures:
            if a.name == s:
                return True
    return False
IDP.blockNameCheck = blockNameCheck


################################ Vocabulary  ##############################


# class Vocabulary(ASTNode):

def SCA_Check(self, detections):
    for i in self.declarations:
        i.SCA_Check(detections)
Vocabulary.SCA_Check = SCA_Check


# class TypeDeclaration(ASTNode):

def SCA_Check(self, detections):
    # style guide check : capital letter for type
    if self.name[0].islower():
        detections.append((self, "Style guide check, type name should start with a capital letter ", "Warning"))

    # check if type has interpretation, if not check if in structures the type has given an interpretation
    if (self.interpretation is None and not builtIn_type(self.name)):
        structs = self.block.idp.get_blocks(self.block.idp.structures)
        list = []
        for i in structs:
            list.append(i.name)
        for s in structs:
            if s.vocab_name == self.block.name:
                if self.name not in s.interpretations:
                    detections.append((self, f"Expected an interpretation for type {self.name} in Vocabulary {self.block.name} or Structures {list} ", "Error"))
                    break
TypeDeclaration.SCA_Check = SCA_Check


# class SymbolDeclaration(ASTNode):


def SCA_Check(self, detections):
    if self.name[0].isupper():
        detections.append((self, f"Style guide check, predicate/function name should start with a lower letter ", "Warning"))
SymbolDeclaration.SCA_Check = SCA_Check


# class VarDeclaration(ASTNode):
#TODO ?


################################ TheoryBlock  ###############################


# class TheoryBlock(ASTNode):

def SCA_Check(self, detections):
    for c in self.constraints:
        c.SCA_Check(detections)
    for d in self.definitions:
        d.SCA_Check(detections)
TheoryBlock.SCA_Check = SCA_Check


# class Definition(ASTNode):

def SCA_Check(self, detections):
    for r in self.rules:
        r.SCA_Check(detections)
Definition.SCA_Check = SCA_Check


# class Rule(ASTNode):

def SCA_Check(self, detections):
    for q in self.quantees:
        q.SCA_Check(detections)
    self.definiendum.SCA_Check(detections)
    self.body.SCA_Check(detections)
Rule.SCA_Check = SCA_Check


# Expressions : see Expression.py

################################ Structure  ###############################

# class Structure(ASTNode):

def SCA_Check(self, detections):
    for i in self.interpretations:
        self.interpretations[i].SCA_Check(detections)
Structure.SCA_Check = SCA_Check


# class SymbolInterpretation(ASTNode):


def SCA_Check(self, detections):

    if self.is_type_enumeration:  # If the symbol is a type, do nothing.
        return

    # Auxiliary function
    def check_type(value, type, values, message):
        err_str = ''
        if type.name == BOOL:
            if str(value) not in ['true', 'false']:
                err_str = (f'{message} {str(value)} should be Bool')
        elif type.name == REAL:
            if value.type not in [REAL, INT]:
                err_str = (f'{message} {str(value)} should be Real')
        elif type.name == INT:
            if value.type != INT:
                err_str = (f'{message} {str(value)} should be Int')
        elif type.name == DATE:
            if value.type != DATE:
                err_str = (f'{message} {str(value)} should be Date')
        else:
            if type and str(value) not in values:
                err_str = f"{message} of wrong type, {str(value)} should be {type.name}"
        if err_str:
                detections.append((value, err_str, "Error"))

    # options = list of list of possible values for an argument
    options = []
    for i in self.symbol.decl.sorts:
        if i.name in [BOOL, INT, REAL, DATE]:
            in_type_values = []
        elif i.decl.enumeration is None:  # Interpretation in Struct
            in_type_interpretation = self.parent.interpretations.get(i.str, [])

            if in_type_interpretation != []:
                in_type_values = list(in_type_interpretation.enumeration.tuples.keys())
            else:
                detections.append((self, f'Symbol has an uninterpreted type: "{i.str}". Cannot verify correctness.', "Error"))
                return

        else:  # Interpretation in Voc
            in_type_values = list(i.decl.enumeration.tuples.keys())
        options.append(in_type_values)

    # same logic, for out value
    out_type, out_type_values = self.symbol.decl.out, None
    if out_type.name in [BOOL, INT, REAL, DATE]:
        out_type_values = []
    elif out_type.decl.enumeration is None:
        # Type interpretation in Struct.
        out_type_interpretation = self.parent.interpretations.get(out_type.str, [])

        if out_type_interpretation != []:
            out_type_values = list(out_type_interpretation.enumeration.tuples.keys())
        else:
            detections.append((self, f'Symbol has an uninterpreted type: "{out_type.str}". Cannot verify correctness', "Error"))
            return
    else:
        # Type interpretation in Voc.
        out_type_values = list(out_type.decl.enumeration.tuples.keys())


    domain_size = 1
    for x in options:
        domain_size *= len(x)
    # possibilities = set of all possible tuples of arguments (if not too big)
    if domain_size < 1000:
        possibilities = set(tuple(x) for x in list(itertools.product(*options)))
    else:
        possibilities = set()
    duplicates = set()
    function = 1 if isinstance(self.enumeration, FunctionEnum) else 0  # to ignore the last element of the tuple
    for t in self.enumeration.tuples:
        for i in range(0, self.symbol.decl.arity):  # check each argument in tuple
            check_type(t.args[i], self.symbol.decl.sorts[i], options[i], 'Element')

        elements = tuple(str(t.args[i]) for i in range(0, self.symbol.decl.arity))
        if len(t.args) - function > self.symbol.decl.arity:
            detections.append((t.args[0], f"Too many input elements, expected {self.symbol.decl.arity}", "Error"))
        possibilities.discard(elements)
        if elements in duplicates:
            detections.append((t.args[0], "Duplicate input elements", "Error"))
        duplicates.add(elements)

    if self.default:  # for constant, or else value
        check_type(self.default, out_type, out_type_values, 'Output element')

    if isinstance(self.enumeration, FunctionEnum):
        for t in self.enumeration.tuples:  # check output of each tuple
            check_type(t.args[-1].value, out_type, out_type_values, 'Output element')

        if self.sign == "≜" and len(possibilities) > 0 and not self.default:
            detections.append((self, f"Function not totally defined, missing {str(possibilities)[:25]}", "Error"))


SymbolInterpretation.SCA_Check = SCA_Check


## class Enumeration(ASTNode):
## class FunctionEnum(Enumeration):
## class CSVEnumeration(Enumeration):
## class ConstructedFrom(Enumeration):

## class TupleIDP(ASTNode):
## class FunctionTuple(TupleIDP):
## class CSVTuple(TupleIDP):
## class Ranges(Enumeration):
## class IntRange(Ranges):
## class RealRange(Ranges):
## class DateRange(Ranges):

################################ Display  ###############################

## class Display(ASTNode):

################################ Main  ##################################

## class Procedure(ASTNode):.pystatements)}"

def SCA_Check(self, detections):
    for a in self.pystatements:
        a.SCA_Check(detections)
Procedure.SCA_Check = SCA_Check


## class Call1(ASTNode):

def SCA_Check(self, detections):
    if self.name in ["model_check", "model_expand", "model_propagate"]:
        if self.parent.name != "pretty_print":    #check if pretty_print is used
            detections.append((self, "No pretty_print used!", "Warning"))

    if self.name == "model_check":  # check if correct amount of arguments used by model_check
        if (len(self.args) > 2 or len(self.args) == 0):
            detections.append((self, f"Wrong number of arguments for model_check: given {len(self.args)} <-> expected {1} or {2}", "Error"))
        else:
            a = self.parent
            while not isinstance(a, IDP):
                # Find IDP node in parent.
                a = a.parent
            for i in self.args:
                if not a.blockNameCheck(i):
                    # Check whether the block exists.
                    detections.append((i, f"Block {i} does not exist!", "Error"))

    for a in self.args:
        a.SCA_Check(detections)
Call1.SCA_Check = SCA_Check


## class String(ASTNode):
## class PyList(ASTNode):
## class PyAssignment(ASTNode):


########################################################################
