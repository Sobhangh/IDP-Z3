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
    self.warnings = flatten(t.annotate_block(self)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/utils.py", line ??, in flatten
    for sublist in a:
  File "idp_engine/Parse.py", line ??, in <genexpr>
    self.warnings = flatten(t.annotate_block(self)
                            ^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in annotate_block
    c1 = c.annotate(self.voc, {})
         ^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in annotate
    out = Operator.annotate(self, voc, q_vars)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in annotate
    self = Expression.annotate(self, voc, q_vars)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in annotate
    return self.set_variables()
           ^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in set_variables
    out = Operator.set_variables(self)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in set_variables
    self.type = base_type(self.sub_exprs)
                ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in base_type
    e.check(False, f"Invalid type {b.name} (expecting {base.name})")
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(msg, self)
idp_engine.utils.IDPZ3Error: Error: line 8 - colStart 21 - colEnd 25 => Invalid type Color (expecting LivingBeing)

