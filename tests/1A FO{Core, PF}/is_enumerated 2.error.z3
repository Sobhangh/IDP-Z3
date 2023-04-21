T3, S
Traceback (most recent call last):
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
  File "idp_engine/Interpret.py", line ??, in interpret
    assert self.decl.type != BOOL, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Run.py", line ??, in pretty_print
    for i, xi in enumerate(x):
  File "idp_engine/Run.py", line ??, in model_expand
    problem = Theory(*theories, extended=extended)
  File "idp_engine/Theory.py", line ??, in __init__
    self.add(*theories)
  File "idp_engine/Theory.py", line ??, in add
    self.constraints = OrderedSet([v.interpret(self)
  File "idp_engine/Theory.py", line ??, in <listcomp>
    self.constraints = OrderedSet([v.interpret(self)
  File "idp_engine/Expression.py", line ??, in inner_function
    self.check(False, str(e))
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")
idp_engine.utils.IDPZ3Error: Error on line ??, col 5: Can't use 'is enumerated' with predicate is_color.

