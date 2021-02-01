Traceback (most recent call last):
  File "IDP-Z3/idp_solver/Idp_to_Z3.py", line 221, in translate1
    raise self.create_error(f"Incorrect number of arguments for"
  File "IDP-Z3/idp_solver/Expression.py", line 350, in create_error
    location = get_location(self)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.8/lib/python3.8/site-packages/textx/model.py", line 183, in get_location
    line, col = the_model._tx_parser.pos_to_linecol(
AttributeError: 'AppliedSymbol' object has no attribute '_tx_parser'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "test.py", line 63, in generateZ3
    idp.execute()
  File "IDP-Z3/idp_solver/Run.py", line 106, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 1, in <module>
  File "IDP-Z3/idp_solver/Run.py", line 85, in myprint
    for i, xi in enumerate(x):
  File "IDP-Z3/idp_solver/Run.py", line 37, in model_check
    z3_formula = problem.formula().translate()
  File "IDP-Z3/idp_solver/Idp_to_Z3.py", line 46, in translate
    return self.translate1()
  File "IDP-Z3/idp_solver/Idp_to_Z3.py", line 149, in translate1
    out = And([e.translate() for e in self.sub_exprs])
  File "IDP-Z3/idp_solver/Idp_to_Z3.py", line 149, in <listcomp>
    out = And([e.translate() for e in self.sub_exprs])
  File "IDP-Z3/idp_solver/Idp_to_Z3.py", line 46, in translate
    return self.translate1()
  File "IDP-Z3/idp_solver/Idp_to_Z3.py", line 236, in translate1
    raise AttributeError(e)
AttributeError: 'AppliedSymbol' object has no attribute '_tx_parser'

