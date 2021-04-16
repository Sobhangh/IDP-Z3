T3, S
Traceback (most recent call last):
  File "test.py", line 63, in generateZ3
    idp.execute()
  File "IDP-Z3/idp_engine/Run.py", line 122, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 2, in <module>
  File "IDP-Z3/idp_engine/Run.py", line 101, in myprint
    for i, xi in enumerate(x):
  File "IDP-Z3/idp_engine/Run.py", line 49, in model_expand
    ms = [str(m) for m in problem.expand(max=max, complete=complete, extended=extended)]
  File "IDP-Z3/idp_engine/Run.py", line 49, in <listcomp>
    ms = [str(m) for m in problem.expand(max=max, complete=complete, extended=extended)]
  File "IDP-Z3/idp_engine/Problem.py", line 244, in expand
    z3_formula = self.formula().translate()
  File "IDP-Z3/idp_engine/Problem.py", line 199, in formula
    self._interpret()
  File "IDP-Z3/idp_engine/Problem.py", line 185, in _interpret
    c.interpret(self)
  File "IDP-Z3/idp_engine/Interpret.py", line 400, in interpret
    assert self.decl.type != BOOL, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

