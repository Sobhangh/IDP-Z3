T3, S
Traceback (most recent call last):
  File "IDP-Z3/test.py", line 66, in generateZ3
    idp.execute()
  File "IDP-Z3/idp_engine/Run.py", line 129, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 2, in <module>
  File "IDP-Z3/idp_engine/Run.py", line 107, in pretty_print
    for i, xi in enumerate(x):
  File "IDP-Z3/idp_engine/Run.py", line 47, in model_expand
    problem = Problem.make(theories, structures, extended=extended)
  File "IDP-Z3/idp_engine/Problem.py", line 102, in make
    self = cls(* [theories] + structures, extended=extended)
  File "IDP-Z3/idp_engine/Problem.py", line 88, in __init__
    self.add(*blocks)
  File "IDP-Z3/idp_engine/Problem.py", line 179, in add
    c.interpret(self)
  File "IDP-Z3/idp_engine/Interpret.py", line 386, in interpret
    assert self.decl.type != BOOL, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

