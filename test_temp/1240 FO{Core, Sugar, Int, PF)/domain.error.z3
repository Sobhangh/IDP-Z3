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
  File "idp_engine/Interpret.py", line ??, in interpret
    problem.interpretations[self.name].interpret(problem)
  File "idp_engine/Interpret.py", line ??, in interpret
    self.check(not condition.same_as(FALSE),
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(msg, self)
idp_engine.utils.IDPZ3Error: Error: line 11 - colStart 2 - colEnd 2 => Alice is not in the domain of spouse

