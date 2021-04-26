Traceback (most recent call last):
  File "test.py", line 65, in generateZ3
    state = State(idp)
  File "IDP-Z3/idp_server/State.py", line 76, in __init__
    self._interpret()
  File "IDP-Z3/idp_engine/Problem.py", line 170, in _interpret
    self.def_constraints[decl] = rule.interpret(self).whole_domain
  File "IDP-Z3/idp_engine/Interpret.py", line 128, in interpret
    self.whole_domain = expr.interpret(theory)
  File "IDP-Z3/idp_engine/Interpret.py", line 341, in interpret
    new_f = f.instantiate(vars, val, problem)
  File "IDP-Z3/idp_engine/Interpret.py", line 255, in instantiate
    return out.instantiate1(e0, e1, problem)
  File "IDP-Z3/idp_engine/Interpret.py", line 266, in instantiate1
    out = self.update_exprs(e.instantiate(e0, e1, problem)
  File "IDP-Z3/idp_engine/Simplify.py", line 162, in update_exprs
    exprs = list(new_exprs)
  File "IDP-Z3/idp_engine/Interpret.py", line 266, in <genexpr>
    out = self.update_exprs(e.instantiate(e0, e1, problem)
  File "IDP-Z3/idp_engine/Interpret.py", line 255, in instantiate
    return out.instantiate1(e0, e1, problem)
  File "IDP-Z3/idp_engine/Interpret.py", line 458, in instantiate1
    self.check(len(out.sub_exprs) == len(out.symbol.decl.sorts),
  File "IDP-Z3/idp_engine/Expression.py", line 60, in check
    raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")
idp_engine.utils.IDPZ3Error: Error on line 11, col 35: Incorrect arity for $($important!0$)

