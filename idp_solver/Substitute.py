# cython: binding=True

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

Methods to

* substitute a constant by its value in an expression
* replace symbols interpreted in a structure by their interpretation
* instantiate an expresion, i.e. replace a variable by a value
* expand quantifiers

This module monkey-patches the Expression class and sub-classes.

( see docs/zettlr/Substitute.md )

"""

import copy

from idp_solver.Expression import Constructor, Expression, IfExpr, AQuantification, \
                    ADisjunction, AConjunction,  AAggregate, AUnary, \
                    AComparison, AppliedSymbol, Variable, NumberConstant, \
                    Fresh_Variable, TRUE


# class Expression  ###########################################################


# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, todo=None):
    """ recursively substitute e0 by e1 in self (e0 is not a Fresh_Variable)

    implementation for everything but AppliedSymbol, Variable and
    Fresh_variable
    """

    assert not isinstance(e0, Fresh_Variable) or isinstance(e1, Fresh_Variable)# should use instantiate instead
    assert self.co_constraint is None  # see AppliedSymbol or Variable instead

    # similar code in AppliedSymbol !
    if self.code == e0.code:
        if self.code == e1.code:
            return self  # to avoid infinite loops
        return self._change(value=e1)  # e1 is Constructor or NumberConstant
    else:
        # will update self.simpler
        out = self.update_exprs(e.substitute(e0, e1, assignments, todo)
                                for e in self.sub_exprs)
        return out
Expression.substitute = substitute


def instantiate(self, e0, e1, theory):
    """
    recursively substitute Fresh_Variable e0 by e1 in self

    instantiating e0=`x by e1=`f in self=`x(y) returns f(y)
    (or any instance of f if arities don't match)
    """
    out = copy.copy(self)
    out.annotations = copy.copy(out.annotations)

    # instantiate expressions, with simplification
    out = out.update_exprs(e.instantiate(e0, e1, theory) for e
                           in out.sub_exprs)

    simpler, co_constraint = None, None
    if out.simpler is not None:
        simpler = out.simpler.instantiate(e0, e1, theory)
    if out.co_constraint is not None:
        co_constraint = out.co_constraint.instantiate(e0, e1, theory)
    out._change(simpler=simpler, co_constraint=co_constraint)

    if out.value is not None:  # replace by new value
        out = out.value
    else:
        out.original = out

    if e0.name in out.fresh_vars:
        out.fresh_vars.discard(e0.name)
        if type(e1) in [Fresh_Variable, Variable]:
            # e1 is Variable when instantiating some definitions
            out.fresh_vars.add(e1.name)
        if isinstance(out, AComparison):
            out.annotate1()
    out.code = str(out)
    out.annotations['reading'] = out.code
    return out
Expression.instantiate = instantiate


def expand_quantifiers(self, theory):
    """ replaces quantified formula by its expansion

    implementation for everything but AQuantification and AAgregate
    """
    return self.update_exprs(e.expand_quantifiers(theory)
                                for e in self.sub_exprs)
Expression.expand_quantifiers = expand_quantifiers


def interpret(self, theory):
    """ for every defined term in self, add the instantiated definition
    as co-constraint

    implementation for everything but AppliedSymbol, Variable and
    Fresh_variable
    """
    if self.is_type_constraint_for:  # do not interpret typeConstraints
        return self
    out = self.update_exprs(e.interpret(theory) for e in self.sub_exprs)
    return out
Expression.interpret = interpret


# Class AQuantification  ######################################################

def expand_quantifiers(self, theory):
    inferred = self.sub_exprs[0].type_inference()
    for q in self.quantees:
        if q.var not in self.q_vars:  # Fresh_Variable not created yet
            new_var = Fresh_Variable(q.var, inferred[q.var])
            self.sub_exprs[0].substitute(new_var, new_var, {})
            self.q_vars[q.var] = new_var

    for v, s in inferred.items():
        assert v not in self.q_vars or self.q_vars[v].sort.decl == s.decl, \
            f"Inconsistent types for {v} in {self}"

    forms = [self.sub_exprs[0]]
    self.vars = []
    self.sorts = []  # not used
    for name, var in self.q_vars.items():
        if var.sort.decl.range:
            out = []
            for f in forms:
                for val in var.sort.decl.range:
                    new_f = f.instantiate(var, val, theory)
                    out.append(new_f)
            forms = out
        else:
            self.vars.append(var)
            self.sorts.append(var.sort.decl)
    forms = [f.expand_quantifiers(theory) for f in forms]

    if not self.vars:
        if self.q == '∀':
            out = AConjunction.make('∧', forms)
        else:
            out = ADisjunction.make('∨', forms)
        return self._change(sub_exprs=[out])
    return self._change(sub_exprs=forms)
AQuantification.expand_quantifiers = expand_quantifiers


# Class AAggregate  ######################################################

def expand_quantifiers(self, theory):
    inferred = self.sub_exprs[0].type_inference()
    if 1 < len(self.sub_exprs):
        inferred = {**inferred, **self.sub_exprs[1].type_inference()}
    for q in self.quantees:
        if q.var not in self.q_vars:  # Fresh_Variable not created yet
            new_var = Fresh_Variable(q.var, inferred[q.var])
            self.sub_exprs[0].substitute(new_var, new_var, {})
            self.q_vars[q.var] = new_var

    forms = [IfExpr.make(if_f=self.sub_exprs[AAggregate.CONDITION],
             then_f=NumberConstant(number='1') if self.out is None else self.sub_exprs[AAggregate.OUT],
             else_f=NumberConstant(number='0'))]
    for name, var in self.q_vars.items():
        if var.sort.decl.range:
            out = []
            for f in forms:
                for val in var.sort.decl.range:
                    new_f = f.instantiate(var, val, theory)
                    out.append(new_f)
            forms = out
        else:
            raise Exception('Can only quantify aggregates over finite domains')
    forms = [f.expand_quantifiers(theory) for f in forms]
    self.vars = None  # flag to indicate changes
    return self.update_exprs(forms)
AAggregate.expand_quantifiers = expand_quantifiers


# Class AppliedSymbol, Variable  ##############################################

def interpret(self, theory):
    sub_exprs = [e.interpret(theory) for e in self.sub_exprs]
    simpler, co_constraint = None, None
    if self.is_enumerated:
        assert self.decl.function, \
            f"Can't use 'is enumerated' with predicate {self.name}."
        interpretation = theory.interpretations[self.name]
        if interpretation.is_complete:
            simpler = TRUE
        else:
            simpler = interpretation.enumeration.contains(sub_exprs, True)
        if 'not' in self.is_enumerated:
            simpler = AUnary.make('¬', simpler)
        simpler.annotations = self.annotations
    elif self.in_enumeration:
        # re-create original Applied Symbol
        core = AppliedSymbol.make(self.s, sub_exprs).copy()
        simpler = self.in_enumeration.contains([core], False)
        simpler.annotations = self.annotations
    elif (self.name in theory.interpretations
            and any(s.name == '`Symbols' for s in self.decl.sorts)):
        # apply enumeration of predicate over symbols to allow simplification
        # do not do it otherwise, for performance reasons
        simpler = (theory.interpretations[self.name].interpret)(theory, 0,
                                                                self,
                                                                sub_exprs)
    if self.decl in theory.clark:  # has a theory
        #TODO need to quantify the co_constraints for the fresh_vars
        assert not self.fresh_vars, (
            f"The following variable(s) has not been quantified: "
            f"{','.join([str(v) for v in self.fresh_vars])}")
        co_constraint = theory.clark[self.decl].instantiate_definition(sub_exprs, theory)
    out = self._change(sub_exprs=sub_exprs, simpler=simpler, co_constraint=co_constraint)
    if simpler is not None:
        out.original = simpler.copy()  # so that translated assignment is correct
    return out
