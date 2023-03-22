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
    # Check the defined functions, predicates, constants and propositions

    # If the symbol is a type, do nothing.
    out_type = self.symbol.decl.out
    if self.is_type_enumeration:
        return

    # The symbol is a function.
    elif isinstance(self.enumeration, FunctionEnum):
        # Create a list containing the possible output values.
        # This is left None if the output type is an Int or Real.
        out_type_values = None
        if out_type.name not in ['ℤ', 'ℝ']:
            if out_type.decl.enumeration is None:
                # Type interpretation in Struct.
                out_type_values = list(self.parent.interpretations.get(out_type.str, []).enumeration.tuples.keys())
            else:
                # Type interpretation in Voc.
                out_type_values = list(out_type.decl.enumeration.tuples.keys())

        # Create a list containing all possible input arguments (to check
        # the totality of the interpretation)
        options = []
        for i in self.symbol.decl.sorts:    # Get all values of the argument types
            if i.decl.enumeration is None:
                # Type interpretation in Structure
                in_type_values = list(self.parent.interpretations.get(i.str, []).enumeration.tuples.keys())
            else:
                # Type interpretation in the vocabulary.
                in_type_values = list(i.decl.enumeration.tuples.keys())
            options.append(in_type_values)

        # possibilities = old_list
        possibilities = [list(x) for x in list(itertools.product(*options))]
        duplicates = []
        for t in self.enumeration.tuples:
            # Check if the output element is of correct type.
            if out_type.name == 'ℝ':
                if t.value.type not in ['ℝ', 'ℤ']:
                    err_str = (f'Output element {str(t.value)} should be Real')
                    detections.append((t.value, err_str, "Error"))

            elif out_type.name == 'ℤ':
                if t.value.type == 'ℝ':
                    err_str = (f'Output element {str(t.value)} should be Int')
                    detections.append((t.value, err_str, "Error"))

            else:
                if str(t.value) not in out_type_values:  # Used an output element of wrong type
                    detections.append((t.value, f"Output element of wrong type, {str(t.value)}", "Error"))

            elements = []
            for i in range(0, len(t.args)-1, 1):  # Get input elements
                if (i < len(options) and (str(t.args[i]) not in options[i])):
                    detections.append((t.args[i], f"Element of wrong type, {str(t.args[i])}", "Error"))  # Element of wrong type used
                elements.append(str(t.args[i]))
            if len(t.args) > self.symbol.decl.arity+1:    # Given to much input elements
                detections.append((t.args[0], f"Too many input elements, expected {self.symbol.decl.arity}", "Error"))
            elif elements in possibilities:     # Valid possiblity
                possibilities.remove(elements)  # Remove used possibility out of list
                duplicates.append(elements)     # Add used possibility to list to detect duplicates
            elif (self.symbol.decl.arity == 1 and elements[0] in possibilities):  # Function with 1 input element, valid possibility
                possibilities.remove(elements[0])   # Remove used possibility out of list
                duplicates.append(elements[0])      # Add used possibility to list to detect duplicates
            elif (elements in duplicates or elements[0] in duplicates): # Duplicate
                detections.append((t.args[0], "Wrong input elements, duplicate", "Error"))

        if len(possibilities) > 0:
            detections.append((self, f"Function not totally defined, missing {possibilities}", "Error"))

    # Symbol is a predicate of arity > 0
    elif self.symbol.decl.arity > 0:
        options = []
        for i in self.symbol.decl.sorts:
            # Get all values of the argument types
            if i.decl.enumeration is None:
                # Interpretation in Struct
                in_type_values = list(self.parent.interpretations.get(i.str, []).enumeration.tuples.keys())
            else:
                # Interpretation in Voc
                in_type_values = list(i.decl.enumeration.tuples.keys())
            options.append(in_type_values)
        for t in self.enumeration.tuples:
            if len(t.args) > self.symbol.decl.arity:    # Given to much input elements
                detections.append((t.args[0], f"Too many input elements, expected {self.symbol.decl.arity}", "Error"))
            else:
                for i in range(0, len(t.args), 1):  # Get elements
                    if str(t.args[i]) not in options[i]:
                        detections.append((t.args[i], "Element of wrong type", "Error"))  # Element of wrong type used in predicate

    # Symbol is a proposition (no check necessary).
    elif out_type.name == '𝔹':
        return

    # Symbol is a constant.
    else:
        # If the output is not a built-in type, check if it is correct.
        if hasattr(out_type.decl, 'enumeration'):
            # Output type is no built-in type
            if out_type.decl.enumeration is None:
                # Type interpertation in Struct.
                out_type_values = list(self.parent.interpretations.get(out_type.str, []).enumeration.tuples.keys())
            else:
                # Type interpretation in Voc.
                out_type_values = list(out_type.decl.enumeration.tuples.keys())

            if self.default.str not in out_type_values:
                detections.append((self.default, "Element of wrong type", "Error"))  # Element of wrong type used


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
