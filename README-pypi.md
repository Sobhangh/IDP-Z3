idp-engine is a reasoning engine for knowledge represented using the FO(.) language.
FO(.) (aka FO-dot) is First Order logic, with various extensions to make it more expressive:  types, equality, arithmetic, inductive definitions, aggregates, and intensional objects.
The idp-engine uses the Z3 SMT solver as a back-end.

It is developed by the Knowledge Representation group at KU Leuven in Leuven, Belgium, and made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).

See more information at [www.IDP-Z3.be](https://www.IDP-Z3.be).


# Installation

``idp_engine`` can be installed from [pypi.org](https://pypi.org/), e.g. using [pip](https://pip.pypa.io/en/stable/user_guide/):

```
   pip install idp_engine
```

# Get started

The following code illustrates how to run inferences on a knowledge base.

```
    from idp_engine import IDP, model_expand
    kb = IDP.parse("path/to/file.idp")
    T, S = kb.get_blocks("T, S")
    for model in model_expand(T,S):
        print(model)
```

For more information, please read [the documentation](http://docs.idp-z3.be/en/latest/).

# Contribute

Contributions are welcome!  The repository is [on GitLab](https://gitlab.com/krr/IDP-Z3).