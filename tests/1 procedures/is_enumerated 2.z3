Traceback (most recent call last):
  File "test.py", line 61, in generateZ3
    idp = IDP.parse(theory)
  File "IDP-Z3/idp_engine/Parse.py", line 108, in parse
    return idpparser.model_from_str(file_or_string)
  File "site-packages/textx/metamodel.py", line 615, in model_from_str
    model = self._parser_blueprint.clone().get_model_from_str(
  File "site-packages/textx/model.py", line 341, in get_model_from_str
    model = parse_tree_to_objgraph(
  File "site-packages/textx/model.py", line 837, in parse_tree_to_objgraph
    _end_model_construction(m)
  File "site-packages/textx/model.py", line 928, in _end_model_construction
    obj.__init__(**attrs)
  File "IDP-Z3/idp_engine/Parse.py", line 93, in __init__
    t.annotate(self)
  File "IDP-Z3/idp_engine/Annotate.py", line 148, in annotate
    self.constraints = OrderedSet([e.interpret(self) #TODO why is this needed ?
  File "IDP-Z3/idp_engine/Annotate.py", line 148, in <listcomp>
    self.constraints = OrderedSet([e.interpret(self) #TODO why is this needed ?
  File "IDP-Z3/idp_engine/Interpret.py", line 378, in interpret
    assert self.decl.type != BOOL, \
AssertionError: Can't use 'is enumerated' with predicate is_color.

