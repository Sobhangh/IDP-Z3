T, S

Model 1
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->green}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->A}

Model 2
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->green}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
propagate
And(Color == blue,
    opposite(red) == green,
    opposite(blue) == blue,
    opposite(green) == green,
    f(A, A) == A,
    f(A, B) == A,
    f(B, A) == B,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    Or(f(B, B) == A, f(B, B) == B),
    True)
T, S2
No models.
T2, S

Model 1
==========
Color:={->green}
opposite:={(red)->green; (blue)->green; (green)->green}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->A}

Model 2
==========
Color:={->green}
opposite:={(red)->green; (blue)->green; (green)->green}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
T4, S2

Model 1
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->red}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
T3, S
Traceback (most recent call last):
  File "test.py", line 57, in generateZ3
    idp.execute()
  File "Idp/Run.py", line 77, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 12, in <module>
  File "Idp/Run.py", line 58, in myprint
    for i, xi in enumerate(x):
  File "Idp/Run.py", line 49, in model_expand
    yield from problem.expand(max=max, complete=complete, extended=extended)
  File "Idp/Problem.py", line 155, in expand
    z3_formula = self.formula().translate()
  File "Idp/Problem.py", line 113, in formula
    self._interpret()
  File "Idp/Problem.py", line 103, in _interpret
    c.interpret(self)
  File "Idp/Substitute.py", line 203, in interpret
    assert self.decl.function, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

