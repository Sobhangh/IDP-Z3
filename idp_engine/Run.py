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
import time
import types
from typing import Any, Iterator, List, Union, Optional
from z3 import Solver

from idp_engine.Expression import FALSE, TRUE, AUnary, AppliedSymbol, UnappliedSymbol

from .Parse import IDP, Enumeration, FunctionTuple, SymbolDeclaration, SymbolInterpretation, TemporalDeclaration, TheoryBlock, Structure, TupleIDP, Vocabulary
from .Theory import Theory
from .Assignments import Status as S, Assignments
from .utils import NEWL, IDPZ3Error, PROCESS_TIMINGS, OrderedSet

last_call = time.process_time()  # define it as global

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


def toStructure(assign,vocab_name:str,voc:Vocabulary,tempdcl:List[TemporalDeclaration]) -> Structure:
        #print("enter to structure..")
        out : dict[SymbolDeclaration, List[TupleIDP]] = {}
        outname : dict[str,SymbolDeclaration] = {}
        outall : dict[str,SymbolDeclaration] = {}
        nullary: dict[SymbolDeclaration, Any] = {}
        nullaryname : dict[str,SymbolDeclaration] = {}
        nullaryall : dict[str,SymbolDeclaration] = {}
        #print("in loop")
        for a in assign.values():
            if type(a.sentence) == AppliedSymbol:
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
        for t in tempdcl:
            for k ,v in nullary.items():
                if t.symbol.name == k.name:
                    n = nullaryname.get(k.name+'_next',None)
                    if n is None:
                        nullaryc.pop(k)
                    else:
                        vn = nullaryc.get(n,None)
                        if vn is  not None:
                            nullaryc[k] = vn
                elif k.is_next and k.name.endswith('_next'):
                    #k.is_next= False
                    #nullaryc[k] = v
                    if t.symbol.name == k.name[:-len('_next')]:
                        nullaryc.pop(k,None)
                        n = nullaryall.get(k.name[:-len('_next')],None)
                        if n is None:
                            print("Error: current state of predicate should be in the list")
                        else:
                            nullaryc[n] = v
                else:
                    #nullaryc[k] = v
                    k
            for k ,v in out.items():
                if t.symbol.name == k.name:
                    #print("remove")
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
        #voc.add_voc_to_block(s)
        return s

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
    if len(ms) >=1:
        return toStructure(ms[0],struct.init_struct.vocab_name,struct.init_struct.voc,[])
    PROCESS_TIMINGS['solve'] += time.time() - solve_start
    #return model_expand(theory.init_theory,struct.init_struct)

def progression(theory:TheoryBlock,struct):
    #print("inside progression")
    problem = None
    voc = None
    if isinstance(struct, types.GeneratorType):
        for i, xi in enumerate(struct):
            #print(xi)
            problem = Theory(theory.bistate_theory,xi)
            voc = xi.voc.idp.next_voc.get(theory.vocab_name+'_next',None)
            #print(voc)
            if voc is None:
                print("Error vocabulary is wrong")
                return
            #print(problem.assignments)
    elif isinstance(struct,List):
        for xi in struct:
            if isinstance(xi,Structure):
                problem = Theory(theory.bistate_theory,xi)
                voc = xi.voc.idp.next_voc.get(theory.vocab_name+'_next',None)
                if voc is None:
                    print("Error vocabulary is wrong")
                    return
    elif isinstance(struct,Structure):
        problem = Theory(theory.bistate_theory,struct)
        voc = struct.voc.idp.next_voc.get(theory.vocab_name+'_next',None)
        if voc is None:
            print("Error vocabulary is wrong")
            return
    PROCESS_TIMINGS['ground'] = time.time() - PROCESS_TIMINGS['ground']
    if problem is None:
        print("reciedved None")
        #problem = Theory(theory.bistate_theory)
        return
    solve_start = time.time()
    ms = list(problem.expand(max=10, timeout_seconds=10, complete=False))
    if isinstance(ms[-1], str):
        ms, last = ms[:-1], ms[-1]
    else:
        last = ""
    out: List[Structure] = []
    if len(ms) == 0:
        #yield last
        return last
    for i, m in enumerate(ms):
        s = toStructure(m,theory.bistate_theory.vocab_name,voc,theory.voc.tempdcl)
        #for i in s.interpretations.values():
            #print(i)
        out.append(s)
    #yield out 
    return out
    PROCESS_TIMINGS['solve'] += time.time() - solve_start

def isinvariant(theory:TheoryBlock,invariant:TheoryBlock,s:Structure|None=None):
    if len(invariant.constraints) > 1:
        return "Only one formula should be specified for invariant"
    if len(invariant.constraints) == 0:
        return "Please provide an invariant"
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
                    print(interp)
            elif isinstance(xi, List) and len(xi)>0 and isinstance(xi[0],Structure):
                for s in xi:
                    print(f"{NEWL}Model {i+1}{NEWL}==========")
                    for interp in s.interpretations.values():
                        print(interp)
            else:
                print(xi)
    elif isinstance(x, Theory):
        print(x.assignments)
    elif isinstance(x,List):
        i=0
        for s in x:
            if isinstance(s,Structure):
                print(f"{NEWL}Model {i+1}{NEWL}==========")
                for interp in s.interpretations.values():
                    print(interp)
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
        elif isinstance(x, Theory):
            out.append(str(x.assignments))
        else:
            out.append(str(x))

    mylocals = copy(self.vocabularies)
    mylocals.update(self.theories)
    mylocals.update(self.structures)
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

    try:
        exec(main, mybuiltins, mylocals)
    except (SyntaxError, AttributeError) as e:
        raise IDPZ3Error(f'Error in procedure, {e}')
    if out:
        return linesep.join(out) + linesep

IDP.execute = execute





Done = True
