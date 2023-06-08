Traceback (most recent call last):
  File "idp_engine/Idp_to_Z3.py", line ??, in translate1
    return (self.decl.translate(problem))(arg)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "z3/z3.py", line ??, in __call__
    tmp = self.domain(i).cast(args[i])
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "z3/z3.py", line ??, in cast
    _z3_assert(self.eq(val.sort()), "Sort mismatch")
  File "z3/z3.py", line ??, in _z3_assert
    raise Z3Exception(msg)
z3.z3types.Z3Exception: Sort mismatch

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
    ms = list(problem.expand(max=max, timeout_seconds=timeout_seconds, complete=complete))
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Theory.py", line ??, in expand
    solver = self.solver
             ^^^^^^^^^^^
  File "idp_engine/Theory.py", line ??, in solver
    if self.constraintz():
       ^^^^^^^^^^^^^^^^^^
  File "idp_engine/Theory.py", line ??, in constraintz
    collect_constraints(e.translate(self), self._constraintz)
                        ^^^^^^^^^^^^^^^^^
  File "idp_engine/Expression.py", line ??, in inner_function
    raise e
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Idp_to_Z3.py", line ??, in translate
    out = self.translate1(problem, vars)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Expression.py", line ??, in inner_function
    raise e
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Idp_to_Z3.py", line ??, in translate1
    x = self.sub_exprs[i-1].translate(problem, vars)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Expression.py", line ??, in inner_function
    raise e
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Idp_to_Z3.py", line ??, in translate
    out = self.translate1(problem, vars)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Expression.py", line ??, in inner_function
    raise e
  File "idp_engine/Expression.py", line ??, in inner_function
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Idp_to_Z3.py", line ??, in translate1
    self.check(False, msg)
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")
idp_engine.utils.IDPZ3Error: Error on line ??, col 5: Incorrect symbol application: spouseOf(red)

