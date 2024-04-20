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
from multiprocessing.managers import BaseManager
from os import linesep
from sys import intern
import time
from tkinter import Variable
import types
from typing import Any, Iterator, List, Union, Optional
import subprocess
from z3 import Solver

from idp_engine.Expression import BOOL_SETNAME, FALSE, INT_SETNAME, ONE, OR, SETNAME, TRUE, VARIABLE, ZERO, AAggregate, AComparison, AConjunction, ADisjunction, AEquivalence, AFFormula, AGFormula, AIfExpr, AImplication, AMultDiv, APower, AQuantification, ARImplication, ASumMinus, AUFormula, AUnary, AXFormula, AppliedSymbol, Brackets, CCFormula, CLFormula, CTLFormula, DCFormula, DLFormula, EFFormula, EGFormula, EUFormula, EXFormula, Expression, FLFormula, ForNext, GLFormula, ICFormula, ILFormula, LFormula, NCFormula, NLFormula, NextAppliedSymbol, NowAppliedSymbol, Number, Operator, Quantee, RLFormula, SetName, StartAppliedSymbol, SymbolExpr, ULFormula, UnappliedSymbol, WLFormula, XLFormula

from .Parse import IDP, Enumeration, FunctionTuple, RangeElement, Ranges, SymbolDeclaration, SymbolInterpretation, TempLogic, TemporalDeclaration, TheoryBlock, Structure, TransiotionGraph, TupleIDP, TypeDeclaration, Vocabulary
from .Theory import Theory
from .Assignments import Status as S, Assignments
from .utils import BOOL, DATE, INT, NEWL, REAL, TIJD, IDPZ3Error, PROCESS_TIMINGS, OrderedSet, v_time
from .Annotate import annotate_exp_theory
import multiprocessing
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

def necessary_assignments(lasgn:List[Assignments|str],transitiongraph:TransiotionGraph):
    fluents = transitiongraph.fextentions.keys()
    ffluents = transitiongraph.ffextentions.keys()
    reallist = []
    if len(lasgn) > 0:
        reallist.append(lasgn[0])

    for i in range(len(lasgn)-1):
        if not isinstance(lasgn[i],str):
            j = 0
            for k, a  in lasgn[i].items():
                if type(a.sentence) == AppliedSymbol:
                    asymb = a.symbol_decl.name[:-len('_next')]
                    fluent_check = a.symbol_decl.is_next and (asymb  in fluents or asymb in ffluents )
                    if fluent_check:
                        if not isinstance(lasgn[i+1],str):
                            #print("afasdfds")
                            #print(type(lasgn[i+1][j]))
                            if str(a.sentence) == str(lasgn[i+1][k].sentence):
                                if a.value != lasgn[i+1][k].value:
                                    reallist.append(lasgn[i+1])
                                    break

                j += 1
        else:
            reallist.append(lasgn[i])

    return reallist
    #return [lasgn[i] for i in reallist]

def identifystatesparallel(assign,fluents:List,ffluents:List,allstates:List,lock,initialstate=False):
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
            fluent_check = False
            asymb = a.symbol_decl.name
            if initialstate:
                fluent_check = (asymb  in fluents or asymb in ffluents )
            else:
                asymb = a.symbol_decl.name[:-len('_next')]
                fluent_check = a.symbol_decl.is_next and (asymb  in fluents or asymb in ffluents )
            if fluent_check:
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
                if c is not None:
                    if len(states) == 0:
                        states.append([(c,asymb,args)])
                    else:
                        for s in states:
                            s.append((c,asymb,args))
                elif c is None:
                    if len(states) == 0:
                        states.append([(True,asymb,args)])
                        states.append([(False,asymb,args)])
                    else:
                        nstate = []
                        for s in states:
                            nstate.append(s+[(True,asymb,args)])
                            nstate.append(s+[(False,asymb,args)])
                        states = nstate
    #print("states.........,,,,,,")
    #print(states)
    matchedStates = []
    statesVisited = []
    i = 0
    for s in states:
        nstrue = 0
        for e2 in s:
            if e2[0]== True:
                nstrue += 1
        statenmbr = 0
        for os in allstates:
            ntrue = 0
            allmatch = False
            onematch = False
            for e in os:
                #print(e)
                onematch = True
                if e[0] == True:
                    onematch = False
                    ntrue += 1
                    for e2 in s:
                        if e2[0]== True and e2[1] == e[1] and str(e2[2]) == str(e[2]):
                            #print("wordkssfd")
                            onematch = True
                            break
                if not onematch:
                    allmatch = False
                    break
                allmatch =True
            
            if ntrue == nstrue and allmatch:
                matchedStates.append(i)
                statesVisited.append(statenmbr)
                break
            statenmbr += 1
        i += 1
    #print("matched states")
    #print(matchedStates)
    addedstates = []
    index = len(allstates)
    i = 0
    #print("states list...")
    for s in states:
        if not (i in matchedStates):
            #checking if function fluents have a true value in a given state.
            #print(s)
            validstate = True
            ffluentnumber :dict(str,int) = {}
            existtrue = 0
            for e in s:
                if e[1] in ffluents:
                    name = e[1]+str(e[2][:-1])
                    nm = ffluentnumber.get(name,0)
                    ffluentnumber[name] = nm
                    if e[0]==True:
                        ffluentnumber[name] = nm+1
                        existtrue += 1
            for v in ffluentnumber.values():
                if v != 1:
                    validstate = False
                    break
            if validstate:
                with lock:
                    allstates.append(s)
                    addedstates.append(len(allstates))
                index += 1
        i+=1
    #print("added states")
    #print(addedstates)
    return statesVisited + addedstates


