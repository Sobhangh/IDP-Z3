
Model 1
==========
p := {A->1, B->1, C->1, D->1}.


More models may be available.  Change the max argument to see them.
Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Theory.py", line ??, in explain
    assert result == unsat, ("Incorrect solver result during explain inference. "
AssertionError: Incorrect solver result during explain inference. This may be due to floating point imprecision.

