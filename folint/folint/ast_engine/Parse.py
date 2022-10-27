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
#help functies voor SCA
def builtIn_type(elem):     #kijkt of het meegegeven type builtIn type is (return true or false)
    listOfSbuildIn = ["ℤ" , "𝔹", "ℝ", "Concept", "Int", "Bool", "Real", "Date"]
    return elem in listOfSbuildIn
################


## class IDP(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    #get all vocabularies
    V = self.get_blocks(self.vocabularies)
    for v in V :
        v.printAST(spaties+3)
    #get all structures
    S = self.get_blocks(self.structures)
    for s in S :
        s.printAST(spaties+3)
    #get all theories
    T = self.get_blocks(self.theories)
    for t in T :
        t.printAST(spaties+3)
    #get all procedures
    P = self.get_blocks(self.procedures)
    for p in P :
        p.printAST(spaties+3)
IDP.printAST = printAST

def blockNameCheck(self,a) :
    if hasattr(a,'name'):
        for t in self.theories :
            if a.name == t:
                return True
        for s in self.structures :
            if a.name == s:
                return True
    return False
IDP.blockNameCheck = blockNameCheck


################################ Vocabulary  ##############################


## class Vocabulary(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+":"+self.name)
    for i in self.declarations:
        i.printAST(spaties+5)
Vocabulary.printAST = printAST

def SCA_Check(self,detections):
    for i in self.declarations:
        i.SCA_Check(detections)
Vocabulary.SCA_Check = SCA_Check


## class TypeDeclaration(ASTNode):

def printAST(self,spaties):
    if str(self) > self.name:
        print(spaties*" "+type(self).__name__+":",self)
    else :
        print(spaties*" "+type(self).__name__+":",self.name)
    for i in self.sorts:
        i.printAST(spaties+5)
    if self.interpretation is not None:
        self.interpretation.printAST(spaties+5)
TypeDeclaration.printAST = printAST

def SCA_Check(self,detections):
    # style guide check : capital letter for type
    if self.name[0].islower():
        detections.append((self,f"Style guide check, type name should start with a capital letter ","Warning"))

    # check if type has interpretation, if not check if in structures the type has given an interpretation
    if (self.interpretation is None and not(builtIn_type(self.name))):
        structs = self.block.idp.get_blocks(self.block.idp.structures)
        list =[]
        for i in structs:
            list.append(i.name)
        for s in structs :
            if s.vocab_name == self.block.name:
                if not(self.name in s.interpretations):
                    detections.append((self,f"Expected an interpretation for type {self.name} in Vocabulary {self.block.name} or Structures {list} ","Error"))
                    break
TypeDeclaration.SCA_Check = SCA_Check


## class SymbolDeclaration(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__,":",self)
    for i in self.sorts:
        i.printAST(spaties+5)
    self.out.printAST(spaties+5)
SymbolDeclaration.printAST = printAST

def SCA_Check(self,detections):
    # style regel: func/pred namen met een kleine letter
    if self.name[0].isupper():
        detections.append((self,f"Style guide check, predicate/function name should start with a lower letter ","Warning"))
SymbolDeclaration.SCA_Check = SCA_Check


## class VarDeclaration(ASTNode):
#TODO ?


################################ TheoryBlock  ###############################


## class TheoryBlock(ASTNode):
def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for c in self.constraints:
        c.printAST(spaties+5)
    for d in self.definitions:
        d.printAST(spaties+5)
TheoryBlock.printAST = printAST

def SCA_Check(self,detections):
    for c in self.constraints:
        c.SCA_Check(detections)
    for d in self.definitions:
        d.SCA_Check(detections)
TheoryBlock.SCA_Check = SCA_Check


## class Definition(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for r in self.rules:
        r.printAST(spaties+5)
Definition.printAST = printAST

def SCA_Check(self,detections):
    for r in self.rules:
        r.SCA_Check(detections)
Definition.SCA_Check = SCA_Check


## class Rule(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for q in self.quantees:
        q.printAST(spaties+5)
    self.definiendum.printAST(spaties+5)
    self.body.printAST(spaties+5)
Rule.printAST = printAST

