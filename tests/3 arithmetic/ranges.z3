Traceback (most recent call last):
  File "idp_engine/Expression.py", line ??, in check
    location = get_location(self)
  File "textx/model.py", line ??, in get_location
    line, col = the_model._tx_parser.pos_to_linecol(
AttributeError: 'SymbolInterpretation' object has no attribute '_tx_parser'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp = IDP.from_str(theory)
  File "idp_engine/Parse.py", line ??, in from_str
    out = idpparser.model_from_str(code)
  File "textx/metamodel.py", line ??, in model_from_str
    model = self._parser_blueprint.clone().get_model_from_str(
  File "textx/model.py", line ??, in get_model_from_str
    model = parse_tree_to_objgraph(
  File "textx/model.py", line ??, in parse_tree_to_objgraph
    _end_model_construction(m)
  File "textx/model.py", line ??, in _end_model_construction
    obj.__init__(**attrs)
  File "idp_engine/Parse.py", line ??, in __init__
    self.check(False, f"Can't have a range over real: {x.fromI}..{x.toI}")
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(f"{msg}")
idp_engine.utils.IDPZ3Error: Can't have a range over real: 0.2..0.3

