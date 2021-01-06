Traceback (most recent call last):
  File "test.py", line 61, in generateZ3
    idp = idpparser.model_from_str(theory)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.7/lib/python3.7/site-packages/textx/metamodel.py", line 617, in model_from_str
    pre_ref_resolution_callback=kwargs_callback)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.7/lib/python3.7/site-packages/textx/model.py", line 344, in get_model_from_str
    is_main_model=is_main_model, encoding=encoding)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.7/lib/python3.7/site-packages/textx/model.py", line 837, in parse_tree_to_objgraph
    _end_model_construction(m)
  File "/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.7/lib/python3.7/site-packages/textx/model.py", line 928, in _end_model_construction
    obj.__init__(**attrs)
  File "IDP-Z3/idp_solver/Parse.py", line 88, in __init__
    t.annotate(self)
  File "IDP-Z3/idp_solver/Parse.py", line 510, in annotate
    for e in self.constraints])
  File "IDP-Z3/idp_solver/Parse.py", line 510, in <listcomp>
    for e in self.constraints])
  File "IDP-Z3/idp_solver/Substitute.py", line 210, in interpret
    f"Can't use 'is enumerated' with predicate {self.name}."
AssertionError: Can't use 'is enumerated' with predicate is_color.

