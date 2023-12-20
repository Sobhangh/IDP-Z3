Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    prints = idp.execute(capture_print = True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Theory.py", line ??, in explain
    raise IDPZ3Error("Theory is satisfiable: nothing to explain.")
idp_engine.utils.IDPZ3Error: Theory is satisfiable: nothing to explain.

