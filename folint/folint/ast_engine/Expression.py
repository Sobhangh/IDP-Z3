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

# help functies voor SCA
#####################################################
def type_symbol_to_str(type1):    # zet type symbol om in str
    if type1.name == "ℤ":
        return "Int"
    if type1.name == "𝔹":
        return "Bool"
    if type1.name == "ℝ":
        return "Real"
    return type1
def builtIn_type(elem):     #kijkt of het meegegeven type builtIn type is (return true or false)
    listOfSbuildIn = ["ℤ" , "𝔹", "ℝ", "Int", "Bool", "Real", "Date"]
    return elem in listOfSbuildIn
"""
types vergelijken : 4 categorieen
    (1) Dezelfde types
    (2) Niet dezelfde types maar mogen vergeleken worden
    (3) Niet dezelfde types en mogen NIET vergeleken worden maar kunnen toch vergeleken worden
    (4) Niet dezelfde types en mogen NIET vergeleken worden en kunnen NIET vergeleken worden
"""
def typesVergelijken(type1,type2):
    if ((type1=="Int" and type2=="Real") or (type1=="Real" and type2=="Int")):  #soort (2)
        return 2
    if (not(builtIn_type(type1)) and builtIn_type(type2)) or (builtIn_type(type1) and not(builtIn_type(type2))):  #als geen specifieker type gevonden is
        return 3
    if not(builtIn_type(type1)) and not(builtIn_type(type2)):
        return 4
    WarMetBool = ["Int","Real"]
    if (type1=="Bool" and (type2 in WarMetBool)):
        return 3
    WarMetInt = ["Bool","Date"]
    if ((type1=="Int") and (type2 in WarMetInt)):
        return 3
    WarMetReal = ["Bool"]
    if (type1=="Real" and  (type2 in WarMetReal)):
        return 3
    WarMetDate = ["Int"]
    if (type1=="Date" and  (type2 in WarMetDate)):
        return 3
    return 4
##################################################

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

## class Set_(Expression):

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

def SCA_Check(self, detections):
    for i in range(0,len(self.sub_exprs)):
        l_type = self.sub_exprs[i].get_type()
        r_type = self.sub_exprs[i-1].get_type()
        if l_type is None or r_type is None:
            continue
        if (l_type == "𝔹" and r_type == "𝔹"):
            detections.append((self,f"Cannot sum or subtract Bools","Error"))
            break

        lijst = ["Int","Real","Bool"]
        if not(type_symbol_to_str(r_type) in lijst):
            detections.append((self,f"Wrong type '{type_symbol_to_str(self.sub_exprs[i-1].get_type())}' used in sum or difference ","Error"))

        if r_type != l_type:
            type1 = type_symbol_to_str(r_type)
            type2 = type_symbol_to_str(l_type)
            if ((type1=="Int" and type2=="Real") or (type1=="Real" and type2=="Int")):      #types Int en Real mogen met elkaar opgeteld of afgetrokken worden
                continue
            else:
                detections.append((self,f"Sum or difference of elements with possible incompatible types: {type1} and {type2}","Warning"))
                break

    return Operator.SCA_Check(self, detections)
ASumMinus.SCA_Check = SCA_Check


## class AMultDiv(Operator):

def SCA_Check(self, detections):
    for i in range(0,len(self.sub_exprs)):
        # multi/div of 2 "Bool" is not possible (error)
        if (self.sub_exprs[i].get_type()=="𝔹" and self.sub_exprs[i-1].get_type()=="𝔹"):
            detections.append((self,f"Multiplication or division of two elements of type Bool","Error"))
        lijst = ["Int","Real","Bool"]
        # multi/div only possible with "Int","Real" and "Bool" or numerical
        # subtypes.
        if not(type_symbol_to_str(self.sub_exprs[i-1].get_type()) in lijst):
            detections.append((self.sub_exprs[i-1],f"Type '{type_symbol_to_str(self.sub_exprs[i-1].get_type())}' might not be allowed in multiplication or divison ","Warning"))
        if self.sub_exprs[i].get_type() != self.sub_exprs[0].get_type():        #vermenigvuldigen of delen van elementen van verschillende types
            type1 = type_symbol_to_str(self.sub_exprs[i-1].get_type())
            type2 = type_symbol_to_str(self.sub_exprs[i].get_type())
            if ((type1=="Int" and type2=="Real") or (type1=="Real" and type2=="Int")):      #vermenigvuldigen of delen tss met int en Real mag
                continue
            else:
                detections.append((self,f"Multiplication or division of elements with possible incompatible types: {type1} and {type2}","Warning"))
                break
    return Operator.SCA_Check(self, detections)
AMultDiv.SCA_Check = SCA_Check


## class APower(Operator):
#TODO ?


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

def SCA_Check(self,detections):
    # Check for the correct number of arguments.
    if self.decl and self.decl.arity != len(self.sub_exprs):
        if self.code != str(self.original):
            if abs(self.decl.arity - len(self.sub_exprs))!=1:  # For definitions
                detections.append((self,f"Wrong number of arguments: given {len(self.sub_exprs)} but expected {self.decl.arity}","Error"))
        else:
            detections.append((self,f"Wrong number of arguments: given {len(self.sub_exprs)} but expected {self.decl.arity}","Error"))
    elif self.decl:
        # For each argument, find the expected type and the found type.
        # We make a distinction between normal types, partial functions and
        # constructors.
        for i in range(self.decl.arity):
            expected_type = self.decl.domains[i]
            found_type = None

            if (hasattr(self.sub_exprs[i], 'sort') and
                    self.sub_exprs[i].sort and
                    len(self.sub_exprs[i].sort.decl.domains) >= 1 and
                    isinstance(self.sub_exprs[i].sort.decl.domains[0], Set_)):
                # In the case of a partial function interpretation, the type is actually
                # the argument.
                # found_type = str(self.sub_exprs[i].sort.decl.domains[i])
                continue
                found_type = self.sub_exprs[i].get_type() #TODO dead code ?
            elif not hasattr(self.sub_exprs[i], 'name'):
                continue
            else:
                # Otherwise, it's just the type.
                found_type = self.sub_exprs[i].get_type()

            if expected_type != found_type:
                if not found_type:
                    if isinstance(self.sub_exprs[i], (ASumMinus, AMultDiv)):
                        detections.append((self, f"Could not derive type of {self.sub_exprs[i]} (formula with different types)","Warning"))
                    else:
                        detections.append((self, f"Could not derive type of {self.sub_exprs[i]}","Warning"))
                else :
                    detections.append((self, f"Argument of wrong type: expected type '{type_symbol_to_str(expected_type)}' but given type '{type_symbol_to_str(found_type)}'","Error"))
                break #so only 1 error message

    # check if elementen in enumeratie are of correct type, vb Lijn() in {Belgie}. expected type Kleur, Belgie is of type Land
    if self.is_enumeration =='in':
        for i in self.in_enumeration.tuples :
            if self.decl.codomain != i.args[0].get_type():
                detections.append((i.args[0],
                    f"Element of wrong type : "
                    f"expected type= {type_symbol_to_str(self.decl.codomain)} "
                    f"but given type= {type_symbol_to_str(i.args[0].get_type())}"
                    ,"Error"))
                break

    Expression.SCA_Check(self, detections)
AppliedSymbol.SCA_Check = SCA_Check

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
