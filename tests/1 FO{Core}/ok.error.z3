ok
2
Traceback (most recent call last):
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
NameError: name 'u' is not defined

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    raise IDPZ3Error(f'Error in procedure, {e}')
idp_engine.utils.IDPZ3Error: Error in procedure, name 'u' is not defined

