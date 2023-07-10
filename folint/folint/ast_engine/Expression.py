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
    if type1 == "ℤ":
        return "Int"
    if type1 == "𝔹":
        return "Bool"
    if type1 == "ℝ":
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

## class Symbol(Expression):
## class Subtype(Symbol):

##  class AIfExpr(Expression):

def get_type(self):
    return self.then_f.type
AIfExpr.get_type = get_type


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

def get_type(self):
    return self.type    #return type of Operator and subclasses (in 'str')
Operator.get_type = get_type


## class AImplication(Operator):
## class AEquivalence(Operator):
## class ADisjunction(Operator):
## class AConjunction(Operator):


## class AComparison(Operator):

def SCA_Check(self,detections):
    """ Compare types: 4 categories
        (1) Both are the same type
        (2) They are different, but can be compared (e.g. Int <> Real)
        (3) Cannot be compared, but are allowed by IDP-Z3. This also
        happens when a numerical type is interpreted in the structure (warning)
        (4) Cannot be compared at all. (error)
    """
    # Get types and convert to String.
    type1 = self.sub_exprs[0].get_type()
    type2 = self.sub_exprs[1].get_type()
    type1 = type_symbol_to_str(type1)
    type2 = type_symbol_to_str(type2)

    if type1 != type2:  # Cat 2, 3 and 4
        if type1 is None:
            detections.append((self.sub_exprs[0],f"Could not determine the type of {self.sub_exprs[0]} ","Warning"))
        elif type2 is None:
            detections.append((self.sub_exprs[1],f"Could not determine the type of {self.sub_exprs[1]} ","Warning"))
        else:
            cat = typesVergelijken(type1,type2)
            if cat == 3:  #cat(3) WARNING
                detections.append((self,f"Comparison of 2 possibly incompatible types: {type1} and {type2}","Warning"))
            if cat == 4:  #cat(4) ERROR
                detections.append((self,f"Comparison of 2 incompatble types: {type1} and {type2}","Error"))
    if (type1 is None and type2 is None):   #beide types zijn unknown
        detections.append((self.sub_exprs[0],f"Comparison of 2 unknown types: {type1} and {type2}","Warning"))

    Expression.SCA_Check(self, detections)
AComparison.SCA_Check = SCA_Check


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

def get_type(self):
    help = 0
    for i in range(0,len(self.sub_exprs)):
        if self.sub_exprs[i].get_type() != self.sub_exprs[0].get_type():
            help = help + 1
    if help == 0: # als alle elementen van hetzelfde type zijn return dit type
        return self.sub_exprs[0].get_type()
    else :  #elementen van versschillende types
        lijst = ["Int","Real"]
        for i in self.sub_exprs:
            if type_symbol_to_str(i.get_type()) in lijst:
                continue
            else:
                return None
        return "Int"    #als alle type van oftwel Int of Real zijn
ASumMinus.get_type = get_type


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

def get_type(self):
    help = 0
    for i in range(0,len(self.sub_exprs)):
        if self.sub_exprs[i].get_type() != self.sub_exprs[0].get_type():
            help = help + 1
    if help == 0: # als alle elementen van hetzelfde type zijn return dit type, anders return None
        return self.sub_exprs[0].get_type()
    else :  #elementen van versschillende types
        lijst = ["Int","Real"]
        for i in self.sub_exprs:
            if type_symbol_to_str(i.get_type()) in lijst:
                continue
            else:
                return None
        return "Int"    #als alle type van oftwel Int of Real zijn
AMultDiv.get_type = get_type


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

def get_type(self):
    return self.type
AUnary.get_type = get_type


## class AAggregate(Expression):

def SCA_Check(self,detections):
    assert self.aggtype in ["sum", "#"], "Internal error"  # min aggregates are changed by Annotate !
    if self.lambda_ == "lambda":
        detections.append((self,f"Please use the new syntax for aggregates","Warning"))
    Expression.SCA_Check(self, detections)
AAggregate.SCA_Check = SCA_Check

def get_type(self):
    # return "Int"        #Sum zou altijd Int moeten zijn
    return self.type    #return type of AAggregate (in 'str')
AAggregate.get_type = get_type

## class AppliedSymbol(Expression):

def SCA_Check(self,detections):
    # Check for the correct number of arguments.
    if self.decl.arity != len(self.sub_exprs):
        if self.code != str(self.original):
            if abs(self.decl.arity - len(self.sub_exprs))!=1:  # For definitions
                detections.append((self,f"Wrong number of arguments: given {len(self.sub_exprs)} but expected {self.decl.arity}","Error"))
        else:
            detections.append((self,f"Wrong number of arguments: given {len(self.sub_exprs)} but expected {self.decl.arity}","Error"))
    else:
        # For each argument, find the expected type and the found type.
        # We make a distinction between normal types, partial functions and
        # constructors.
        for i in range(self.decl.arity):
            expected_type = None
            found_type = None
            if isinstance(self.decl, Constructor):
                # Constructors.
                expected_type = self.decl.sorts[i].decl.type
            elif len(self.decl.sorts[i].decl.sorts) == 1 and self.decl.sorts[i].decl.sorts[0].type == self.decl.sorts[i].type and self.decl.sorts[i].type != '𝔹':
                # Normal types
                expected_type = self.decl.sorts[i].type
            else:
                # Partial functions
                continue
                expected_type = self.decl.sorts[i].decl.sorts[i].type

            if (hasattr(self.sub_exprs[i], 'sort') and
                    self.sub_exprs[i].sort and
                    len(self.sub_exprs[i].sort.decl.sorts) >= 1 and
                    isinstance(self.sub_exprs[i].sort.decl.sorts[0], Type)):
                # In the case of a partial function interpretation, the type is actually
                # the argument.
                # found_type = str(self.sub_exprs[i].sort.decl.sorts[i])
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
            if self.decl.type != i.args[0].get_type():
                detections.append((i.args[0],f"Element of wrong type : expected type= {type_symbol_to_str(self.decl.type)} but given type= {type_symbol_to_str(i.args[0].get_type())}","Error"))
                break

    Expression.SCA_Check(self, detections)
AppliedSymbol.SCA_Check = SCA_Check

def get_type(self):
    """
    Return the type of the symbol.
    Constructors are handled differently here.
    """
    if isinstance(self.decl, Constructor):
        return self.decl.type
    return self.decl.out.decl.type
AppliedSymbol.get_type = get_type


## class SymbolExpr(Expression):

## class UnappliedSymbol(Expression):

def get_type(self):
    return self.decl.type          #geeft type terug (als 'str')
UnappliedSymbol.get_type = get_type


## class Variable(Expression):

def get_type(self):
    if self.sort is None:
        return self.sort        #return None als self.sort onbekend is
    return self.sort.type       #returns specifieker type of Variable (als 'str')
Variable.get_type = get_type


## class Number(Expression):

def get_type(self):
    return self.type    #return type of number
Number.get_type = get_type


## class Date(Expression):

def get_type(self):
    return self.type    #return type of date
Date.get_type = get_type


## class Brackets(Expression):

def SCA_Check(self, detections):
    # style regel: Vermijd onnodige haakje
    if isinstance(self.f,Brackets):
        detections.append((self,f"Style guide, redundant brackets","Warning"))
    return Expression.SCA_Check(self, detections)
Brackets.SCA_Check = SCA_Check

def get_type(self):
    return self.f.get_type()     #return type van regel tussen haakjes
Brackets.get_type = get_type
