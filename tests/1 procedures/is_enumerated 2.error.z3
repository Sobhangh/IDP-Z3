T3, S
Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Run.py", line ??, in pretty_print
    for i, xi in enumerate(x):
  File "idp_engine/Run.py", line ??, in model_expand
    problem = Theory._make(theories, structures, extended=extended)
  File "idp_engine/Problem.py", line ??, in _make
    self = cls(* [theories] + structures, extended=extended)
  File "idp_engine/Problem.py", line ??, in __init__
    self.add(*blocks)
  File "idp_engine/Problem.py", line ??, in add
    c.interpret(self)
  File "idp_engine/Interpret.py", line ??, in interpret
    assert self.decl.type != BOOL, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

