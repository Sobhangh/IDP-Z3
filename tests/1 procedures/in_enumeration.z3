No more consequences.
(p ⇒ Color in {red, blue}) ∧ (Color = red ∨ Color = blue ∨ Color = green) ∧ true
Traceback (most recent call last):
  File "test.py", line 63, in generateZ3
    idp.execute()
  File "IDP-Z3/idp_solver/Run.py", line 122, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 3, in <module>
  File "IDP-Z3/idp_solver/Run.py", line 101, in myprint
    for i, xi in enumerate(x):
  File "IDP-Z3/idp_solver/Run.py", line 49, in model_expand
    ms = [str(m) for m in problem.expand(max=max, complete=complete, extended=extended)]
  File "IDP-Z3/idp_solver/Run.py", line 49, in <listcomp>
    ms = [str(m) for m in problem.expand(max=max, complete=complete, extended=extended)]
  File "IDP-Z3/idp_solver/Problem.py", line 254, in expand
    ass = self._from_model(solver, todo, complete, extended)
  File "IDP-Z3/idp_solver/Problem.py", line 236, in _from_model
    val = str_to_IDP(q, str(val1))
  File "IDP-Z3/idp_solver/Parse.py", line 61, in str_to_IDP
    out = atom.decl.out.decl.map[val_string]
KeyError: 'True'

