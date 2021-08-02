Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Run.py", line ??, in pretty_print
    for i, xi in enumerate(x):
  File "idp_engine/Run.py", line ??, in model_expand
    yield from problem.expand(max=max, complete=complete)
  File "idp_engine/Problem.py", line ??, in expand
    ass = self._from_model(solver, todo, complete)
  File "idp_engine/Problem.py", line ??, in _from_model
    val = str_to_IDP(q, str(val1))
  File "idp_engine/Parse.py", line ??, in str_to_IDP
    out = Number(number=str(eval(val_string.replace('?', ''))))
  File "<string>", line ??, in <module>
NameError: name 'pos' is not defined

