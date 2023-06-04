Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Theory.py", line ??, in __init__
    self.add(*theories)
  File "idp_engine/Theory.py", line ??, in add
    decl.interpret(self)
  File "idp_engine/Expression.py", line ??, in inner_function
    raise e
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Interpret.py", line ??, in interpret
    problem.interpretations[self.name].interpret(problem)
  File "idp_engine/Expression.py", line ??, in inner_function
    raise e
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Interpret.py", line ??, in interpret
    self.check(not condition.same_as(FALSE),
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")
idp_engine.utils.IDPZ3Error: Error on line ??, col 2: Alice is not in the domain of spouse

