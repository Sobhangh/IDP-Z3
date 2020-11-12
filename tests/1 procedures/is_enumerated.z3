T, S

Model 1
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->red}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->A}

Model 2
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->red}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
T, S2
No models.
T2, S

Model 1
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->red}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->A}

Model 2
==========
Color:={->blue}
opposite:={(red)->green; (blue)->blue; (green)->red}
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
  File "test.py", line 56, in generateZ3
    idp.execute()
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Run.py", line 355, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 10, in <module>
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Run.py", line 336, in myprint
    for i, xi in enumerate(x):
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Run.py", line 327, in model_expand
    yield from problem.expand(max=max, complete=complete, extended=extended)
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Run.py", line 153, in expand
    z3_formula = self.formula().translate()
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Run.py", line 110, in formula
    self._interpret()
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Run.py", line 100, in _interpret
    c.interpret(self)
  File "/home/pcarbonn/Documents/repos/IDP-Z3/Idp/Substitute.py", line 222, in interpret
    simpler = theory.interpretations[self.name].is_enumerated(self.sub_exprs)
KeyError: 'is_color'