def SCA_Check(self,detections):
    for q in self.quantees:
        q.SCA_Check(detections)
    self.definiendum.SCA_Check(detections)
    self.body.SCA_Check(detections)
Rule.SCA_Check = SCA_Check


# Expressions : see Expression.py

################################ Structure  ###############################

## class Structure(ASTNode):
def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for i in self.interpretations:
        self.interpretations[i].printAST(spaties+5)
Structure.printAST = printAST

def SCA_Check(self,detections):
    for i in self.interpretations:
        self.interpretations[i].SCA_Check(detections)
Structure.SCA_Check = SCA_Check


## class SymbolInterpretation(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self.name)
    self.enumeration.printAST(spaties+5)
SymbolInterpretation.printAST = printAST

def SCA_Check(self,detections):
    # Check the defined functions, predicates, constants and propositions
    if (not(isinstance(self.enumeration,(Ranges,FunctionEnum))) and not(self.is_type_enumeration)):   # Symbol is predicate, constant or boolean
        if self.symbol.decl.arity==0: # Symbol is constant or boolean
            out_type = self.symbol.decl.out             # Get output type
            if hasattr(out_type.decl,'enumeration'):    # Output type is no built-in type
                out_type_values = str(out_type.decl.enumeration).replace(" ", "").split(',')   # Get output type values out of Vocabulary
                if (out_type_values[0] == 'None'):       # If type interpretation not in Vocabulary, check Structure
                    out_type_values = str(self.parent.interpretations[out_type.str].enumeration).replace(" ", "").split(',')
                if self.default.str not in out_type_values:
                    detections.append((self.default,f"Element of wrong type","Error"))  # Element of wrong type used
        else : # Symbol is predicate
            options = []
            for i in self.symbol.decl.sorts:    # Get all values of the argument types
                in_type_values = str(i.decl.enumeration).replace(" ", "").split(',')
                if (in_type_values[0] != 'None'):   # Type interpretation in Vocabulary
                    options.append(in_type_values)
                else:                               # Type interpretation in Structure
                    options.append(str(self.parent.interpretations[i.str].enumeration).replace(" ", "").split(','))
            for t in self.enumeration.tuples:
                if len(t.args) > self.symbol.decl.arity:    # Given to much input elements
                    detections.append((t.args[0],f"To much input elements, expected {self.symbol.decl.arity}","Error"))
                else :
                    for i in range(0,len(t.args),1):  # Get elements
                        if str(t.args[i]) not in options[i]:
                            detections.append((t.args[i],f"Element of wrong type","Error"))  # Element of wrong type used in predicate

    if isinstance(self.enumeration, FunctionEnum):
        out_type = self.symbol.decl.out   # Get output type of function

        # Create a list containing the possible output values, left None if
        # the output type is an infinite number range.
        out_type_value = None
        if out_type.name not in ['ℤ', 'ℝ']:
            out_type_values = str(out_type.decl.enumeration).replace(" ", "").split(',')   # Get output type values out of Vocabulary
            if (out_type_values[0] == 'None'):       # If type interpretation not in Vocabulary, check Structure
                out_type_values = str(self.parent.interpretations[out_type.str].enumeration).replace(" ", "").split(',')

        # Create a list containing all possible input arguments (to check
        # the totality of the interpretation)
        options = []
        for i in self.symbol.decl.sorts:    # Get all values of the argument types
            in_type_values = str(i.decl.enumeration).replace(" ", "").split(',')
            if (in_type_values[0] != 'None'): # Type interpretation in Vocabulary
                options.append(in_type_values)
            else:                              # Type interpretation in Structure
                options.append(str(self.parent.interpretations[i.str].enumeration).replace(" ", "").split(','))

        # Determine all possible combinations
        new_list = []
        old_list = options[0]
        for i in range(1,len(options)):
            new_list = []
            for a in old_list:
                for b in options[i]:
                    hulp_element = []
                    if isinstance(a,list):
                        for c in a:
                            hulp_element.append(c)
                    else :
                        hulp_element.append(a)
                    hulp_element.append(b)
                    new_list.append(hulp_element)
            old_list = new_list

        possibilities = old_list
        duplicates = []
        for t in self.enumeration.tuples:
            # Check if the output element is of correct type.
            if out_type.name == 'ℝ':
                try:
                    float(t.value)
                except:
                    err_str = (f'Output element {str(t.value)} should be Real')
                    detections.append((t.value, err_str, "Error"))

            elif out_type.name == 'ℤ':
                try:
                    int(t.value)
                except:
                    err_str = (f'Output element {str(t.value)} should be Int')
                    detections.append((t.value, err_str, "Error"))

            else:
                if str(t.value) not in out_type_values:  # Used an output element of wrong type
                    detections.append((t.value,f"Output element of wrong type, {str(t.value)}","Error"))

            elements = []
            for i in range(0,len(t.args)-1,1):  # Get input elements
                if (i < len(options) and (str(t.args[i]) not in options[i])) :
                    detections.append((t.args[i],f"Element of wrong type, {str(t.args[i])}","Error"))  # Element of wrong type used
                elements.append(str(t.args[i]))
            if len(t.args) > self.symbol.decl.arity+1:    # Given to much input elements
                detections.append((t.args[0],f"To much input elements, expected {self.symbol.decl.arity}","Error"))
            elif elements in possibilities:     # Valid possiblity
                possibilities.remove(elements)  # Remove used possibility out of list
                duplicates.append(elements)     # Add used possibility to list to detect duplicates
            elif (self.symbol.decl.arity == 1 and elements[0] in possibilities): # Function with 1 input element, valid possibility
                possibilities.remove(elements[0])   # Remove used possibility out of list
                duplicates.append(elements[0])      # Add used possibility to list to detect duplicates
            elif (elements in duplicates or elements[0] in duplicates): # Duplicate
                    detections.append((t.args[0],f"Wrong input elements, duplicate","Error"))

        if (len(possibilities) > 0 and self.symbol.decl.arity == 1): # Function not totally defined
                detections.append((self,f"Function not total defined, missing {possibilities}","Error"))
        elif len(possibilities) > 0: # Function not totally defined
            detections.append((self,f"Function not total defined, missing elements","Error"))

    else:
        # Symbol is a function mapping an ℝ or ℤ
        pass
