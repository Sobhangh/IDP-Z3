Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    prints = idp.execute(capture_print = True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Run.py", line ??, in pretty_print
    for i, xi in enumerate(x):
  File "idp_engine/Run.py", line ??, in model_expand
    problem = Theory(*theories, extended=extended)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Theory.py", line ??, in __init__
    self.add(*theories)
  File "idp_engine/Theory.py", line ??, in add
    decl.interpret(self)
  File "idp_engine/Interpret.py", line ??, in interpret
    problem.interpretations[self.name].interpret(problem)
  File "idp_engine/Interpret.py", line ??, in interpret
    self.check(not condition.same_as(FALSE),
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(msg, self)
idp_engine.utils.IDPZ3Error: Error: line 11 - colStart 5 - colEnd 5 => Belgium is not in the domain of p