def identifystates(assign,transitiongraph:TransiotionGraph,initialstate=False):
    fluents = transitiongraph.fextentions.keys()
    ffluents = transitiongraph.ffextentions.keys()
    out : dict[SymbolDeclaration, List[TupleIDP]] = {}
    nullary: dict[SymbolDeclaration, Any] = {}
    states = []
    print("matching states .....")
    print(initialstate)
    for a in assign.values():
        if type(a.sentence) == AppliedSymbol:
            #print(a)
            args = [e for e in a.sentence.sub_exprs]
            args = tuple(args)
            c = None
            default = False
            fluent_check = False
            asymb = a.symbol_decl.name
            if initialstate:
                fluent_check = (asymb  in fluents or asymb in ffluents )
            else:
                asymb = a.symbol_decl.name[:-len('_next')]
                fluent_check = a.symbol_decl.is_next and (asymb  in fluents or asymb in ffluents )
            if fluent_check:
                print(a)
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
                if c is not None:
                    if len(states) == 0:
                        states.append([(c,asymb,args)])
                    else:
                        for s in states:
                            s.append((c,asymb,args))
                elif c is None:
                    if len(states) == 0:
                        states.append([(True,asymb,args)])
                        states.append([(False,asymb,args)])
                    else:
                        nstate = []
                        for s in states:
                            nstate.append(s+[(True,asymb,args)])
                            nstate.append(s+[(False,asymb,args)])
                        states = nstate
    #print("states.........,,,,,,")
    #print(states)
    matchedStates = []
    statesVisited = []
    i = 0
    # for s in states:
    #     nstrue = 0
    #     for e2 in s:
    #         if e2[0]== True:
    #             nstrue += 1
    #     statenmbr = 0
    #     for os in transitiongraph.states:
    #         ntrue = 0
    #         allmatch = False
    #         onematch = False
    #         #print("os")
    #         #print(os)
    #         for e in os:
    #             #print(e)
    #             onematch = True
    #             if e[0] == True:
    #                 onematch = False
    #                 ntrue += 1
    #                 for e2 in s:
    #                     if e2[0]== True and e2[1] == e[1] and str(e2[2]) == str(e[2]):
    #                         #print("wordkssfd")
    #                         onematch = True
    #                         break
    #             if not onematch:
    #                 allmatch = False
    #                 break
    #             allmatch =True
            
    #         if ntrue == nstrue and allmatch:
    #             matchedStates.append(i)
    #             statesVisited.append(statenmbr)
    #             break
    #         statenmbr += 1
    #     i += 1
    #print("matched states")
    #print(matchedStates)
    #USES THE CHRACTERISTIC THAT THE ORDER OF PREDICATES IS THE SAME ACROSS DIFFERENT STATES.
    for s in states:
        statenmbr = 0
        for os in transitiongraph.states:
            onematch = True
            #print("os")
            #print(os)
            if len(os) != len(s):
                print("ERROR:THE LENGTHS SHOULD MAYCH !!!!!!!!!!!!")
                return
            j = 0
            while j < len(os):
                if os[j][0] != s[j][0]:
                    onematch = False
                    break
                j +=1
            if onematch:
                matchedStates.append(i)
                statesVisited.append(statenmbr)
                break
            statenmbr += 1
        i += 1
    addedstates = []
    index = len(transitiongraph.states)
    i = 0
    #print("states list...")
    for s in states:
        if not (i in matchedStates):
            #checking if function fluents have a true value in a given state.
            #print(s)
            validstate = True
            ffluentnumber :dict(str,int) = {}
            existtrue = 0
            for e in s:
                if e[1] in ffluents:
                    name = e[1]+str(e[2][:-1])
                    nm = ffluentnumber.get(name,0)
                    ffluentnumber[name] = nm
                    if e[0]==True:
                        ffluentnumber[name] = nm+1
                        existtrue += 1
            for v in ffluentnumber.values():
                if v != 1:
                    validstate = False
                    break
            #if existtrue != 1:
            #    validstate = False
            #    break
            #print("ffluents  ...")
            #print(ffluentnumber)
            if validstate:
                #print("valid index")
                #print(index)
                transitiongraph.states.append(s)
                addedstates.append(index)
                index += 1
        i+=1
    #print("added states")
    #print(addedstates)
    return statesVisited + addedstates

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
        #print("negataevie theoriies")
        #print(fth.constraints)
        return (s,fth)

def initialize(theory:TheoryBlock,struct:Structure,nbmodel=10):
    #print("inside initialize")
    #print(theory.init_theory.definitions)
    problem = Theory(theory.init_theory,struct.init_struct)
    PROCESS_TIMINGS['ground'] = time.time() - PROCESS_TIMINGS['ground']

    solve_start = time.time()
    ms = list(problem.expand(max=nbmodel, timeout_seconds=10, complete=False))
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

#Start inclusive , end exclusive
def progression(theory:TheoryBlock,struct,nbmodel=10,additional_theory:TheoryBlock=None,start=0,end=-1):
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
    out = []
    PROCESS_TIMINGS['ground'] = time.time() - PROCESS_TIMINGS['ground']
    solve_start = time.time()
    if isinstance(struct,List):
        #When the result is received either form initialize or progression
        if end == -1:
            end = len(struct)
        else:
            if start>end:
                return "The end index should be larger than start"
            if end>len(struct):
                return "end should be smaller than the length of input structures"
            if start <0:
                return "start should be positive"
            
        j = 1
        for xi in struct:
            if j>start and j <= end:
                strcx = None
                thrx =None
                if isinstance(xi,Structure):
                    strcx = xi
                    #pass
                elif isinstance(xi[0],Structure) and isinstance(xi[1],TheoryBlock):
                    strcx =xi[0]
                    thrx = xi[1]
                else:
                    j += 1
                    continue
                if additional_theory:
                    problem = Theory(theory.bistate_theory,strcx,thrx,additional_theory)
                else:
                    problem = Theory(theory.bistate_theory,strcx,thrx)
                voc = strcx.voc.idp.next_voc.get(theory.vocab_name+'_next',None)
                if voc is None:
                    print("Error vocabulary is wrong")
                    return
                if problem is None:
                    pass
                ms = list(problem.expand(max=nbmodel, timeout_seconds=10, complete=False))
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
                out.append(last + " For Structure " + str(j))
            j += 1
    elif isinstance(struct,tuple) or isinstance(struct,Structure):
        #Used in simulate and in case a single structure is given
        strcx = None
        thrx =None
        if isinstance(struct,Structure):
            strcx = struct
        elif isinstance(struct[0],Structure) and isinstance(struct[1],TheoryBlock):
            strcx =struct[0]
            thrx = struct[1]
        else:
            print("Wrong input given")
            return
        if not isinstance(struct[0],Structure):
            print("Error a structure should be given")
            return
        if additional_theory:
            problem = Theory(theory.bistate_theory,strcx,thrx,additional_theory)
        else:
            problem = Theory(theory.bistate_theory,strcx,thrx)
        #problem = Theory(theory.bistate_theory,struct)
        voc = strcx.voc.idp.next_voc.get(theory.vocab_name+'_next',None)
        if voc is None:
            print("Error vocabulary is wrong")
            return
        if problem is None:
            pass
        ms = list(problem.expand(max=nbmodel, timeout_seconds=10, complete=False))
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
    

def simulate(theory:TheoryBlock,struct:Structure,nbmodel=10):
    result = initialize(theory,struct,nbmodel=nbmodel)
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
                result = progression(theory,result[i-1],nbmodel=nbmodel)
            else:
                result = progression(theory,result[i-1],th,nbmodel=nbmodel)
            print_struct(result)
        else:
            result = progression(theory,result[i-1],nbmodel=nbmodel)
            print_struct(result)

def ForProgression(theory:TheoryBlock,struct,number:int,nbmodel=10):
    m = '\n' +"Generated models by progression number "
    out = [m+str(1)]
    result = progression(theory,struct,nbmodel=nbmodel)
    out += result
    print_struct(result)
    i = 2
    while i<=number:
        out += [m+str(i)]
        result = progression(theory,result,nbmodel=nbmodel)
        out += result
        print_struct(result)
        i+=1
    return out

