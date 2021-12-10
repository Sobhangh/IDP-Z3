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

Classes to execute the main block of an IDP program

"""

import time
import types
from z3 import Solver

from .Parse import IDP
from .Problem import Theory
from .Assignments import Status as S, Assignments
from .utils import NEWL

last_call = time.process_time()  # define it as global

def model_check(theories, structures=None):
    """ output: "sat", "unsat" or "unknown" """

    problem = Theory.make(theories, structures)
    z3_formula = problem.formula()

    solver = Solver(ctx=problem.ctx)
    solver.add(z3_formula)
    yield str(solver.check())


def model_expand(theories, structures=None, max=10, timeout=10, complete=False,
                 extended=False, sort=False):
    """ output: a list of Assignments, ending with a string """
    problem = Theory.make(theories, structures, extended=extended)
    ms = list(problem.expand(max=max, timeout=timeout, complete=complete))
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


def model_propagate(theories, structures=None, sort=False):
    """ output: a list of Assignment """
    problem = Theory.make(theories, structures)
    if sort:
        ms = [str(m) for m in problem._propagate(tag=S.CONSEQUENCE)]
        ms = sorted(ms[:-1]) + [ms[-1]]
        out = ""
        for i, m in enumerate(ms[:-1]):
            out = out + (f"{NEWL}Model {i+1}{NEWL}==========\n{m}\n")
        yield out + f"{ms[-1]}"
    else:
        yield from problem._propagate(tag=S.CONSEQUENCE)


def decision_table(theories, structures=None, goal_string="",
                timeout=20, max_rows=50, first_hit=True, verify=False):
    """returns a decision table for `goal_string`, given `theories` and `structures`.

    Args:
        goal_string (str, optional): the last column of the table.
        timeout (int, optional): maximum duration in seconds. Defaults to 20.
        max_rows (int, optional): maximum number of rows. Defaults to 50.
        first_hit (bool, optional): requested hit-policy. Defaults to True.
        verify (bool, optional): request verification of table completeness.  Defaults to False

    Yields:
        str: a textual representation of each rule
    """
    problem = Theory.make(theories, structures, extended=True)
    for model in problem.decision_table(goal_string, timeout, max_rows,
                                        first_hit, verify):
        row = f'{NEWL}∧ '.join(str(a) for a in model
            if a.sentence.code != goal_string)
        has_goal = model[-1].sentence.code == goal_string
        yield((f"{(f'  {row}{NEWL}') if row else ''}"
              f"⇒ {str(model[-1]) if has_goal else '?'}"))
        yield("")
    yield "end of decision table"


def pretty_print(x=""):
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


def duration(msg=""):
    """Returns the processing time since the last call to `duration()`,
    or since the begining of execution"""
    global last_call
    out = round(time.process_time() - last_call, 3)
    last_call = time.process_time()
    return f"{out} {msg}"

def execute(self):
    """ Execute the IDP program """
    global last_call
    last_call = time.process_time()
    main = str(self.procedures['main'])
    mybuiltins = {}
    mylocals = {**self.vocabularies, **self.theories, **self.structures}
    mylocals['model_check'] = model_check
    mylocals['model_expand'] = model_expand
    mylocals['model_propagate'] = model_propagate
    mylocals['decision_table'] = decision_table
    mylocals['pretty_print'] = pretty_print
    mylocals['Theory'] = Theory
    mylocals['time'] = time
    mylocals['duration'] = duration

    exec(main, mybuiltins, mylocals)

IDP.execute = execute





Done = True
