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
  File "IDP-Z3/idp_solver/Parse.py", line 88, in __init__
    t.annotate(self)
  File "IDP-Z3/idp_solver/Parse.py", line 504, in annotate
    self.constraints = OrderedSet([e.interpret(self)
  File "IDP-Z3/idp_solver/Parse.py", line 504, in <listcomp>
    self.constraints = OrderedSet([e.interpret(self)
  File "IDP-Z3/idp_solver/Substitute.py", line 212, in interpret
    assert self.decl.function, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

