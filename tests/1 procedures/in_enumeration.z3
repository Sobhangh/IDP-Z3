Traceback (most recent call last):
  File "test.py", line 61, in generateZ3
    idp = idpparser.model_from_str(theory)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.8/lib/python3.8/site-packages/textx/metamodel.py", line 615, in model_from_str
    model = self._parser_blueprint.clone().get_model_from_str(
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.8/lib/python3.8/site-packages/textx/model.py", line 341, in get_model_from_str
    model = parse_tree_to_objgraph(
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.8/lib/python3.8/site-packages/textx/model.py", line 837, in parse_tree_to_objgraph
    _end_model_construction(m)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.8/lib/python3.8/site-packages/textx/model.py", line 928, in _end_model_construction
    obj.__init__(**attrs)
  File "IDP-Z3/idp_solver/Parse.py", line 85, in __init__
    t.annotate(self)
  File "IDP-Z3/idp_solver/Annotate.py", line 117, in annotate
    self.constraints = OrderedSet([e.annotate(self.voc, {})
  File "IDP-Z3/idp_solver/Annotate.py", line 117, in <listcomp>
    self.constraints = OrderedSet([e.annotate(self.voc, {})
  File "IDP-Z3/idp_solver/Expression.py", line 220, in annotate
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
  File "IDP-Z3/idp_solver/Expression.py", line 220, in <listcomp>
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
  File "IDP-Z3/idp_solver/Expression.py", line 768, in annotate
    self.in_enumeration.annotate(voc)
  File "IDP-Z3/idp_solver/Parse.py", line 739, in annotate
    t.annotate(voc)
  File "IDP-Z3/idp_solver/Parse.py", line 795, in annotate
    self.args = [arg.annotate(voc, {}) for arg in self.args]
  File "IDP-Z3/idp_solver/Parse.py", line 795, in <listcomp>
    self.args = [arg.annotate(voc, {}) for arg in self.args]
  File "IDP-Z3/idp_solver/Expression.py", line 877, in annotate
    self.check(False, f"Symbol not in vocabulary: {self}")
  File "IDP-Z3/idp_solver/Expression.py", line 59, in check
    raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")
idp_solver.utils.IDPZ3Error: Error on line 8, col 24: Symbol not in vocabulary: red