def isinvariant(theory:TheoryBlock,invariant:TheoryBlock,s:Structure|None=None,forward_chaining=False):
    if not theory.ltc:
        return "Invariant proving is only for LTC theories"
    #TO DO: check if the invariant is correctly formulated
    if len(invariant.constraints) > 1:
        return "Only one formula should be specified for invariant"
    if len(invariant.constraints) == 0:
        return "Please provide an invariant"
    if forward_chaining:
        if s:
            return forward_chain(theory,invariant,s)
        else:
            return forward_chain(theory,invariant)
    invorg = None
    for c in invariant.constraints:
        invorg = c
    inv = invorg.init_copy()
    inv2 = inv.init_copy()
    #print("ch1")
    #Checking the formula is valid LTC expression
    time: SetName = SETNAME(TIJD)
    t: Variable = VARIABLE(v_time,time)
    qt: Quantee = Quantee(None,[t],time) 
    invorg = AQuantification(None,None,'forall',[qt],invorg)
    invorg.annotate(theory.voc,{},True)
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
        p0 = model_expand(theory.init_theory,invariant,s.static_now)
    else:
        p0 = model_expand(theory.init_theory,invariant)
    j =0
    for i, xi in enumerate(p0):
        #print(xi)
        if xi == 'No models.':
            first_step = True
        j+=1
    if not first_step or j > 1:
        return "Invariant is FALSE: It cannot be proven at the initial time point"
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
        p1 = model_expand(theory.transition_theory,invariant,invariant2,s.static_next)
    else:
        p1 = model_expand(theory.transition_theory,invariant,invariant2)
    j=0
    for i, xi in enumerate(p1):
        #print(xi)
        if xi == 'No models.':
            second_step = True
        j+=1
    if not second_step or j>1:
        return "Invariant is FALSE: Induction step cannot be proven"
    return "Invariant is TRUE"

