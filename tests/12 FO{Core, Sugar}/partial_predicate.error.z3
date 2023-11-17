Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp = IDP.from_str(theory)
          ^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Parse.py", line ??, in from_str
    out = idpparser.model_from_str(code)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "textx/metamodel.py", line ??, in model_from_str
    model = self._parser_blueprint.clone().get_model_from_str(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "textx/model.py", line ??, in get_model_from_str
    model = parse_tree_to_objgraph(
            ^^^^^^^^^^^^^^^^^^^^^^^
  File "textx/model.py", line ??, in parse_tree_to_objgraph
    _end_model_construction(m)
  File "textx/model.py", line ??, in _end_model_construction
    obj.__init__(**attrs)
  File "idp_engine/Parse.py", line ??, in __init__
    struct.annotate_block(self)
  File "idp_engine/Annotate.py", line ??, in annotate_block
    i.annotate(self.voc, {})
  File "idp_engine/Annotate.py", line ??, in annotate
    self.check(not(self.symbol.decl.out.decl.base_decl == BOOLT
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(msg, self)
idp_engine.utils.IDPZ3Error: Error: line 12 - colStart 5 - colEnd 5 => Can't use function enumeration for predicates 'c' (yet)