SymbolInterpretation.SCA_Check = SCA_Check


## class Enumeration(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for t in self.tuples:
        t.printAST(spaties+5)
Enumeration.printAST = printAST


## class FunctionEnum(Enumeration):
## class CSVEnumeration(Enumeration):
## class ConstructedFrom(Enumeration):

## class TupleIDP(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for a in self.args:
        a.printAST(spaties+5)
TupleIDP.printAST = printAST


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

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self.name)
    for a in self.pystatements:
        a.printAST(spaties+5)
Procedure.printAST = printAST

def SCA_Check(self,detections):
    for a in self.pystatements:
        a.SCA_Check(detections)
Procedure.SCA_Check = SCA_Check


## class Call1(ASTNode):

def printAST(self,spaties):
    print(spaties*" "+type(self).__name__+": ",self)
    for a in self.args:
        a.printAST(spaties+5)
Call1.printAST = printAST

def SCA_Check(self,detections):
    lijst_inferenties = ["model_check","model_expand","model_propagate"]
    if self.name in lijst_inferenties:
        if self.parent.name != "pretty_print":    #check if pretty_print is used
            detections.append((self,f"No pretty_print used!","Warning"))
    if self.name == "model_check":  #check if correct amount of arguments used by model_check
        if (len(self.args) > 2 or len(self.args) == 0):
            detections.append((self,f"Wrong number of arguments for model_check: given {len(self.args)} <-> expected {1} or {2}","Error"))
        else :
            a = self.parent
            while not(isinstance(a,IDP)):   #zoek IDP node in parent
                a = a.parent
            for i in self.args:
                if not(a.blockNameCheck(i)):   #check of block naam bestaat
                    detections.append((i,f"Block {i} does not exist!","Error"))

    for a in self.args:
        a.SCA_Check(detections)
Call1.SCA_Check = SCA_Check


## class String(ASTNode):
## class PyList(ASTNode):
## class PyAssignment(ASTNode):


########################################################################
