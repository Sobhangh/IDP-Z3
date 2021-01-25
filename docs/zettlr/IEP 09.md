# IEP 09 Unicode

Todo::
- [x] '<-' can be encoded as ←
* [x]  bool, int, real can be entered 𝔹, ℤ, ℚ (and ℕ, ℝ) (Rationale: mathematical notation)
- [ ] `in` can be encoded ∈
- [ ] `Symbols can be encoded as Σ
- [ ] accented characters in symbols and constructors

## Problem with accented characters in predicate name
Error raised:  'utf-8' codec can't decode byte 0xe9 in position 2: invalid continuation byte
error raised in:
/home/pcarbonn/.cache/pypoetry/virtualenvs/idp-solver-jObFWZdg-py3.8/lib/python3.8/site-packages/z3/z3core.py

[on stackoverflow](https://stackoverflow.com/questions/65768674/use-of-non-ascii-strings-in-defining-z3-variablels-and-types/65812448?noredirect=1#comment116376199_65812448), on [github of Z3](https://github.com/Z3Prover/z3/issues/4956)

New code in z3core.py:

`if sys.version < '3':
  def _str_to_bytes(s):
    return s
  def _to_pystr(s):
     return s
else:
  def _str_to_bytes(s):
    if isinstance(s, str):
        enc = sys.stdout.encoding
        return s.encode(enc if enc != None else 'latin-1')
    else:
      return s

  def _to_pystr(s):
     if s != None:
        enc = sys.stdout.encoding
        return s.decode(enc if enc != None else 'latin-1')
     else:
        return ""
        `