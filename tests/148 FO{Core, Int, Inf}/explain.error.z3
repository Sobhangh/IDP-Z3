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
    t.annotate_block(self)
  File "idp_engine/Annotate.py", line ??, in annotate_block
    self.definitions = [e.annotate(self.voc, {}) for e in self.definitions]
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in <listcomp>
    self.definitions = [e.annotate(self.voc, {}) for e in self.definitions]
                        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "idp_engine/Annotate.py", line ??, in annotate
    self.check(len(error) == 0,
  File "idp_engine/Expression.py", line ??, in check
    raise IDPZ3Error(f"Error on line {line}, col {col}: {msg}")
idp_engine.utils.IDPZ3Error: Error on line ??, col 5: Eliminate variable ['y'] in the head of : ∀ x ∈ List1,y ∈ ℤ: len1(x)  = y← y = len1(cdr1(x)) + 1 ∧ is_cons1(x)

