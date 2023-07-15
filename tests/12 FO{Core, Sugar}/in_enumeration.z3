No more consequences.
And(Or(Not(p), Or(Color == blue, Color == red)),
    Or(Color == red, Color == blue, Color == green))
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
    different.append(q.translate(self) != a.value.translate(self))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "z3/z3.py", line ??, in __ne__
    a, b = _coerce_exprs(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "z3/z3.py", line ??, in _coerce_exprs
    s = _coerce_expr_merge(s, b)
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "z3/z3.py", line ??, in _coerce_expr_merge
    _z3_assert(False, "sort mismatch")
  File "z3/z3.py", line ??, in _z3_assert
    raise Z3Exception(msg)
z3.z3types.Z3Exception: sort mismatch