def forward_chain(theory:TheoryBlock,invariant:TheoryBlock,struct:Structure|None=None):
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
    """output = ""
    print("adjusted formula")
    print(f)
    output += str(f) + '\n'"""
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
        output += str(c) + '\n'
    for d in exp_th.definitions:
        for r in d.rules:
            print(r)
            output += str(r) + '\n'"""
    
    p1 = None
    if struct is not None:
        #TO DO : IF THE ANNOTATE OF STRUCTURE CHANGES THEN THIS CODE WOULD ALSO CHANGE
        struct.static_expanded.voc = voc
        for i in struct.static_expanded.interpretations.values():
            i.annotate(voc, {})
        voc.add_voc_to_block(struct.static_expanded)
        p1 = model_expand(exp_th,invariant,struct.static_expanded,timeout_seconds=50)
    else:
        p1 = model_expand(exp_th,invariant,timeout_seconds=50)
    second_step =False
    j=0
    for i, xi in enumerate(p1):
        #print(xi)
        if xi == 'No models.':
            second_step = True
        j+=1
    #return output
    if not second_step or j>1:
        return "Forward chaining formula is FALSE"
    return "Forward chaining formula is TRUE"

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
    expression.sub_exprs[0] = r
    return n
    
def adjust_implicant(expression:Expression,tempdcl:List[TemporalDeclaration]):
    if isinstance(expression,(StartAppliedSymbol,NowAppliedSymbol,NextAppliedSymbol,ForNext)):
        return "Not allowed to use Start/Now/Next/ForNext"
    if isinstance(expression,AppliedSymbol):
        for t in tempdcl:
            if expression.symbol.name == t.symbol.name:
                last = expression.sub_exprs.pop()
                if isinstance(last,ASumMinus):
                    for op in last.operator:
                        if not op == '+':
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
    
#TO DO:Test if empty tmpdcl is given
def adjust_sub(expression:Expression,tempdcl:List[TemporalDeclaration],n:int):
    if isinstance(expression,(StartAppliedSymbol,NowAppliedSymbol,NextAppliedSymbol)):
        return "Not allowed to use Start/Now/Next"
    if isinstance(expression,ForNext):
        return adjust_sub(expandForNext(expression),tempdcl,n)
    if isinstance(expression,AppliedSymbol):
        for t in tempdcl:
            if expression.symbol.name == t.symbol.name:
                last = expression.sub_exprs.pop()
                if isinstance(last,ASumMinus):
                    for op in last.operator:
                        if not op == '+':
                            return "Only addition is acceptable in atecedant"
                    sum = 0
                    for e in last.sub_exprs:
                        if isinstance(e,Number) and e.type == INT_SETNAME:
                            sum += e.py_value
                    if sum > n :
                        return "Cant use numbers higher than the upperlimit"
                    level = sum
                    if level != 0:
                        expression.symbol.name = expression.symbol.name + '_' + str(level)
                        expression.code = intern(str(expression))
                        expression.str = expression.code
                    break   
                break
    j = 0
    for e in expression.sub_exprs:
        r = adjust_sub(e,tempdcl,n)
        if isinstance(r,str):
            return r
        expression.sub_exprs[j] = r
        j += 1
    expression.code = intern(str(expression))
    expression.str = expression.code
    return expression

def expandForNext(exp:ForNext):
    n = exp.num.py_value
    #range(n+1) = 0...n (n is included)
    expanded = [expanditer(exp.exp.init_copy(),i,exp.var) for i in range(n+1)]
    ops = ['and'] * (len(expanded)-1)
    return AConjunction(None,ops,expanded)

def expanditer(expression:Expression,i:int,s:SymbolExpr):
    if isinstance(expression,(UnappliedSymbol,Variable)):
        if s.name == expression.name:
            return Number(number=str(i))
    j = 0
    for e in expression.sub_exprs:
        r = expanditer(e,i,s)
        expression.sub_exprs[j] = r
        j += 1
    expression.code = intern(str(expression))
    expression.str = expression.code
    return expression

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
    
def ProveModalLogic(ltllogic:TempLogic,init_structure:Structure,theory:TheoryBlock,generate_transition_machine=False):
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
    print(problem.extensions)
    TransmachconstructTime = time.time()
    Alg3 = True  
    transitiongraph = TransiotionGraph(init_structure.voc,problem,Alg3)
    #print("transiiton graph states")
    #for l in transitiongraph.states:
    #    print(l)
    #Formula for stating ftemporal predicates are functions meaning they have exactly one value at each time
    ffluentConst = []
    ffluentinit = []
    """for d in voc_now.declarations:
        if isinstance(d,SymbolDeclaration):
            if d.name in init_structure.voc.ftemproral:
                j = 0
                qt = []
                qt2 = []
                subex =[]
                subex2 = []
                lendom = len(d.domains)
                for q in d.domains:
                    if j != lendom -1 :
                        qt.append(Quantee(None,[VARIABLE(d.name+str(j),q.init_copy())],q.init_copy()))
                        qt2.append(Quantee(None,[VARIABLE(d.name+str(j),q.init_copy())],q.init_copy()))
                    subex.append(UnappliedSymbol(None,d.name+str(j)))
                    subex2.append(UnappliedSymbol(None,d.name+str(j)))
                    j += 1
                outpq = [Quantee(None,[VARIABLE(d.name+str(lendom-1),d.domains[lendom-1].init_copy())],d.domains[lendom-1].init_copy())]
                outpq2 = [Quantee(None,[VARIABLE(d.name+str(lendom-1),d.domains[lendom-1].init_copy())],d.domains[lendom-1].init_copy())]
                aggconst = AAggregate(None,"#",outpq,f=AppliedSymbol(None,SymbolExpr(None,d.name+"_next",None,None),subex))
                cardinality = AComparison(None,"=",[aggconst,ONE])
                uniquant = AQuantification(None,None,"forall",qt,cardinality)
                uniquant.annotate(theory.transition_theory.voc,{})

                aggconst2 = AAggregate(None,"#",outpq2,f=AppliedSymbol(None,SymbolExpr(None,d.name,None,None),subex2))
                cardinality2= AComparison(None,"=",[aggconst2,ONE])
                uniquant2 = AQuantification(None,None,"forall",qt2,cardinality2)
                uniquant2.annotate(theory.transition_theory.voc,{})

                ffluentConst.append(uniquant)
                ffluentConst.append(uniquant2)
                ffluentinit.append(uniquant2)"""
    print("fluent const")
    print(ffluentConst)
    no_conc = False
    Posaction = {}
    Nonaction = {}
    #To make beforehand the negation of actions and annotate them
    if no_conc:
        for action , extentsion in transitiongraph.aextentions.items():
            e = extentsion[0]
            if e == [[]]:
                na = AppliedSymbol(None,SymbolExpr(None,action,None,None),[])
                na.annotate(theory.transition_theory.voc,{})
                nal = Posaction.get(action,[])
                nal.append(na)
                Posaction[action] = nal
            else:
                for arg in e:
                    na = None
                    if len(extentsion) > 2 and extentsion[2] == True:
                        ap = AppliedSymbol(None,SymbolExpr(None,action,None,None),arg[:-1])
                        na = AComparison(None,"=",[ap,arg[-1]])
                    else:
                        na = AppliedSymbol(None,SymbolExpr(None,action,None,None),arg)
                    na.annotate(theory.transition_theory.voc,{})
                    nal = Posaction.get(action,[])
                    nal.append(na)
                    Posaction[action] = nal
    else:
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
                    na = None
                    if len(extentsion) > 2 and extentsion[2] == True:
                        ap = AppliedSymbol(None,SymbolExpr(None,action,None,None),arg[:-1])
                        na = AUnary(None,['not'],AComparison(None,"=",[ap,arg[-1]]))
                    else:
                        na = AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,action,None,None),arg))
                    na.annotate(theory.transition_theory.voc,{})
                    nal = Nonaction.get(action,[])
                    nal.append(na)
                    Nonaction[action] = nal
    Nstate = []
    Nnextstate = []
    if not Alg3:
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
            i += 1
    initialStates = []
    if not Alg3:
        initialStates = AlternativeAlg2(transitiongraph,Nstate,Nnextstate,Nonaction,temps,theory)
    else:
        #initialStates = AlternativeAlg3(transitiongraph,Nonaction,temps,theory,ffluentinit,ffluentConst)
        if no_conc:
            initialStates = AlternativeAlg3(transitiongraph,Posaction,temps,theory,no_conc=True)
        else:
            #This had the beter performance
            initialStates = AlternativeAlg3(transitiongraph,Nonaction,temps,theory)
            #initialStates = AlternativeAlgparallel(transitiongraph,Nonaction,temps,theory)

    TransmachconstructTime = time.time() - TransmachconstructTime
    """print("transition states")
    print(transitiongraph.aextentions)
    print(transitiongraph.states)
    print(len(transitiongraph.states))
    print("transition list")
    print(len(transitiongraph.transtions.keys()))
    for k ,v in transitiongraph.transtions.items():
        print(k,v)"""

    #print(problem.extensions)
    ProbTransTime = time.time()
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
                if d.codomain != BOOL_SETNAME:
                    probacts[d.name] += [d.codomain]
    #TO DO: Check that the sorts dont have inifinte types like INT
    
    tsets = "SETS "
    i = 0
    numsets = []
    setenum = False
    for s , e in probsets.items():
        #tsets += s 
        notNum = True
        if e == [[]]:
            if i != 0:
                tsets += " ; "
            tsets += s + " =BOOL"
            setenum = True
        else:
            if not isinstance(e[0][0],Number):
                if i != 0:
                    tsets += " ; "
                setenum = True
                tsets += s + " ={ "
                j = 0
                for elem in e:
                    if j != 0:
                        tsets += " , "
                    tsets += str(elem[0])
                    j += 1
                tsets += " }"
            else:
                notNum = False
                numsets.append(s)
                i -= 1
        
        #if i != len(probsets.keys()) -1 and notNum :
        #    tsets += ";"
        i += 1
    #could also be if i != 0
    if not setenum:
        tsets =""
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
    if i == 0:
        tvars= ""
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
                    domname = "(" + str(probnumset[d.name][0]) + ".." + str(probnumset[d.name][1]) +")"
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
    if i ==0:
        tinvar =""
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
    if leninitstate == 0:
        tinint =""

    #it contains the list of conditions for each action
    actioncondition :dict(str,List[str]) = {}
    actionoperation :dict(str,List) = {}
    transitmachine:dict((int,AppliedSymbol),List[int])={}

    for trans ,act in transitiongraph.transtions.items():
        for a in act:
            n = transitmachine.get((trans[0],a),[])
            n.append(trans[1])
            transitmachine[(trans[0],a)] = n
    #This is where if there are multiple final states for state and action pair, then CHOICE will be used for the final state.
    for stateaction ,nxtstates in transitmachine.items():
        a = stateaction[1]
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
        StateToProb(transitiongraph.states[stateaction[0]],beginstate)
        endstates = []
        for ns in nxtstates:
            endstates.append({})
            StateToProb(transitiongraph.states[ns],endstates[-1])
        if j > 0  and len(beginstate.keys()) > 0:
            cnd += " & "
        cnd += toProbSubstitution(" = "," & ",beginstate)
        cnd += " ) "
        if j > 0 or len(beginstate.keys()) > 0: 
            conds.append(cnd)
            actioncondition[n] = conds
            op =""
            if len(endstates) == 1:
                op = cnd + " THEN " + toProbSubstitution(" := ", " ; ", endstates[0])
            else:
                op = cnd + " THEN CHOICE "
                ei =0
                for e in endstates:
                    if ei != 0:
                        op += " OR "
                    op += toProbSubstitution(" := ", " ; ", e)
                    ei += 1
                op += " END "
            oprtns = actionoperation.get(n,[])
            oprtns.append(op)
            actionoperation[n] = oprtns
    """for trans ,act in transitiongraph.transtions.items():
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
                actionoperation[n] = oprtns"""
    
    toprts ="OPERATIONS "
    actnum = 0
    for a , domains in probacts.items():
        actstr = ""
        if actnum != 0:
            actstr += " ; "
        actstr += a 
        argn = len(domains)
        if argn > 0:
            actstr += "("
        j = 0
        while j < argn:
            if j != 0:
                actstr += ", "
            actstr += a + str(j)
            j += 1
        if argn > 0:
            actstr += ")"
        actstr += " = PRE "
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
        cndln = len(actioncondition.get(a,[]))
        if cndln > 0:
            if argn > 0:
                actstr += " & ("
            else:
                actstr += "("
        j = 0
        for a1 in actioncondition.get(a,[]):
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
        for ops in actionoperation.get(a,[]):
            if j == 0:
                actstr += " IF "
            else:
                actstr += " ELSIF "
            actstr += ops
            j += 1
        if len(actionoperation.get(a,[])) > 0:
            actstr += " END END "
        else:
            actstr += " skip END "
        toprts += actstr
        actnum += 1
    if len(probacts.keys()) == 0:
        toprts =""
    
    machine = "MACHINE Test" + '\n' + tsets + '\n' + tvars + '\n' + tinvar + \
          '\n' + tinint + '\n' + toprts + '\n' + "END"
    print(machine)
    ProbTransTime = time.time() - ProbTransTime
    
    f = open("test.mch","w")
    f.write(machine)
    f.close()  
    ProbSolvingTime = 0
    reserrror= ""
    resmessage = ""
    if generate_transition_machine:
        #open('states.dot', 'w').close()
        a =subprocess.run('C:\Prob\probcli  test.mch -model-check -spdot states.dot',shell=True,capture_output=True)  
        stsf = open('states.dot',"r")
        resmessage = stsf.read()
        stsf.close()
        #resmessage = a.stdout.decode()
        reserrror = a.stderr.decode()
    else:
        #"(F {owns = owns \/ {(1,B1)}}) & G {F {john_owns=TRUE}}"
        #ltlf = "(EF { (2,B1):owns })" 
        ltlf = translateLogicFormula(ltllogic.formula,probnumset)
        ProbSolvingTime = time.time()
        #a = subprocess.run(f'C:\Prob\probcli --help ',shell=True,capture_output=True)
        #a =subprocess.run('C:\Prob\probcli  test.mch -model-check -spdot states.dot',shell=True,capture_output=True)  
        #a =subprocess.run('C:\Prob\probcli  test.mch -animate 20 -his history.txt',shell=True,capture_output=True)          
        if isinstance(ltllogic.formula,(ILFormula,DLFormula,CLFormula,NLFormula,XLFormula,FLFormula,GLFormula,ULFormula,WLFormula,RLFormula)):
            a = subprocess.run(f'C:\Prob\probcli -ltlformula "{ltlf}" test.mch -disable_timeout',shell=True,capture_output=True) # -model-check -spdot states.dot
        else:
            a = subprocess.run(f'C:\Prob\probcli -ctlformula "{ltlf}" test.mch -disable_timeout',shell=True,capture_output=True)
        ProbSolvingTime = time.time() - ProbSolvingTime
        resmessage = a.stdout.decode()
        reserrror = a.stderr.decode()
        
    nbTransitions = 0
    for k ,v in transitiongraph.transtions.items():
        nbTransitions += len(v)
    print(" Transition machine construction time:")
    print(TransmachconstructTime)
    print("prob translation time")
    print(ProbTransTime)
    print("prob solving time")
    print(ProbSolvingTime)
    print("number of states")
    print(len(transitiongraph.states))
    print("number of transitions")
    print(nbTransitions)

    print("PROBCLI............")
    print(resmessage)
    print(reserrror)
    return resmessage +'\n' + reserrror

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
    print("inside algoo2")
    print(reachedStates)
    print(len(reachedStates))
    for r in reachedStates:
        print(transitiongraph.states[r])
    return initialStates

def AlternativeAlg3(transitiongraph:TransiotionGraph,Nonaction:dict,init_struct:Structure,theory:TheoryBlock,ffluentinit=[],ffluentConst=[],no_conc=False):
    nextreachedState = []
    initialStates = []
    reachedStates = []
    z3solvetime = 0
    numreachedstate = 0
    Nstate : dict(int,List) = {}
    i = 0
    res = findnextStates(transitiongraph,"",None,init_struct,theory.init_theory,[],{},alg3=True)
    initialStates = res[0]
    z3solvetime = res[2]
    nextreachedState = initialStates.copy()
    reachedStates= initialStates.copy()
    if len(initialStates)==0:
        return []
    numreachedstate = max(initialStates)
    print("inital state")
    print(initialStates)
    tempstate = nextreachedState.copy()
    oldreached = -1
    #while len(tempstate) > 0 :
    while numreachedstate - oldreached > 0:
        #nextreachedState = tempstate.copy()
        print("next states")
        print(numreachedstate)
        #tempstate = []
        #for i in nextreachedState:
        for i in range(oldreached+1,numreachedstate+1):
            if i == oldreached+1:
               oldreached = numreachedstate
            Nstate[i] = translateToNstate(transitiongraph.states[i],theory)
            for action , extentsion in transitiongraph.aextentions.items():
                e = extentsion[0]
                t = False
                if e == [[]]:
                    t = []
                    #if no_conc:
                    #    ract = Nonaction[action][0]
                    #    t = findnextStates(transitiongraph,action,None,init_struct,theory.transition_theory,Nstate[i],Nonaction,alg3=True)
                    #else:
                    t = findnextStates(transitiongraph,action,None,init_struct,theory.transition_theory,Nstate[i],Nonaction,alg3=True)
                    for j in t[0]:
                        trs = transitiongraph.transtions.get((i,j),[])
                        trs.append(t[1])
                        transitiongraph.transtions[(i,j)] = trs
                        if j > numreachedstate:
                            numreachedstate = j
                        #if not (j in reachedStates):
                        #    tempstate.append(j)
                        #    reachedStates.append(j)
                    z3solvetime += t[2]
                    tempstate
                       
                else:
                    q = 0
                    for arg in e:
                        t = []
                        #if no_conc:
                        #    ract = Nonaction[action][q]
                        #    t = findnextStates(transitiongraph,action,arg,init_struct,theory.transition_theory,Nstate[i],Nonaction,q,alg3=True,ffluentconst=ffluentConst,realaction=ract)
                        #else:
                        t = findnextStates(transitiongraph,action,arg,init_struct,theory.transition_theory,Nstate[i],Nonaction,q,alg3=True)
                        for j in t[0]:
                            trs = transitiongraph.transtions.get((i,j),[])
                            trs.append(t[1])
                            transitiongraph.transtions[(i,j)] = trs
                            if j > numreachedstate:
                                numreachedstate = j
                            #if not (j in reachedStates):
                            #    tempstate.append(j)
                            #    reachedStates.append(j)
                        z3solvetime += t[2]
                        q += 1
    print("TOTAL Z3 SOLVING TIME:")
    print(z3solvetime)
    return initialStates

def AlternativeAlgparallel(transitiongraph:TransiotionGraph,Nonaction:dict,init_struct:Structure,theory:TheoryBlock,ffluentinit=[],ffluentConst=[],no_conc=False):
    initialStates = []
    z3solvetime = 0
    numreachedstate = 0

    CustomManager.register("TransitionGraph",TransiotionGraph)
    with CustomManager() as manager:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        
        res = findnextStatesparallel(transitiongraph,"",None,init_struct,theory.init_theory,[],{},lock,alg3=True,ffluentconst=ffluentinit)
        initialStates = res[0]
        z3solvetime = res[2]
        nextreachedState = initialStates.copy()
        if len(initialStates)==0:
            return []
        numreachedstate = max(initialStates)
        print("inital state")
        print(initialStates)

        # Create a shared dictionary to store the object
        shared_dict = manager.dict()
        
        # Initialize the shared object in the dictionary
        shared_dict['oldreached'] = -1
        shared_dict['numreachedstate'] = numreachedstate
        shared_dict['z3solvetime'] = z3solvetime
        #voc = transitiongraph.voc
        #transitiongraph.voc= None
        #shared_dict['transitiongraph'] = transitiongraph
        #shared_dict['transitiongraph'] = manager.TransitionGraph(transitiongraph)
        #while len(tempstate) > 0 :
        while shared_dict['numreachedstate'] - shared_dict['oldreached'] > 0:
            #nextreachedState = tempstate.copy()
            print("next states")
            print(shared_dict['numreachedstate'])
            # Create and start multiple processes
            processes = []
            for i in range(shared_dict['oldreached']+1,shared_dict['numreachedstate']+1):
                p = multiprocessing.Process(target=parallelalgo, args=(shared_dict,theory,init_struct,Nonaction,no_conc,i))
                #p = multiprocessing.Process(target=parallelalgo, args=(shared_dict,no_conc,i))
                processes.append(p)
                p.start()
            # Wait for all processes to finish
            for p in processes:
                p.join()
        #transitiongraph.voc = voc
        print("TOTAL Z3 SOLVING TIME:")
        print(shared_dict['z3solvetime'])
    return initialStates

class CustomManager(BaseManager):
    # nothing
    pass
 

def parallelalgo(shared_dict,theory=None,init_struct=None,Nonaction=None,no_conc=False,i=0,lock=None):
    #transitiongraph,numreachedstate,oldreached,z3solvetime are shared
    transitiongraph = shared_dict['transitiongraph']
    if i == shared_dict['oldreached']+1:
        shared_dict['oldreached'] = shared_dict['numreachedstate']
    Nstatei = translateToNstate(transitiongraph.states[i],theory)
    for action , extentsion in transitiongraph.aextentions.items():
        e = extentsion[0]
        t = False
        if e == [[]]:
            t = []
            if no_conc:
                ract = Nonaction[action][0]
                t = findnextStatesparallel(transitiongraph,action,None,init_struct,theory.transition_theory,Nstatei,Nonaction,lock,alg3=True,realaction=ract)
            else:
                t = findnextStatesparallel(transitiongraph,action,None,init_struct,theory.transition_theory,Nstatei,Nonaction,lock,alg3=True)
            for j in t[0]:
                trs = transitiongraph.transtions.get((i,j),[])
                trs.append(t[1])
                transitiongraph.transtions[(i,j)] = trs
                if j > shared_dict['numreachedstate']:
                    shared_dict['numreachedstate'] = j
            shared_dict['z3solvetime'] += t[2]
        else:
            q = 0
            for arg in e:
                t = []
                if no_conc:
                    ract = Nonaction[action][q]
                    t = findnextStatesparallel(transitiongraph,action,arg,init_struct,theory.transition_theory,Nstatei,Nonaction,lock,q,alg3=True,ffluentconst=ffluentConst,realaction=ract)
                else:
                    t = findnextStatesparallel(transitiongraph,action,arg,init_struct,theory.transition_theory,Nstatei,Nonaction,lock,q,alg3=True,ffluentconst=ffluentConst)
                for j in t[0]:
                    trs = transitiongraph.transtions.get((i,j),[])
                    trs.append(t[1])
                    transitiongraph.transtions[(i,j)] = trs
                    if j > shared_dict['numreachedstate']:
                        shared_dict['numreachedstate'] = j
                shared_dict['z3solvetime'] += t[2]
                q += 1

def translateToNstate(s1,theory):
    Nstate = []
    for s in s1:
        if s[2] is None:
            if s[0] == True:
                Nstate.append(AppliedSymbol(None,SymbolExpr(None,s[1],None,None),[]))
                Nstate[-1].annotate(theory.transition_theory.voc,{})
            else:
                Nstate.append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,s[1],None,None),[])))
                Nstate[-1].annotate(theory.transition_theory.voc,{})
        else:
            if s[0] == True:
                Nstate.append(AppliedSymbol(None,SymbolExpr(None,s[1],None,None),s[2]))
                Nstate[-1].annotate(theory.transition_theory.voc,{})
            else:
                Nstate.append(AUnary(None,['not'],AppliedSymbol(None,SymbolExpr(None,s[1],None,None),s[2])))
                Nstate[-1].annotate(theory.transition_theory.voc,{})
    return Nstate

def findnextStates(transitiongraph:TransiotionGraph,action:str,args,init_struct:Structure,transition_theory:TheoryBlock,Nstate:List,non_action:dict,argindex:int=0,alg3 =False):
    actionPred = None
    no_concurrency = []
    for a , act in non_action.items():
        if a == action:
            i = 0
            while i < len(act):
                if i != argindex:
                    #TO DO: COULD MAKE IT MORE EFFICIENT BY CHECKING IF IT IS ACOMPARISON AT THE BEGINING OF THE WHILE LOOP
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
    solvetime = 0
    solvetime = time.time()
    res = list(p.expand())
    solvetime = time.time() - solvetime
    transition_theory.interpretations = interp
    second_step =False
    nextstates = []
    j = 0
    #print("act pred")
    #if str(actionPred.sub_exprs) == str([1,1]):
    #    print(actionPred)
    #    print(Nstate)
    #    print(transition_theory.constraints)
    #    for d in transition_theory.definitions:
    #        for r in d.rules:
    #            print(r)
    
    #This caused error for graph_movement
    realassigns = []
    if len(Nstate) == 0 and action == "":
        realassigns = res
    else:
        realassigns = necessary_assignments(res,transitiongraph)
    
    
    #print("NEW CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL")
    #for i, xi in enumerate(res):
    for xi in realassigns:
        if xi == 'No models.':
            second_step = True
        elif type(xi) != str:
            if alg3:
                if len(Nstate) == 0 and action == "":
                    nextstates += (identifystates(xi,transitiongraph,True))
                else:
                    nextstates += (identifystates(xi,transitiongraph))
            else:
                nextstates += (matchingstates(xi,transitiongraph))
        j+=1
    #print("next states ...")
    #print(nextstates)
    if isinstance(actionPred,AComparison):
        ap = actionPred.sub_exprs[0].init_copy()
        ap.sub_exprs.append(actionPred.sub_exprs[1])
        actionPred = ap
    if second_step and j==1:
        return ([],actionPred,solvetime)
    return (list(set(nextstates)),actionPred,solvetime)


def findnextStatesparallel(transitiongraph:TransiotionGraph,action:str,args,init_struct:Structure,transition_theory:TheoryBlock,Nstate:List,non_action:dict,lock,argindex:int=0,alg3 =False,ffluentconst=[],realaction=None):
    actionPred = None
    no_concurrency = []
    if not realaction:
        for a , act in non_action.items():
            if a == action:
                i = 0
                while i < len(act):
                    if i != argindex:
                        #TO DO: COULD MAKE IT MORE EFFICIENT BY CHECKING IF IT IS ACOMPARISON AT THE BEGINING OF THE WHILE LOOP
                        no_concurrency += [act[i]]
                    else:
                        actionPred = act[i].sub_exprs[0]
                    i+=1
            else:
                no_concurrency += act 
    else:
        actionPred = realaction    
    testth = TheoryBlock(name="Transit",vocab_name=transition_theory.vocab_name,ltc = None,inv=None,
                                                     constraints=[],definitions=[],interpretations=[])
    if actionPred is None:
        testth.constraints = OrderedSet(Nstate+no_concurrency+ffluentconst)
    else:    
        testth.constraints = OrderedSet(Nstate+[actionPred]+no_concurrency+ffluentconst)
    interp = transition_theory.interpretations
    transition_theory.interpretations = {}
    p = Theory(init_struct,transition_theory,testth)
    solvetime = time.time()
    res = list(p.expand())
    solvetime = time.time() - solvetime
    transition_theory.interpretations = interp
    second_step =False
    nextstates = []
    j = 0
    realassigns = necessary_assignments(res,transitiongraph)
    #realassigns = res
    #print("NEW CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL")
    #for i, xi in enumerate(res):
    for xi in realassigns:
        if xi == 'No models.':
            second_step = True
        elif type(xi) != str:
            if alg3:
                if len(Nstate) == 0 and action == "":
                    nextstates += (identifystatesparallel(xi,transitiongraph.fextentions.keys(),transitiongraph.ffextentions.keys(),transitiongraph.states,lock,True))
                else:
                    nextstates += (identifystatesparallel(xi,transitiongraph.fextentions.keys(),transitiongraph.ffextentions.keys(),transitiongraph.states,lock))
            else:
                nextstates += (matchingstates(xi,transitiongraph))
        j+=1
    #print("next states ...")
    #print(nextstates)
    if isinstance(actionPred,AComparison):
        ap = actionPred.sub_exprs[0].init_copy()
        ap.sub_exprs.append(actionPred.sub_exprs[1])
        actionPred = ap
    if second_step and j==1:
        return ([],actionPred,solvetime)
    return (list(set(nextstates)),actionPred,solvetime)



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
    """if isinstance(actionPred,AComparison):
        ap = actionPred.sub_exprs[0].init_copy()
        ap.sub_exprs.append(actionPred.sub_exprs[1])
        actionPred = ap"""
    return actionPred



def translateLogicFormula(formula:LFormula|CTLFormula,probnumset):
    #Union[Expression,ILFormula,DLFormula,CLFormula,NLFormula,XLFormula,
    #FLFormula,GLFormula,ULFormula,WLFormula,RLFormula]
    return recTransProb(formula,probnumset)

#Remember to add the interval for number sorts in quantifiers
#check if the retured is False then pass that
def recTransProb(formula:LFormula|CTLFormula,probnumset:dict(str,List),firstexp=False):
    #print("ptob parsing")
    #print(type(formula))
    #print(formula)
    if isinstance(formula,(ILFormula,ICFormula)):
        return "(" + recTransProb(formula.expr1,probnumset) + " => " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,(DLFormula,DCFormula)):
        return "(" + recTransProb(formula.expr1,probnumset) + " or " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,(CLFormula,CCFormula)):
        return "(" + recTransProb(formula.expr1,probnumset) + " & " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,(NLFormula,NCFormula)):
        return  " not " + "(" + recTransProb(formula.expr,probnumset) + ")" 
    elif isinstance(formula,XLFormula):
        return  "X " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,FLFormula):
        return  "F " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,GLFormula):
        return  "G " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,ULFormula):
        return "(" + recTransProb(formula.expr1,probnumset) + " U " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,RLFormula):
        return "(" + recTransProb(formula.expr1,probnumset) + " R " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,WLFormula):
        return "(" + recTransProb(formula.expr1,probnumset) + " W " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,AXFormula):   
        return "AX " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,EXFormula):
        return "EX " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,AFFormula):
        return "AF " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,EFFormula):
        return "EF " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,AGFormula):
        return "AG " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,EGFormula):
        return "EG " + "(" + recTransProb(formula.expr,probnumset) +  ")"
    elif isinstance(formula,AUFormula):
        return "(A " + recTransProb(formula.expr1,probnumset) + " U " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,EUFormula):
        return "(E " + recTransProb(formula.expr1,probnumset) + " U " + recTransProb(formula.expr2,probnumset) + ")"
    elif isinstance(formula,Expression):
        res = ""
        if not firstexp:
            res += "{ "
        if isinstance(formula,AQuantification):
            if formula.q == "∀":
                res += "!("
            else:
                res += "#("
            precond ="("
            i = 0
            for q in formula.quantees:
                if i != 0:
                    precond += " & "
                qvars =[]
                i2 =0
                for q1 in q.vars:
                    j2 =0
                    for q2 in q1:
                        if i2 != 0 or j2 != 0 or i != 0:
                            res += ", "
                        res += str(q2)
                        qvars.append(str(q2))
                        j2 += 1
                    i2 += 1
                styp = "" 
                if str(q.subtype) in probnumset.keys():
                    styp = str(probnumset[str(q.subtype)][0]) + ".." + str(probnumset[str(q.subtype)][1])
                else:
                    styp = str(q.subtype)
                    if styp == "Bool":
                        styp = "BOOL"
                j = 0
                for q1 in qvars:
                    if j != 0:
                        precond += " & "
                    precond += q1 + ": " + styp
                    j += 1
                i += 1
            res += ").("
            precond += " ) "
            res += precond
            if formula.q == "∀":
                res += " => "
            else:
                res += " & "
            res += "(" + recTransProb(formula.f,probnumset,True) + ") )"
        elif isinstance(formula,AppliedSymbol):
            if len(formula.sub_exprs) > 0:
                args = "("
                j = 0
                for s in formula.sub_exprs:
                    if j != 0:
                        args += " , "
                    args += recTransProb(s,probnumset,True)
                    j += 1
                args += ")"
                #res += str(formula.symbol) + " = " + str(formula.symbol) + " \/ " + "{" + args + "}"
                res += args + " : " + str(formula.symbol)
            else:
                 res += str(formula.symbol) + " = " + "TRUE"
        elif isinstance(formula,SetName):
            #TO DO: dealing with concepts???
            if formula.name == "Bool":
                res += "BOOL"
            elif formula.name == "true":
                res += "TRUE"
            elif formula.name == "false":
                res += "FALSE"
            else:
                res += str(formula.name)
        elif isinstance(formula,AIfExpr):
            res += "IF " + recTransProb(formula.if_f,probnumset,True) + " THEN " + \
                recTransProb(formula.then_f,probnumset,True) + " ELSE " + recTransProb(formula.else_f,probnumset,True) + " END"
        elif isinstance(formula,Operator):
            sign = ""
            if isinstance(formula,ARImplication):
                sign = " => "
                res += "("
                j = len(formula.sub_exprs) -1
                while j>= 0:
                    if j != len(formula.sub_exprs) -1:
                        res += sign
                    res += recTransProb(formula.sub_exprs[j],probnumset,True)
                    j -= 1

                res += ")"
            else:
                if isinstance(formula,AImplication):
                    sign =" => "
                elif isinstance(formula,AEquivalence):
                    sign =" <=> "
                elif isinstance(formula,ADisjunction):
                    sign =" or "
                elif isinstance(formula,AConjunction):
                    sign =" & "
                elif isinstance(formula,AComparison):
                    if formula.operator[0] == "∧":
                        sign =" & "
                    elif formula.operator[0] == "∨":
                        sign = " or "   
                    elif formula.operator[0] == "⨯":
                        sign = " * "   
                    elif formula.operator[0] == "≠":
                        sign = " /= "   
                    elif formula.operator[0] == "≥":
                        sign = " >= "   
                    elif formula.operator[0] == "≤":
                        sign = " <= "    
                elif isinstance(formula,ASumMinus):
                    sign = formula.operator[0] 
                elif isinstance(formula,AMultDiv):
                    if formula.operator[0] == "⨯":
                        sign = " * "   
                        '/' | '%'
                    elif formula.operator[0] == "/":
                        sign = " / "   
                    elif formula.operator[0] == "%":
                        sign = " mod "  
                    else: 
                        sign = formula.operator[0]   
                elif isinstance(formula,APower):
                    sign =" ** "
                res += "("
                j = 0
                while j < len(formula.sub_exprs) :
                    if j != 0:
                        res += sign
                    res += recTransProb(formula.sub_exprs[j],probnumset,True)
                    j += 1
                res += ")"
        elif isinstance(formula,AUnary):
            res += "not (" + recTransProb(formula.f,probnumset,True) + " )"
        elif isinstance(formula,AAggregate):
            pass
            #TO DO: ADD AGGREGATE ??    
        elif isinstance(formula,(StartAppliedSymbol,NowAppliedSymbol,NextAppliedSymbol)):
            pass
        elif isinstance(formula,UnappliedSymbol):
            if formula.name == "true":
                res += "TRUE"
            elif formula.name == "false":
                res += "FALSE"
            else:
                res += str(formula.name)
        elif isinstance(formula,Brackets):
            res += "( " + recTransProb(formula.f,probnumset,True) + " )"
        else:
            res += str(formula)  
                    
        if not firstexp:
            res += " }"
        return res
    return ""

def checkLtlFormula(theory:TheoryBlock,struct:Structure,templog:TempLogic):
    tempdcl = [t.symbol.name for t in theory.voc.tempdcl]
    f = translateLtlToFo(templog.formula,ZERO,tempdcl,0)
    try:
        f.annotations =None
        f.annotate(theory.voc,{})
    except (IDPZ3Error) as e :
            return e
    print("tarnslated formula")
    print(f)
    thltl = TheoryBlock(name="LogicFormula",vocab_name=theory.vocab_name,ltc = None,inv=None,constraints=[],definitions=[],interpretations=[])
    thltl.constraints = [f]
    p = Theory(struct,theory,thltl)
    res = list(p.expand())
    second_step =False
    j=0
    for i, xi in enumerate(res):
        if xi == 'No models.':
            second_step = True
        j+=1
    if second_step and j==1:
        print("FALSE.....")
        return "Ltl formula is False"
    print("TRUE.....")
    return "LTL Formula is TRUE"
    
def translateLtlToFo(formula:Expression,t:Expression,tempdcl:List[str],num=0):
    if isinstance(formula,AppliedSymbol):
        if formula.symbol.name in tempdcl:
            formula.sub_exprs.append(t)
    elif isinstance(formula,UnappliedSymbol):
        return formula
    elif isinstance(formula,XLFormula):
        return translateLtlToFo(formula.expr,ASumMinus(None,"+",[t,ONE]),tempdcl)
    elif isinstance(formula,(FLFormula,GLFormula,ULFormula)):
        time = INT_SETNAME
        tn = VARIABLE("time"+str(num+1),time)
        qt = Quantee(None,[tn],time) 
        tu = UnappliedSymbol(None,tn.name)
        comp = AComparison(None,">=",[tu,t])
        if isinstance(formula,FLFormula):
            f = translateLtlToFo(formula.expr,tu,tempdcl,num+1)
            uf = AQuantification(None,None,"?",[qt],AConjunction(None,"∧",[comp,f]))
            f.code = intern(str(f))
            f.str = f.code
            return uf
        elif isinstance(formula,GLFormula):
            f = AQuantification(None,None,"forall",[qt],AConjunction(None,"∧",[comp,formula.expr]))
            return translateLtlToFo(f,tu,tempdcl,num+1)
        elif isinstance(formula,ULFormula):
            tn2 = VARIABLE("time"+str(num+2),time)
            qt2 = Quantee(None,[tn2],time) 
            tu2 = UnappliedSymbol(None,tn2.name)
            comp2 = AComparison(None,">=",[tu2,t])
            comp3 = AComparison(None,">",[tu,tu2])
            comptogether = AConjunction(None,"∧",[comp2,comp3])
            first = translateLtlToFo(formula.expr1,tu2,tempdcl,num+2)
            uquantif = AQuantification(None,None,"forall",[qt2],AImplication(None,"=>",[comptogether,first]))
            second = translateLtlToFo(formula.expr2,tu,tempdcl,num+1)
            return AQuantification(None,None,"?",[qt],AConjunction(None,["∧","∧"],[comp,uquantif,second]))
    elif isinstance(formula,WLFormula):
        equivalant = ADisjunction(None,"∨",[ULFormula(None,formula.expr1,formula.expr2),GLFormula(None,formula.expr1)])
        return equivalant
    elif isinstance(formula,RLFormula):
        equivalant = WLFormula(None,formula.expr2,AConjunction(None,"∧",[formula.expr1,formula.expr2]))
        return equivalant
    elif isinstance(formula,(ILFormula,DLFormula,CLFormula)):
        first = translateLtlToFo(formula.expr1,t,tempdcl,num)
        second = translateLtlToFo(formula.expr2,t,tempdcl,num)
        if isinstance(formula,ILFormula):
            return AImplication(None,"=>",[first,second])
        elif isinstance(formula,DLFormula):
            return ADisjunction(None,"∨",[first,second])
        elif isinstance(formula,CLFormula):
            return AConjunction(None,"∧",[first,second])
    elif isinstance(formula,NLFormula):
        first = translateLtlToFo(formula.expr,t,tempdcl,num)
        return AUnary(None,["not"],first)
    i = 0
    for f in formula.sub_exprs:
        formula.sub_exprs[i] = translateLtlToFo(f,t,tempdcl)
        formula.sub_exprs[i].code = intern(str(formula.sub_exprs[i]))
        formula.sub_exprs[i].str = formula.sub_exprs[i].code
        i+=1
    return formula
#Structure should not contain interpretation of Time
def iterative_planning(theory:TheoryBlock,endcond:TheoryBlock,structure:Structure,start=1,max=10,step=1):
    print("iterative planning....")
    Timestruct=  Structure(name="tiemstruct",vocab_name=structure.vocab_name,interpretations=[])
    for d in structure.voc.declarations:
        if isinstance(d,TypeDeclaration) and d.name == TIJD:
            d.interpretation = None
            break
    reachedAnswer =False
    while not reachedAnswer:
        if start>max:
            break
        enum = Ranges(parent=None,elements=[RangeElement(fromI=ZERO,toI=Number(number=str(start)))])
        Timestruct.interpretations[TIJD] = SymbolInterpretation(None,UnappliedSymbol(None,TIJD),":=",enum,None)
        Timestruct.interpretations[TIJD].annotate(structure.voc,{})
        p = Theory(theory,endcond,structure,Timestruct)
        res = list(p.expand(timeout_seconds=20))
        second_step =False
        j=0
        for i, xi in enumerate(res):
            if xi == 'No models.':
                second_step = True
            j+=1
        if not second_step:
            for r in res:
                print(r)
            return res
        start += step
        print(start)

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
    print("models  ........")
    #print(ms)
    if isinstance(ms[-1], str):
        ms, last = ms[:-1], ms[-1]
    else:
        last = ""
    if sort:
        ms = sorted([str(m) for m in ms])
    out = ""
    for i, m in enumerate(ms):
        out = out + (f"{NEWL}Model {i+1}{NEWL}==========\n{m}\n")
    print(out)
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
                if type(s) == tuple:
                    if isinstance(s[0],Structure):
                        out.append(f"{NEWL}Model {i+1}{NEWL}==========")
                        for interp in s[0].interpretations.values():
                            out.append(str(interp))
                elif isinstance(s,Structure):
                    out.append(f"{NEWL}Model {i+1}{NEWL}==========")
                    for interp in s.interpretations.values():
                        out.append(str(interp))
                else:
                    out.append(str(s))
                    i -= 1
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
    mylocals['iterative_planning'] = iterative_planning

    try:
        exec(main, mybuiltins, mylocals)
    except (SyntaxError, AttributeError) as e:
        raise IDPZ3Error(f'Error in procedure, {e}')
    if out:
        return linesep.join(out) + linesep

IDP.execute = execute





Done = True
