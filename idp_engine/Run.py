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

The following Python functions can be used to perform computations
using FO-dot knowledge bases:

"""
from __future__ import annotations

from copy import copy
import gc
import logging
from os import linesep
from sys import intern
import time
import types
from typing import Any, Iterator, List, Union, Optional
import subprocess
from z3 import Solver

from idp_engine.Expression import FALSE, INT_SETNAME, OR, TRUE, AImplication, AQuantification, ASumMinus, AUnary, AppliedSymbol, NextAppliedSymbol, NowAppliedSymbol, Number, SetName, StartAppliedSymbol, SymbolExpr, UnappliedSymbol

from .Parse import IDP, Enumeration, FunctionTuple, SymbolDeclaration, SymbolInterpretation, TemporalDeclaration, TheoryBlock, Structure, TransiotionGraph, TupleIDP, TypeDeclaration, Vocabulary
from .Theory import Theory
from .Assignments import Status as S, Assignments
from .utils import BOOL, DATE, INT, NEWL, REAL, IDPZ3Error, PROCESS_TIMINGS, OrderedSet, v_time
from .Annotate import annotate_exp_theory

last_call = time.process_time()  # define it as global

input_recived = False
sim_input = ""

def model_check(*theories: Union[TheoryBlock, Structure, Theory]) -> str:
    """Returns a string stating whether the combination of theories is satisfiable.

    For example, ``print(model_check(T, S))`` will print ``sat`` if theory named ``T`` has a model expanding structure named ``S``.

    Args:
        theories (Union[TheoryBlock, Structure, Theory]): 1 or more (data) theories.

    Returns:
        str: ``sat``, ``unsat`` or ``unknown``
    """
    ground_start = time.time()
    problem = Theory(*theories)
    z3_formula = problem.formula()
    PROCESS_TIMINGS['ground'] += time.time() - ground_start


    solver = Solver(ctx=problem.ctx)
    solver.add(z3_formula)
    return str(solver.check())


def matchingstates(assign,transitiongraph:TransiotionGraph):
    fluents = transitiongraph.fextentions.keys()
    ffluents = transitiongraph.ffextentions.keys()
    out : dict[SymbolDeclaration, List[TupleIDP]] = {}
    nullary: dict[SymbolDeclaration, Any] = {}
    states = []
    #print("matching states .....")
    for a in assign.values():
        if type(a.sentence) == AppliedSymbol:
            #print(a)
            args = [e for e in a.sentence.sub_exprs]
            args = tuple(args)
            c = None
            default = False
            if  a.symbol_decl.is_next and (a.symbol_decl.name[:-len('_next')] in fluents or a.symbol_decl.name[:-len('_next')] in ffluents ):
                #print(a)
                if a.symbol_decl.arity == 0:
                    args = None
                    #because we dont have functions c can either be true or false
                    c = a.value
                    if str(c) == "true":
                        c = True
                    elif str(c) == "false":
                        c = False
                elif a.value == TRUE:
                    c = True
                elif a.value == FALSE:
                    c = False
                #print(c)
                if c is not None and c == True:
                    if len(states) == 0:
                        states.append([(c,a.symbol_decl.name[:-len('_next')],args)])
                    else:
                        for s in states:
                            s.append((c,a.symbol_decl.name[:-len('_next')],args))
                elif c is None:
                    if len(states) == 0:
                        states.append([(True,a.symbol_decl.name[:-len('_next')],args)])
                        states.append([])
                    else:
                        nstate = []
                        for s in states:
                            nstate.append(s+[(True,a.symbol_decl.name[:-len('_next')],args)])
                            nstate.append(s)
                        states = nstate
    #print("states.........,,,,,,")
    #print(states)
    #for s in states:
    #    if s[0][2][2] == s[1][2][2]:
    #        print(s[0][2][2])
    matchedStates = []
    i = 0
    for os in transitiongraph.states:
        for s in states:
            ntrue = 0
            allmatch = False
            onematch = False
            #print("os")
            #print(os)
            for e in os:
                #print(e)
                onematch = True
                if e[0] == True:
                    onematch = False
                    ntrue += 1
                    for e2 in s:
                        if e2[1] == e[1] and str(e2[2]) == str(e[2]):
                            #print("wordkssfd")
                            onematch = True
                            break
                if not onematch:
                    allmatch = False
                    break
                allmatch =True
            if ntrue == len(s) and allmatch:
                matchedStates.append(i)
                break
        i += 1
    #print("mathjsdfjklj")
    #print(matchedStates)
    return matchedStates
            
    

def toStructure(assign,vocab_name:str,voc:Vocabulary,tempdcl:List[TemporalDeclaration]) -> (Structure,TheoryBlock):
        #print("enter to structure..")
        out : dict[SymbolDeclaration, List[TupleIDP]] = {}
        #To store the symbol declaration of symbols in out
        outname : dict[str,SymbolDeclaration] = {}
        #To store all symbol declarations of non nullary predicates
        outall : dict[str,SymbolDeclaration] = {}
        nullary: dict[SymbolDeclaration, Any] = {}
        #To store the symbol declaration of symbols in nullary
        nullaryname : dict[str,SymbolDeclaration] = {}
        #To store all symbol declarations of nullary predicates
        nullaryall : dict[str,SymbolDeclaration] = {}
        #no_value : dict[SymbolDeclaration, Any] = {}
        false_val : List[tuple] = []
        #print("in loop")
        for a in assign.values():
            if type(a.sentence) == AppliedSymbol:
                #print(a)
                args = [e for e in a.sentence.sub_exprs]
                c = None
                default = False
                if a.symbol_decl.arity == 0:
                    #TO DO: Should default be used
                    default = True
                    c = a.value
                elif a.value == TRUE:
                    # Symbol is a predicate.
                    c = TupleIDP(args=args)
                elif a.value == FALSE:
                    a
                    false_val.append((a.symbol_decl,args))
                    #c = TupleIDP(args=[])
                elif a.value is not None:
                    # Symbol is a function.
                    c = FunctionTuple(args=args,value=a.value)
                if c:
                    if default:
                        nullary[a.symbol_decl] = c
                        nullaryname[a.symbol_decl.name]= a.symbol_decl
                    else:
                        enum = out.get(a.symbol_decl, [])
                        enum.append(c) 
                        out[a.symbol_decl] = enum
                        outname[a.symbol_decl.name]= a.symbol_decl
                if a.symbol_decl.arity == 0:
                    nullaryall[a.symbol_decl.name]= a.symbol_decl
                else:
                    outall[a.symbol_decl.name]= a.symbol_decl

        nullaryc: dict[SymbolDeclaration, Any] = nullary.copy()
        outc : dict[SymbolDeclaration, List[TupleIDP]] = out.copy()
        false_th = false_val.copy()
        ftheories = []
        #If a symbol has next present then its value should be set to now
        #If there is no next for a temporal symbol it should be removed
        # eg p_next = {1 ,2} and p = {0} then after this loop: p = {1 ,2}
        for t in tempdcl:
            for k ,v in nullary.items():
                if t.symbol.name == k.name:
                    n = nullaryname.get(k.name+'_next',None)
                    if n is None:
                        #There is no next time so now should be removed
                        nullaryc.pop(k)
                    else:
                        vn = nullaryc.get(n,None)
                        if vn is  not None:
                            #value of next should replace now
                            nullaryc[k] = vn
                elif k.is_next and k.name.endswith('_next'):
                    #k.is_next= False
                    #nullaryc[k] = v
                    if t.symbol.name == k.name[:-len('_next')]:
                        #Next should be removed
                        nullaryc.pop(k,None)
                        n = nullaryall.get(k.name[:-len('_next')],None)
                        if n is None:
                            print("Error: current state of predicate should be in the list")
                        else:
                            #Value of next should replace now
                            nullaryc[n] = v
                else:
                    #nullaryc[k] = v
                    k
            for k ,v in out.items():
                if t.symbol.name == k.name:
                    n = outname.get(k.name+'_next',None)
                    if n is None:
                        outc.pop(k)
                    else:
                        vn = outc.get(n,None)
                        if vn is  not None:
                            outc[k] = vn
                elif k.is_next and k.name.endswith('_next'):
                    #k.is_next= False
                    #outc[k] = v
                    if t.symbol.name == k.name[:-len('_next')]:
                        outc.pop(k,None)
                        n = outall.get(k.name[:-len('_next')],None)
                        if n is None:
                            print("Error: current state of predicate should be in the list")
                        else:
                            outc[n] = v
                else:
                    #outc[k] = v
                    k
            index = 0
            for k ,v in false_val:
                if t.symbol.name == k.name:
                    false_th[index] = None
                elif k.is_next and k.name.endswith('_next'):
                    #k.is_next= False
                    #outc[k] = v
                    ftheories.append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,k.name[:-len('_next')],None,None),v)))
                    false_th[index] = None
                index += 1
            
        for f in false_th:
            if f is not None:
                ftheories.append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,f[0].name,None,None),f[1])))
        #print("to struct interprets.....")
        #print(outc)
        #print(nullaryc)
        interps: List[SymbolInterpretation] = []
        for k ,v in nullaryc.items():
            if k.name:
                ku = UnappliedSymbol(None,(k.name))
                interps.append(SymbolInterpretation(parent=None,name=ku,enumeration=None,sign=':=',default=v))
        for k ,v in outc.items():
            if k.name:
                ku = UnappliedSymbol(None,(k.name))
                enm = Enumeration(None,v)
                interps.append(SymbolInterpretation(parent=None,name=ku,enumeration=enm,sign=':=',default=None))
        s = Structure(name="progression",vocab_name=vocab_name,interpretations=interps)
        s.voc= voc
        for i in s.interpretations.values():
            i.block = s
            i = i.annotate(voc,{})
        for f in ftheories:
            #print(f)
            f.annotate(voc,{})
        #voc.add_voc_to_block(s)
        fth = TheoryBlock(name="fth",vocab_name=voc.name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
        fth.voc = voc
        fth.constraints = OrderedSet(ftheories)
        return (s,fth)

def initialize(theory:TheoryBlock,struct:Structure):
    #print("inside initialize")
    #print(theory.init_theory.definitions)
    problem = Theory(theory.init_theory,struct.init_struct)
    PROCESS_TIMINGS['ground'] = time.time() - PROCESS_TIMINGS['ground']

    solve_start = time.time()
    ms = list(problem.expand(max=10, timeout_seconds=10, complete=False))
    if isinstance(ms[-1], str):
        ms, last = ms[:-1], ms[-1]
    else:
        last = ""
    out = []
    #for i, m in enumerate(ms):
    #    s = m.toStructure(struct.vocab_name,struct.voc)
    #    out.append(s)
    for i, m in enumerate(ms):
        #No tempdcl given so that it is not checked with next
        s = toStructure(m,struct.init_struct.vocab_name,struct.init_struct.voc,[])
        out.append(s)
    out.append(last)
    PROCESS_TIMINGS['solve'] += time.time() - solve_start
    return out
    #return model_expand(theory.init_theory,struct.init_struct)

def progression(theory:TheoryBlock,struct,additional_theory:TheoryBlock=None):
    print("inside progression")
    problem = None
    voc = None
    #if isinstance(struct, types.GeneratorType):
    #    for i, xi in enumerate(struct):
    #        #print(xi)
    #        if not isinstance(xi,Structure):
    #            pass
    #        problem = Theory(theory.bistate_theory,xi)
    #        voc = xi.voc.idp.next_voc.get(theory.vocab_name+'_next',None)
    #        #print(voc)
    #        if voc is None:
    #            print("Error vocabulary is wrong")
    #            return
            #print(problem.assignments)
    out = []
    PROCESS_TIMINGS['ground'] = time.time() - PROCESS_TIMINGS['ground']
    solve_start = time.time()
    if isinstance(struct,List):
        j = 1
        for xi in struct:
            if not isinstance(xi,tuple):
                pass
            elif isinstance(xi[0],Structure):
                if additional_theory:
                    problem = Theory(theory.bistate_theory,xi[0],xi[1],additional_theory)
                else:
                    problem = Theory(theory.bistate_theory,xi[0],xi[1])
                voc = xi[0].voc.idp.next_voc.get(theory.vocab_name+'_next',None)
                if voc is None:
                    print("Error vocabulary is wrong")
                    return
                if problem is None:
                    pass
                ms = list(problem.expand(max=10, timeout_seconds=10, complete=False))
                if isinstance(ms[-1], str):
                    ms, last = ms[:-1], ms[-1]
                else:
                    last = ""
                
                for i, m in enumerate(ms):
                    s = toStructure(m,theory.bistate_theory.vocab_name,voc,theory.voc.tempdcl)
                    #for i in s.interpretations.values():
                        #print(i)
                    out.append(s)
                #yield out 
                out.append(last + " For Strtucture " + str(j))
            j += 1
    elif isinstance(struct,tuple):
        #Used in simulate
        if not isinstance(struct[0],Structure):
            print("Error a structure should be given")
            return
        if additional_theory:
            problem = Theory(theory.bistate_theory,struct[0],struct[1],additional_theory)
        else:
            problem = Theory(theory.bistate_theory,struct[0],struct[1])
        #problem = Theory(theory.bistate_theory,struct)
        voc = struct[0].voc.idp.next_voc.get(theory.vocab_name+'_next',None)
        if voc is None:
            print("Error vocabulary is wrong")
            return
        if problem is None:
            pass
        ms = list(problem.expand(max=10, timeout_seconds=10, complete=False))
        if isinstance(ms[-1], str):
            ms, last = ms[:-1], ms[-1]
        else:
            last = ""
        for i, m in enumerate(ms):
            s = toStructure(m,theory.bistate_theory.vocab_name,voc,theory.voc.tempdcl)
            out.append(s)
        #yield out 
        out.append(last)
    #if problem is None:
    #    print("reciedved None")
    #    #problem = Theory(theory.bistate_theory)
    #    return
    PROCESS_TIMINGS['solve'] += time.time() - solve_start
    return out
    

def simulate(theory:TheoryBlock,struct:Structure):
    result = initialize(theory,struct)
    print_struct(result)
    act_question = "Please give the action with its arguments(n to pass) "
    question = "Which structure do you want to continue the simulation with?(N to stop the simulation) "
    while True:  
        correctinp = False
        i = ""
        while not correctinp:
            i = input(question)
            if i == "N":
                break
            try:
                i = int(i)
                correctinp = True
            except ValueError:
                print("Please give a number")
        if i == "N":
            break
        while (i > len(result)) or i < 1:
            correctinp = False
            while not correctinp:
                i = input(question)
                if i == "N":
                    break
                try:
                    i = int(i)
                    correctinp = True
                except ValueError:
                    print("Please give a number")
            if i == "N":
                break
            print("Please give a number within the range of possible models.")
        if i == "N":
            break
        ac = input(act_question)
        first = True
        if ac != "n":
            failed = True
            th = None
            while failed:
                act = False
                if not first:
                    ac = input(act_question)
                    if ac == "n":
                        failed = True
                        break
                else:
                    first = False
                incorrect_inp = False
                #print(theory.voc.actions)
                apred = ""
                try:
                    apred = ac[:ac.index('(')]
                except:
                    print("ERROR:Please provide arguments of the predicate, if there are no, give ()")
                    incorrect_inp = True
                if not incorrect_inp:
                    for a in theory.voc.actions:
                            if  apred == a:
                                act = True
                                break
                if act :
                    failed = False
                    vtxt = theory.init_theory.voc.fullstr()
                    #print(vtxt)
                    thtxt = vtxt + " theory " + "action:"+ theory.init_theory.vocab_name + "{ " + ac + "." " }"
                    try:
                        idpt = IDP.from_str(thtxt)
                        thtemp = idpt.get_blocks("action")[0]
                        aconstraint : Expression =None
                        for c in thtemp.constraints:
                            aconstraint = c
                        th = TheoryBlock(name="action",vocab_name=theory.bistate_theory.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
                        th.voc = theory.bistate_theory.voc
                        aconstraint.annotate(th.voc,{})
                        th.constraints = OrderedSet([aconstraint])

                    except (IDPZ3Error) as e :
                        failed = True
                        print(e)
                elif not incorrect_inp:
                    print("ERROR: The given predicate is not an Action")

            if failed:
                result = progression(theory,result[i-1])
            else:
                result = progression(theory,result[i-1],th)
            print_struct(result)
        else:
            result = progression(theory,result[i-1])
            print_struct(result)

def ForProgression(theory:TheoryBlock,struct,number:int):
    result = progression(theory,struct)
    print_struct(result)
    i = 1
    while i<=number:
        result = progression(theory,result)
        print_struct(result)
        i+=1

def isinvariant(theory:TheoryBlock,invariant:TheoryBlock,s:Structure|None=None,forward_chaining=False):
    if not theory.ltc:
        return "Invariant proving is only for LTC theories"
    #TO DO: check if the invariant is correctly formulated
    if len(invariant.constraints) > 1:
        return "Only one formula should be specified for invariant"
    if len(invariant.constraints) == 0:
        return "Please provide an invariant"
    if forward_chaining:
        return forward_chain(theory,invariant)
    inv = None
    for c in invariant.constraints:
        inv = c
    inv2 = inv.init_copy()
    #print("ch1")
    n = theory.contains_next(inv)
    if n:
        return "Invariant should only contain signle state formulas"
    #Now[p] should be transfered to p
    #print("ch2")
    inv = theory.bis_subexpr(inv)
    if inv == False:
        return "Not allowed to use Start in invariant"
    inv = AUnary(None,['not'],inv)
    voc_now = theory.init_theory.voc
    inv.annotate(voc_now,{})
    invariant.constraints = OrderedSet([inv])
    #print(invariant.constraints)
    p0 = None
    first_step = False
    if s is not None:
        p0 = model_expand(theory.init_theory,invariant,s)
    else:
        p0 = model_expand(theory.init_theory,invariant)
    j =0
    for i, xi in enumerate(p0):
        #print(xi)
        if xi == 'No models.':
            first_step = True
        j+=1
    if not first_step or j > 1:
        return "****Invariant is FALSE****"
    invariant2 = TheoryBlock(name=invariant.name,vocab_name=invariant.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
    inv2 = theory.sis_subexpr(inv2)
    #print(inv2.sub_exprs[0].sub_exprs)
    if inv2 == False:
        return "Not allowed to use Start in invariant"
    inv2 = AUnary(None,['not'],inv2)
    voc_next = theory.bistate_theory.voc
    inv2.annotate(voc_next,{})
    invariant2.constraints = OrderedSet([inv2])
    #print("inv2")
    #print(invariant2.constraints)
    inv = inv.sub_exprs[0]
    invariant.constraints = OrderedSet([inv])
    p1 = None
    second_step = False
    if s is not None:
        p1 = model_expand(theory.transition_theory,invariant,invariant2,s)
    else:
        p1 = model_expand(theory.transition_theory,invariant,invariant2)
    j=0
    for i, xi in enumerate(p1):
        #print(xi)
        if xi == 'No models.':
            second_step = True
        j+=1
    if not second_step or j>1:
        return "****Invariant is FALSE****"
    return "****Invariant is TRUE****"

def forward_chain(theory:TheoryBlock,invariant:TheoryBlock):
    #Format of the thery should be like !t:q(t) and conditions => q(t+n) where n > 0
    #Checking the correctness of the format 
    af = None
    for c in invariant.constraints:
        af = c
    if not isinstance(af,AQuantification):
        return "formula should be of universal quantification"
    f = af.f
    if not isinstance(f,AImplication):
        return "Wrong format: body of quantification should be an implication"
    implicant = f.sub_exprs[1]
    #if not isinstance(implicant,AppliedSymbol):
    #    return "Wrong format: implicant should only have one predicate/function"
    #n = implicant.symbol.name
    #r = contains_symb(f.sub_exprs[0],n)
    #if r == 0:
    #    return "Wrong format: The implicant should be available in the antecedent of implication"
    #if r == -1:
    #    return "Wrong format: should not have Now,Next, Start in forward chaning"
    voc_now = theory.voc
    chain_num = 1
    if voc_now.tempdcl != None:
        r = adjust_formula(f,voc_now.tempdcl)
        if isinstance(r,str):
            return r
        chain_num = r
    #print("adjusted formula")
    #print(f)
    voc : Vocabulary = voc_now.generate_expanded_voc(chain_num)
    voc.annotate_block(theory.voc.idp)
    af = AUnary(None,['not'],af)
    af.annotate(voc,{})
    invariant.constraints = OrderedSet([af])
    exp_th = theory.org_theory.expand_theory(chain_num,voc)
    annotate_exp_theory(exp_th,voc)
    """print("expanded th..")
    for c in exp_th.constraints:
        print(c)
    for d in exp_th.definitions:
        for r in d.rules:
            print(r)"""
    p1 = model_expand(exp_th,invariant,timeout_seconds=50)
    second_step =False
    j=0
    for i, xi in enumerate(p1):
        #print(xi)
        if xi == 'No models.':
            second_step = True
        j+=1
    if not second_step or j>1:
        return "****Invariant is FALSE****"
    return "****Invariant is TRUE****"

def adjust_formula(expression:AImplication,tempdcl:List[TemporalDeclaration]):
    implicant:Expression = expression.sub_exprs[1]
    n = adjust_implicant(implicant,tempdcl)
    if isinstance(n,str):
        return n
    elif n == 0:
        return "Wrong format: No upper limit provided"
    r = adjust_sub(expression.sub_exprs[0],tempdcl,n)
    if isinstance(r,str):
        return r
    return n
    
def adjust_implicant(expression:Expression,tempdcl:List[TemporalDeclaration]):
    if isinstance(expression,(StartAppliedSymbol,NowAppliedSymbol,NextAppliedSymbol)):
        return "Not allowed to use Start/Now/Next"
    if isinstance(expression,AppliedSymbol):
        for t in tempdcl:
            if expression.symbol.name == t.symbol.name:
                last = expression.sub_exprs.pop()
                if isinstance(last,ASumMinus):
                    if not last.operator[0] == '+':
                        return "Only addition is acceptable"
                    if len(last.sub_exprs) > 2 :
                        return "Please provide one number in the additions"
                    for e in last.sub_exprs:
                        if isinstance(e,Number) and e.type == INT_SETNAME:
                            n = e.py_value 
                            expression.symbol.name = expression.symbol.name + '_' + str(n)
                            expression.code = intern(str(expression))
                            expression.str = expression.code
                            return n  
                else:
                    return "End of the chain should be determined"
                break
    n = 0
    for e in expression.sub_exprs:
        r = adjust_implicant(e,tempdcl)
        if r != None:
            if type(r)  == int:
                if n == 0 :
                    n = r
                elif r != 0:
                    if r != n:
                        return "All the predicates in the implicant should be of the same time"
                    #n = max(n,r)
            else:
                return r
    expression.code = intern(str(expression))
    expression.str = expression.code
    return n
    
def adjust_sub(expression:Expression,tempdcl:List[TemporalDeclaration],n:int):
    if isinstance(expression,(StartAppliedSymbol,NowAppliedSymbol,NextAppliedSymbol)):
        return "Not allowed to use Start/Now/Next"
    if isinstance(expression,AppliedSymbol):
        for t in tempdcl:
            if expression.symbol.name == t.symbol.name:
                last = expression.sub_exprs.pop()
                if isinstance(last,ASumMinus):
                    if not last.operator[0] == '+':
                        return "Only addition is acceptable in atecedant"
                    if len(last.sub_exprs) > 2 :
                        return "Please provide one number in the additions"
                    for e in last.sub_exprs:
                        if isinstance(e,Number) and e.type == INT_SETNAME:
                            if e.py_value > n :
                                return "Cant use numbers higher than the upperlimit"
                            level = e.py_value
                            if level != 0:
                                expression.symbol.name = expression.symbol.name + '_' + str(level)
                                expression.code = intern(str(expression))
                                expression.str = expression.code
                            break   
                break
    for e in expression.sub_exprs:
        r = adjust_sub(e,tempdcl,n)
        if r != None:
            return r
    expression.code = intern(str(expression))
    expression.str = expression.code

#checks if an expression contains NextAppliedSymbol
def contains_symb(e:Expression,s:str=""):
    if isinstance(e,AppliedSymbol):
        if e.symbol.name == s:
            return 1
        return 0
    if isinstance(e,(NowAppliedSymbol,StartAppliedSymbol,NextAppliedSymbol)):
        return -1
    for sube in e.sub_exprs:
        r = contains_symb(sube,s)
        if r == 1:
            return 1
        if r == -1:
            return -1
    return 0
    
def ProveModalLogic(formula,init_structure:Structure,theory:TheoryBlock):
    #TO DO: check if the init_structure does interpret all the time independant predicates/functions
    if theory.ltc is None:
        return "Theory should be an LTC theory"
    #In order to avoid giving dupllicae declaration error in Theory.add
    temps = Structure(name="test",vocab_name=init_structure.vocab_name,interpretations=init_structure.interpretations.values())
    temps.voc= init_structure.voc
    #for i in s.interpretations.values():
    #    i.block = s
    print("inside prove......")
    vcnm = init_structure.vocab_name+"_now"
    testth = TheoryBlock(name="T",vocab_name=vcnm,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
    voc_now = init_structure.voc.idp.now_voc[vcnm]
    testth.voc = voc_now
    voc_now.add_voc_to_block(testth)
    problem = Theory(testth)
    #print(problem.extensions)
    transitiongraph = TransiotionGraph(init_structure.voc,problem)
    #print("transiiton graph states")
    #for l in transitiongraph.states:
    #    print(l)
    #To make beforehand the negation of actions and annotate them
    Nonaction = {}
    for action , extentsion in transitiongraph.aextentions.items():
        e = extentsion[0]
        if e == [[]]:
            na = AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,action,None,None),[]))
            na.annotate(theory.transition_theory.voc,{})
            nal = Nonaction.get(action,[])
            nal.append(na)
            Nonaction[action] = nal
        else:
            for arg in e:
                na = AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,action,None,None),arg))
                na.annotate(theory.transition_theory.voc,{})
                nal = Nonaction.get(action,[])
                nal.append(na)
                Nonaction[action] = nal
    Nstate = []
    Nnextstate = []
    removedStates = []
    i = 0
    for s1 in transitiongraph.states:
        Nstate.append([])
        Nnextstate.append([])
        for s in s1:
            if s[2] is None:
                if s[0] == True:
                    Nstate[-1].append(AppliedSymbol(None,SymbolExpr(None,s[1],None,None),[]))
                    Nstate[-1][-1].annotate(theory.transition_theory.voc,{})
                    Nnextstate[-1].append(AppliedSymbol(None,SymbolExpr(None,s[1]+"_next",None,None),[]))
                    Nnextstate[-1][-1].annotate(theory.transition_theory.voc,{})
                else:
                    Nstate[-1].append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,s[1],None,None),[])))
                    Nstate[-1][-1].annotate(theory.transition_theory.voc,{})
                    Nnextstate[-1].append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,s[1]+"_next",None,None),[])))
                    Nnextstate[-1][-1].annotate(theory.transition_theory.voc,{})
            else:
                if s[0] == True:
                    Nstate[-1].append(AppliedSymbol(None,SymbolExpr(None,s[1],None,None),s[2]))
                    Nstate[-1][-1].annotate(theory.transition_theory.voc,{})
                    Nnextstate[-1].append(AppliedSymbol(None,SymbolExpr(None,s[1]+"_next",None,None),s[2]))
                    Nnextstate[-1][-1].annotate(theory.transition_theory.voc,{})
                else:
                    Nstate[-1].append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,s[1],None,None),s[2])))
                    Nstate[-1][-1].annotate(theory.transition_theory.voc,{})
                    Nnextstate[-1].append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,s[1]+"_next",None,None),s[2])))
                    Nnextstate[-1][-1].annotate(theory.transition_theory.voc,{})
        #if purgeImpossibleState(Nstate[-1],temps,theory.init_theory):
            #Nstate.pop()
            #Nnextstate.pop()
            #removedStates.append(i)
        i += 1
    #remove the removed states form transitiongraph
    print("transition states")
    print(transitiongraph.aextentions)
    #print(transitiongraph.states)
    print(len(Nstate))
    initialStates = AlternativeAlg2(transitiongraph,Nstate,Nnextstate,Nonaction,temps,theory)
    print("transition list")
    for k ,v in transitiongraph.transtions.items():
        print(k,v)
    #print(problem.extensions)
        
    #eg: person': ([[John], [Bob]])
    probsets : dict(str,List[List]) = {}
    probvar : dict(str,List[SetName]) = {}
    probacts : dict(str,List[SetName]) = {}
    for s,e in problem.extensions.items():
        for d in init_structure.voc.original_decl:
            if isinstance(d,TypeDeclaration):  
                if s == d.name:
                    probsets[s] = e[0]
                    break
    #TO DO: Check recursive data type definitions and what result for their extension would be
    #If the definition is is recursive there would be an error?
    for d in voc_now.declarations:
        if isinstance(d,SymbolDeclaration):
            if d.name in init_structure.voc.fluents or d.name in init_structure.voc.ftemproral:
                #TO DO : WHAT ABOUT FUNCTIONS
                probvar[d.name] = d.domains
            if d.name in init_structure.voc.actions:
                probacts[d.name] = d.domains
    #TO DO: Check that the sorts dont have inifinte types like INT
    
    tsets = "SETS "
    i = 0
    numsets = []
    for s , e in probsets.items():
        #tsets += s 
        if e == [[]]:
            tsets += s + " =BOOL"
        else:
            if not isinstance(e[0][0],Number):
                tsets += s + " ={ "
                j = 0
                for elem in e:
                    if j != 0:
                        tsets += " , "
                    tsets += str(elem[0])
                    j += 1
                tsets += " }"
            else:
                numsets.append(s)
        
        if i != len(probsets.keys()) -1 :
            tsets += ";"
        i += 1

    probnumset :dict(str,List) = {}
    i = 0
    for s in numsets:
        smin = int(str(probsets[s][0][0]))
        smax = smin
        for elem in probsets[s]:
            n = int(str(elem[0]))
            if  n< smin:
                smin = n
            if n > smax:
                smax = n
        probnumset[s] =[smin,smax]
        i += 1

    tvars ="VARIABLES "
    i = 0
    for f in probvar.keys():
        if i != 0:
            tvars += ", "
        tvars += f
        i += 1
    tinvar ="INVARIANT "
    i = 0
    for f , domains in probvar.items():
        if i != 0:
            tinvar += " & "
        tinvar += f + ": "
        j = 0
        ld = len(domains)
        for d in domains:
            if j == 0 and ld > 2:
                tinvar += "("
            if j != 0 and ld > 2 and j != ld -1 :
                tinvar += " * "
            elif j != 0 and ld == 2 and j == ld -1 :
                tinvar += " <-> "
            elif j != 0 and ld > 2 and j == ld -1 :
                tinvar += " <-> "

            if d.name == BOOL:
                tinvar += "BOOL"
            elif d.name == INT or d.name == DATE or d.name == REAL:
                return "Int or date or real type is not allowed"
            else:
                domname =""
                if d.name in probnumset.keys():
                    domname = str(probnumset[d.name][0]) + ".." + str(probnumset[d.name][1])
                else:
                    domname = d.name 
                if ld == 1:
                    #TO DO: Check if it is a function to reduce possible overload 
                    tinvar += "POW(" + domname + ")"
                else:
                    tinvar += domname

            if j == ld -2 and ld > 2:
                tinvar += ")"
            j += 1
        if ld == 0:
            tinvar += "BOOL"
        i += 1
    
    tinint ="INITIALISATION "
    leninitstate = len(initialStates)
    initialvalues : List[dict] = []
    i = 0
    for s in initialStates:
        initialvalues.append({})
        StateToProb(transitiongraph.states[s],initialvalues[-1])

    i = 0
    if leninitstate != 1:
        tinint += "CHOICE "
    for initst in initialvalues:
        if i != 0:
            tinint += " OR "
        tinint += toProbSubstitution(" := "," ; ",initst)
        i+=1
    if leninitstate != 1:
        tinint += " END"

    #it contains the list of conditions for each action
    actioncondition :dict(str,List[str]) = {}
    actionoperation :dict(str,List) = {}

    for trans ,act in transitiongraph.transtions.items():
        for a in act:
            n = a.symbol.name
            conds = actioncondition.get(n,[])
            cnd = " ("
            j = 0
            #The name of the arguments of action is action0,action1,....
            for elem in a.sub_exprs:
                if j != 0:
                    cnd += " & "
                if str(elem) =="true":
                    cnd += n + str(j) + " = TRUE"
                elif str(elem) =="false":
                    cnd += n + str(j) + " = FALSE" 
                else:
                    cnd += n + str(j) + " = " + str(elem)
                j += 1
            
            beginstate = {}
            StateToProb(transitiongraph.states[trans[0]],beginstate)
            endstate = {}
            StateToProb(transitiongraph.states[trans[1]],endstate)
            if j > 0  and len(beginstate.keys()) > 0:
                cnd += " & "
            cnd += toProbSubstitution(" = "," & ",beginstate)
            cnd += " ) "
            if j > 0 or len(beginstate.keys()) > 0: 
                conds.append(cnd)
                actioncondition[n] = conds
                op = cnd + " THEN " + toProbSubstitution(" := ", " ; ", endstate)
                oprtns = actionoperation.get(n,[])
                oprtns.append(op)
                actionoperation[n] = oprtns
    
    toprts ="OPERATIONS "
    actnum = 0
    for a , domains in probacts.items():
        actstr =""
        if actnum != 0:
            actstr += " ; "
        actstr = a + "("
        argn = len(domains)
        j = 0
        while j < argn:
            if j != 0:
                actstr += ", "
            actstr += a + str(j)
            j += 1
        actstr += ") = PRE "
        j = 0
        for d in domains:
            if j != 0:
                actstr += " & "
            actstr += a + str(j) + " :"
            if d.name == BOOL:
                actstr += "BOOL"
            else:
                domname =""
                if d.name in probnumset.keys():
                    domname = str(probnumset[d.name][0]) + ".." + str(probnumset[d.name][1])
                else:
                    domname = d.name 
                actstr += domname
                #actstr += d.name
            j += 1
        cndln = len(actioncondition[a])
        if cndln > 0:
            if argn > 0:
                actstr += " & ("
            else:
                actstr += "("
        j = 0
        for a1 in actioncondition[a]:
            if j != 0 :
                actstr += " or "
            actstr += a1
            j += 1
        if cndln > 0:
            actstr += ") "
        if cndln ==0 and argn == 0:
            actstr += "TRUE "
        actstr += " THEN "
        j = 0
        for ops in actionoperation[a]:
            if j == 0:
                actstr += " IF "
            else:
                actstr += " ELSIF "
            actstr += ops
            j += 1
        if len(actionoperation[a]) > 0:
            actstr += " END END"
        else:
            actstr += " skip END"
        toprts += actstr
        actnum += 1
    
    machine = "MACHINE Test" + '\n' + tsets + '\n' + tvars + '\n' + tinvar + \
          '\n' + tinint + '\n' + toprts + '\n' + "END"
    print(machine)

    f = open("test.mch","w")
    f.write(machine)
    f.close()        
    a = subprocess.run('C:\Prob\probcli test.mch -model-check -spdot states.dot',shell=True,capture_output=True)
    print("PROBCLI............")
    print(a.stdout.decode())
    print(a.stderr.decode())
    return
    i =0
    for s1 in Nstate:
        j=0
        for s2 in Nnextstate:
            for action , extentsion in transitiongraph.aextentions.items():
                e = extentsion[0]
                t = False
                if e == [[]]:
                    t = checkTransition(action,None,temps,theory.transition_theory,s1,s2,Nonaction)
                    if t != False:
                        trs = transitiongraph.transtions.get((i,j),[])
                        trs.append(t)
                        transitiongraph.transtions[(i,j)] = trs
                else:
                    q = 0
                    for arg in e:
                        t = checkTransition(action,arg,temps,theory.transition_theory,s1,s2,Nonaction,q)
                        if t != False:
                            trs = transitiongraph.transtions.get((i,j),[])
                            trs.append(t)
                            transitiongraph.transtions[(i,j)] = trs
                        q += 1
            j += 1
        i += 1
    print("transition list")
    print(transitiongraph.transtions)

#initst is the dictionary produced by StateToProb function which for each predicates holds the list of values that is true
def toProbSubstitution(equalitysign:str,subdeliminator:str,initst:dict) -> str:
    i2 = 0
    tinint = ""
    for k , valv in initst.items():
        if i2 != 0:
            tinint += subdeliminator
        tinint += k + equalitysign
        if len(valv) == 0:
            #TO DO: It could be the case if a predicate is like int1to5 -> Bool and at first it is false for all 1..5 
            #in that case; maybe in prob the predicate has to becom (int1to5,Bool) -> Bool for this below to work
            #TO DO:Partial functions ????
            tinint += "{}"
        elif len(valv) == 1 and (valv[0] == "TRUE" or valv[0] == "FALSE"):
            tinint += valv[0]
        else:
            tinint += " {"
            j = 0
            for v in valv:
                if j != 0:
                    tinint += " , "
                tinint += "("
                q = 0
                for v1 in v:
                    if q != 0 :
                        tinint += " , "
                    tinint += str(v1)
                    q += 1
                tinint += ")"
                j += 1

            tinint += "} " 
        i2 += 1
    return tinint
            

def StateToProb(state:List,store:dict):
    for s1 in state:
        if s1[2] is None:
            if s1[0] == True:
                store[s1[1]] = ["TRUE"]
            else:
                store[s1[1]] = ["FALSE"]
        else:
            if s1[0] == True:
                posres = store.get(s1[1],[])
                tp = []
                j = 0
                for elem in s1[2]:
                    #if j != 0:
                    #    tp += ","
                    if str(elem) =="true": # elem.name
                        tp.append("TRUE")
                    elif str(elem) =="false":
                        tp.append("FALSE") 
                    else:
                        tp.append(elem)
                    j += 1
                #tp += ")"
                posres.append(tp)
                store[s1[1]] = posres
            else: 
                if store.get(s1[1],None) is None:
                    store[s1[1]] = []

def AlternativeAlg(transitiongraph:TransiotionGraph,Nstate:List,Nnextstate:List,Nonaction:dict,init_struct:Structure,theory:TheoryBlock):
    reachedStates =[]
    nextreachedState = []
    initialStates = []
    i = 0
    for s1 in Nstate:
        t = checkTransition("",None,init_struct,theory.init_theory,s1,[],{})
        if t != False:
            nextreachedState.append(i)
            reachedStates.append(i)
            initialStates.append(i)
        i += 1
    print("inital state")
    print(reachedStates)
    tempstate = nextreachedState.copy()
    while len(tempstate) > 0 :
        nextreachedState = tempstate.copy()
        tempstate = []
        for i in nextreachedState:
            j=0
            for s2 in Nnextstate:
                for action , extentsion in transitiongraph.aextentions.items():
                    e = extentsion[0]
                    t = False
                    if e == [[]]:
                        t = checkTransition(action,None,init_struct,theory.transition_theory,Nstate[i],s2,Nonaction)
                        if t != False:
                            trs = transitiongraph.transtions.get((i,j),[])
                            trs.append(t)
                            transitiongraph.transtions[(i,j)] = trs
                            if not (j in reachedStates):
                                tempstate.append(j)
                                reachedStates.append(j)
                    else:
                        q = 0
                        for arg in e:
                            t = checkTransition(action,arg,init_struct,theory.transition_theory,Nstate[i],s2,Nonaction,q)
                            if t != False:
                                trs = transitiongraph.transtions.get((i,j),[])
                                trs.append(t)
                                transitiongraph.transtions[(i,j)] = trs
                                if not (j in reachedStates):
                                    tempstate.append(j)
                                    reachedStates.append(j)
                            q += 1
                j += 1
    print(reachedStates)
    print(len(reachedStates))
    for r in reachedStates:
        print(transitiongraph.states[r])
    return initialStates


def AlternativeAlg2(transitiongraph:TransiotionGraph,Nstate:List,Nnextstate:List,Nonaction:dict,init_struct:Structure,theory:TheoryBlock):
    reachedStates =[]
    nextreachedState = []
    initialStates = []
    i = 0
    for s1 in Nstate:
        t = checkTransition("",None,init_struct,theory.init_theory,s1,[],{})
        if t != False:
            nextreachedState.append(i)
            reachedStates.append(i)
            initialStates.append(i)
        i += 1
    print("inital state")
    print(reachedStates)
    tempstate = nextreachedState.copy()
    while len(tempstate) > 0 :
        nextreachedState = tempstate.copy()
        tempstate = []
        for i in nextreachedState:
            for action , extentsion in transitiongraph.aextentions.items():
                e = extentsion[0]
                t = False
                if e == [[]]:
                    t = findnextStates(transitiongraph,action,None,init_struct,theory.transition_theory,Nstate[i],Nonaction)
                    for j in t[0]:
                        trs = transitiongraph.transtions.get((i,j),[])
                        trs.append(t[1])
                        transitiongraph.transtions[(i,j)] = trs
                        if not (j in reachedStates):
                            tempstate.append(j)
                            reachedStates.append(j)
                else:
                    q = 0
                    for arg in e:
                        #print("act.................")
                        #print(action)
                        #print(arg)
                        t = findnextStates(transitiongraph,action,arg,init_struct,theory.transition_theory,Nstate[i],Nonaction,q)
                        for j in t[0]:
                            trs = transitiongraph.transtions.get((i,j),[])
                            trs.append(t[1])
                            transitiongraph.transtions[(i,j)] = trs
                            if not (j in reachedStates):
                                tempstate.append(j)
                                reachedStates.append(j)
                        q += 1

    print(reachedStates)
    print(len(reachedStates))
    for r in reachedStates:
        print(transitiongraph.states[r])
    return initialStates

def findnextStates(transitiongraph:TransiotionGraph,action:str,args,init_struct:Structure,transition_theory:TheoryBlock,Nstate:List,non_action:dict,argindex:int=0):
    actionPred = None
    no_concurrency = []
    for a , act in non_action.items():
        if a == action:
            i = 0
            while i < len(act):
                if i != argindex:
                    no_concurrency += [act[i]]
                else:
                    actionPred = act[i].sub_exprs[0]
                i+=1
        else:
            no_concurrency += act     
    testth = TheoryBlock(name="Transit",vocab_name=transition_theory.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
    if actionPred is None:
        testth.constraints = OrderedSet(Nstate+no_concurrency)
    else:
        testth.constraints = OrderedSet(Nstate+[actionPred]+no_concurrency)
    interp = transition_theory.interpretations
    transition_theory.interpretations = {}
    p = Theory(init_struct,transition_theory,testth)
    res = list(p.expand())
    transition_theory.interpretations = interp
    second_step =False
    nextstates = []
    j=0
    """print("act pred")
    if str(actionPred.sub_exprs) == str([1,1]):
        print(actionPred)
        print(Nstate)
        print(transition_theory.constraints)
        for d in transition_theory.definitions:
            for r in d.rules:
                print(r)"""
    for i, xi in enumerate(res):
        if xi == 'No models.':
            second_step = True
        elif type(xi) != str:
            nextstates += (matchingstates(xi,transitiongraph))
        j+=1
    #print("next states ...")
    #print(nextstates)
    if second_step and j==1:
        return ([],actionPred)
    return (list(set(nextstates)),actionPred)
#action is the name of the action to checked; ini_struct is the given initial structure;
#Nstate is a list which contains the annotated of all its positive and negation predicates; Nnextstate is the same but for next time point
# cstt is the index of the cuurent state in Nstate; nstt is the index of the next state in Nnextstate
#non_action is dictionary containing the annotated negation of all actions; arg_action is the index for the argument of the action to be checked
def checkTransition(action:str,args,init_struct:Structure,transition_theory:TheoryBlock,Nstate:List,Nnextstate:List,non_action:dict,argindex:int=0):
    actionPred = None
    #if args is None:
    #    actionPred = AppliedSymbol(None,SymbolExpr(None,action,None,None),[])
    #else:
    #    actionPred = AppliedSymbol(None,SymbolExpr(None,action,None,None),args)
    no_concurrency = []
    for a , act in non_action.items():
        if a == action:
            i = 0
            while i < len(act):
                if i != argindex:
                    no_concurrency += [act[i]]
                else:
                    actionPred = act[i].sub_exprs[0]
                i+=1
        else:
            no_concurrency += act     
    testth = TheoryBlock(name="Transit",vocab_name=transition_theory.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
    if actionPred is None:
        testth.constraints = OrderedSet(Nstate+Nnextstate+no_concurrency)
    else:
        testth.constraints = OrderedSet(Nstate+Nnextstate+[actionPred]+no_concurrency)
    interp = transition_theory.interpretations
    transition_theory.interpretations = {}
    p = Theory(init_struct,transition_theory,testth)
    res = list(p.expand())
    transition_theory.interpretations = interp
    second_step =False
    j=0
    for i, xi in enumerate(res):
        if xi == 'No models.':
            second_step = True
        j+=1
    if second_step and j==1:
        return False
    return actionPred

def purgeImpossibleState(state,init_struct,init_theory):
    testth = TheoryBlock(name="StateTest",vocab_name=init_theory.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
    testth.constraints = OrderedSet(state)
    interp = init_theory.interpretations
    init_theory.interpretations = {}
    p = Theory(init_struct,init_theory,testth)
    res = list(p.expand())
    init_theory.interpretations = interp
    second_step =False
    j=0
    for i, xi in enumerate(res):
        if xi == 'No models.':
            second_step = True
        j+=1
    if second_step and j==1:
        return True
    return False

def model_expand(*theories: Union[TheoryBlock, Structure, Theory],
                 max: int = 10,
                 timeout_seconds: int = 10,
                 complete: bool = False,
                 extended: bool = False,
                 sort: bool = False
                 ) -> Iterator[str]:
    """Returns a (possibly empty) list of models of the combination of theories,
    followed by a string message.

    For example, ``print(model_expand(T, S))`` will return (up to) 10
    string representations of models of theory named ``T``
    expanding structure named ``S``.

    The string message can be one of the following:

    - ``No models.``

    - ``More models may be available.  Change the max argument to see them.``

    - ``More models may be available.  Change the timeout_seconds argument to see them.``

    - ``More models may be available.  Change the max and timeout_seconds arguments to see them.``

    Args:
        theories (Union[TheoryBlock, Structure, Theory]): 1 or more (data) theories.
        max (int, optional): max number of models. Defaults to 10.
        timeout_seconds (int, optional): timeout_seconds seconds. Defaults to 10.
        complete (bool, optional): True to obtain complete structures. Defaults to False.
        extended (bool, optional): use `True` when the truth value of
                inequalities and quantified formula is of interest
                (e.g. for the Interactive Consultant). Defaults to False.
        sort (bool, optional): True if the models should be in alphabetical order. Defaults to False.

    Yields:
        str
    """
    problem = Theory(*theories, extended=extended)
    PROCESS_TIMINGS['ground'] = time.time() - PROCESS_TIMINGS['ground']

    solve_start = time.time()
    ms = list(problem.expand(max=max, timeout_seconds=timeout_seconds, complete=complete))
    if isinstance(ms[-1], str):
        ms, last = ms[:-1], ms[-1]
    else:
        last = ""
    if sort:
        ms = sorted([str(m) for m in ms])
    out = ""
    for i, m in enumerate(ms):
        out = out + (f"{NEWL}Model {i+1}{NEWL}==========\n{m}\n")
    yield out + last
    PROCESS_TIMINGS['solve'] += time.time() - solve_start


def model_propagate(*theories: Union[TheoryBlock, Structure, Theory],
                    sort: bool = False,
                    complete: bool = False,
                    ) -> Iterator[str]:
    """
    Returns a list of assignments that are true in any model of the combination of theories.

    Terms and symbols starting with '_' are ignored.

    For example, ``print(model_propagate(T, S))`` will return the assignments
    that are true in any expansion of the structure named ``S``
    consistent with the theory named ``T``.

    Args:
        theories (Union[TheoryBlock, Structure, Theory]): 1 or more (data) theories.
        sort (bool, optional): True if the assignments should be in alphabetical order. Defaults to False.
        complete (bool, optional): True when requiring a propagation including
                 negated function value assignments. Defaults to False.

    Yields:
        str
    """
    ground_start = time.time()

    problem = Theory(*theories)
    PROCESS_TIMINGS['ground'] += time.time() - ground_start
    solve_start = time.time()
    if sort:
        ms = [str(m) for m in problem._propagate(tag=S.CONSEQUENCE,
                                                 complete=complete)]
        ms = sorted(ms[:-1]) + [ms[-1]]
        out = ""
        for i, m in enumerate(ms[:-1]):
            out = out + (f"{NEWL}Model {i+1}{NEWL}==========\n{m}\n")
        yield out + f"{ms[-1]}"
    else:
        yield from problem._propagate(tag=S.CONSEQUENCE, complete=complete)
    PROCESS_TIMINGS['solve'] += time.time() - solve_start

def maximize(*theories: Union[TheoryBlock, Structure, Theory],
             term: str
             ) -> Theory:
    """Returns a model that maximizes `term`.

    Args:
        theories (Union[TheoryBlock, Structure, Theory]): 1 or more (data) theories.
        term (str): a string representing a term

    Yields:
        str
    """
    return next(Theory(*theories).optimize(term, minimize=False).expand())

def minimize(*theories: Union[TheoryBlock, Structure, Theory],
             term: str
             ) -> Theory:
    """Returns a model that minimizes `term`.

    Args:
        theories (Union[TheoryBlock, Structure, Theory]): 1 or more (data) theories.
        term (str): a string representing a term

    Yields:
        str
    """
    return next(Theory(*theories).optimize(term, minimize=True).expand())

def decision_table(*theories: Union[TheoryBlock, Structure, Theory],
                   goal_string: str = "",
                   timeout_seconds: int = 20,
                   max_rows: int = 50,
                   first_hit: bool = True,
                   verify: bool = False
                   ) -> Iterator[str]:
    """Experimental. Returns a decision table for `goal_string`, given the combination of theories.

    Args:
        theories (Union[TheoryBlock, Structure, Theory]): 1 or more (data) theories.
        goal_string (str, optional): the last column of the table.
            Must be a predicate application defined in the theory, e.g. ``eligible()``.
        timeout_seconds (int, optional): maximum duration in seconds. Defaults to 20.
        max_rows (int, optional): maximum number of rows. Defaults to 50.
        first_hit (bool, optional): requested hit-policy. Defaults to True.
        verify (bool, optional): request verification of table completeness.  Defaults to False

    Yields:
        a textual representation of each rule
    """
    ground_start = time.time()
    problem = Theory(*theories, extended=True)
    PROCESS_TIMINGS['ground'] += time.time() - ground_start

    solve_start = time.time()
    models, timeout_hit = problem.decision_table(goal_string, timeout_seconds,
                                                 max_rows, first_hit, verify)
    PROCESS_TIMINGS['solve'] += time.time() - solve_start
    for model in models:
        row = f'{NEWL}∧ '.join(str(a) for a in model
            if a.sentence.code != goal_string)
        has_goal = model[-1].sentence.code == goal_string
        yield((f"{(f'  {row}{NEWL}') if row else ''}"
              f"⇒ {str(model[-1]) if has_goal else '?'}"))
        yield("")
    yield "end of decision table"
    if timeout_hit:
        yield "**** Timeout was reached. ****"

def determine_relevance(*theories: Union[TheoryBlock, Structure, Theory]) -> Iterator[str]:
    """Generates a list of questions that are relevant,
    or that can appear in a justification of a ``goal_symbol``.

    The questions are preceded with `` ? `` when their answer is unknown.

    When an *irrelevant* value is changed in a model M of the theories,
    the resulting M' structure is still a model.
    Relevant questions are those that are not irrelevant.

    If ``goal_symbol`` has an enumeration in the theory
    (e.g., ``goal_symbol := {`tax_amount}.``),
    relevance is computed relative to those goals.

    Definitions in the theory are ignored,
    unless they influence axioms in the theory or goals in ``goal_symbol``.

    Yields:
        relevant questions
    """
    problem = Theory(*theories, extended=True).propagate()
    problem.determine_relevance()
    for ass in problem.assignments.values():
        if ass.relevant:
            yield str(ass)


def pretty_print(x: Any ="") -> None:
    """Prints its argument on stdout, in a readable form.

    Args:
        x (Any, optional): the result of an API call. Defaults to "".
    """
    if type(x) is tuple and len(x)==2: # result of Theory.explain()
        facts, laws = x
        for f in facts:
            print(str(f))
        for l in laws:
            print(l.annotations['reading'])
    elif isinstance(x, types.GeneratorType):
        for i, xi in enumerate(x):
            if isinstance(xi, Assignments):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                print(xi)
            else:
                print(xi)
    elif isinstance(x, Theory):
        print(x.assignments)
    else:
        print(x)

def print_struct(x):
    #print("inside print struct...")
    if isinstance(x, types.GeneratorType):
        for i, xi in enumerate(x):
            if isinstance(xi, Structure):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                for interp in xi.interpretations.values():
                    print(interp.name)
                    print(interp)
            elif isinstance(xi, List) and len(xi)>0 :
                for s in xi:
                    if isinstance(s,Structure):
                        print(f"{NEWL}Model {i+1}{NEWL}==========")
                        for interp in s.interpretations.values():
                            print(interp)
                    else:
                        print(s)
            else:
                print(xi)
    elif isinstance(x, Theory):
        print(x.assignments)
    elif isinstance(x,List):
        i=0
        for s in x:
            if type(s) == tuple:
                if isinstance(s[0],Structure):
                    print(f"{NEWL}Model {i+1}{NEWL}==========")
                    for interp in s[0].interpretations.values():
                        print(interp)
            elif isinstance(s,Structure):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                for interp in s.interpretations.values():
                    print(interp)
            else:
                print(s)
            i+=1
    else:
        print(x)

def duration(msg: str = "") -> str:
    """Returns the processing time since the last call to `duration()`,
    or since the begining of execution"""
    global last_call
    out = round(time.process_time() - last_call, 3)
    last_call = time.process_time()
    return f"{out} {msg}"

def execute(self: IDP, capture_print : bool = False) -> Optional[str]:
    """ Execute the ``main()`` procedure block in the IDP program """
    global last_call
    last_call = time.process_time()
    main = str(self.procedures['main'])

    mybuiltins = {}

    out = []  # List of output lines
    if capture_print:
        def print(*args):
            out.append(''.join(map(str, args)))
        mybuiltins['print'] = print

    def pretty_print(x: Any ="") -> None:
        """Prints its argument on stdout, in a readable form.

        Args:
            x (Any, optional): the result of an API call. Defaults to "".
        """
        if type(x) is tuple and len(x)==2: # result of Theory.explain()
            facts, laws = x
            for f in facts:
                out.append(str(f))
            for l in laws:
                out.append(l.annotations['reading'])
        elif isinstance(x, types.GeneratorType):
            for i, xi in enumerate(x):
                if isinstance(xi, Assignments):
                    out.append(f"{NEWL}Model {i+1}{NEWL}==========")
                    out.append(str(xi))
                else:
                    out.append(str(xi))
        elif isinstance(x, List) and len(x)>0 :
            i=0
            for s in x:
                if isinstance(s,Structure):
                    out.append(f"{NEWL}Model {i+1}{NEWL}==========")
                    for interp in s.interpretations.values():
                        out.append(str(interp))
                else:
                    out.append(str(s))
                i+=1
        elif isinstance(x, Theory):
            out.append(str(x.assignments))
        else:
            out.append(str(x))

    mylocals = copy(self.vocabularies)
    mylocals.update(self.theories)
    mylocals.update(self.structures)
    mylocals.update(self.temporallogicformulas)
    mylocals['gc'] = gc
    mylocals['logging'] = logging
    mylocals['model_check'] = model_check
    mylocals['model_expand'] = model_expand
    mylocals['model_propagate'] = model_propagate
    mylocals['minimize'] = minimize
    mylocals['maximize'] = maximize
    mylocals['decision_table'] = decision_table
    mylocals['determine_relevance'] = determine_relevance
    mylocals['pretty_print'] = pretty_print
    mylocals['Theory'] = Theory
    mylocals['time'] = time
    mylocals['duration'] = duration
    mylocals['initialize'] = initialize
    mylocals['progression'] = progression
    mylocals['print_struct'] = print_struct
    mylocals['isinvariant'] = isinvariant
    mylocals['simulate'] = simulate
    mylocals['ForProgression'] = ForProgression
    mylocals['ProveModalLogic'] = ProveModalLogic 

    try:
        exec(main, mybuiltins, mylocals)
    except (SyntaxError, AttributeError) as e:
        raise IDPZ3Error(f'Error in procedure, {e}')
    if out:
        return linesep.join(out) + linesep

IDP.execute = execute





Done = True