AppliedSymbol.interpret = interpret
Variable     .interpret = interpret


# @log_calls  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, todo=None):
    """ recursively substitute e0 by e1 in self """

    assert not isinstance(e0, Fresh_Variable) or isinstance(e1, Fresh_Variable)# should use instantiate instead

    if self.code == e0.code and type(e1) == Fresh_Variable:
        out = copy.copy(e1)
        out.code = self.code
        return out

    new_branch = None
    if self.co_constraint is not None:
        new_branch = self.co_constraint.substitute(e0, e1, assignments, todo)
        if todo is not None:
            todo.extend(new_branch.symbolic_propagate(assignments))

    if self.code == e0.code:
        return self._change(value=e1, co_constraint=new_branch)
    elif self.simpler is not None:  # has an interpretation
        assert self.co_constraint is None
        simpler = self.simpler.substitute(e0, e1, assignments, todo)
        return self._change(simpler=simpler)
    else:
        sub_exprs = [e.substitute(e0, e1, assignments, todo) for e in self.sub_exprs]  # no simplification here
        return self._change(sub_exprs=sub_exprs, co_constraint=new_branch)
AppliedSymbol .substitute = substitute
Variable      .substitute = substitute

def instantiate(self, e0, e1, theory):
    if self.name == e0.code:
        if type(self) == AppliedSymbol and self.decl.name == '`Symbols':
            if (isinstance(e1, Constructor)
               and len(self.sub_exprs) == len(e1.symbol.decl.sorts)):
                out = AppliedSymbol.make(e1.symbol, self.sub_exprs)
                return out
            elif isinstance(e1, Fresh_Variable):  # replacing variable in a definition
                out = copy.copy(self)
                out.code = out.code.replace(e0.code, e1.code)
                out.str = out.code.replace(e0.code, e1.code)
                out.name = e1.code
                out.s.name = e1.code
                return out
            else:
                return list(e1.symbol.decl.instances.values())[0]  # should be "unknown"
        elif len(self.sub_exprs) == 0:
            return e1
    out = Expression.instantiate(self, e0, e1, theory)
    if self.name in theory.interpretations:
        # interpret if substituting a symbol, to guard against type/arity error
        # don't do it otherwise, for performance reasons
        if any(e.sort.name == '`Symbols' for e in self.sub_exprs
                if type(e) == Fresh_Variable):
            out = out.interpret(theory)
    return out
AppliedSymbol .instantiate = instantiate
Variable      .instantiate = instantiate


# Class Fresh_Variable  #######################################################

Fresh_Variable.instantiate = instantiate

def interpret(self, theory):
    return self
Fresh_Variable.interpret = interpret

# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, todo=None):
    return e1 if self.code == e0.code else self
Fresh_Variable.substitute = substitute





Done = True
