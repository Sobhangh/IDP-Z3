–-
title: Substitute
tags: #analysis
Date: Substitute
–-

## Call graph
(Partial) Call graph for idp_solver.Substitute, idp_solver.Simplify modules:
The following diagram is a simplification of the full call tree, focusing on the transformations of the AST.

```mermaid
graph TD
    IDP-Z3 --> idpparser
    IDP-Z3 --> execute

    execute -.-> symbolic_propagate;
    symbolic_propagate --> implicants;
    execute -.-> simplify;
    simplify --> substitute;
    substitute --> update_exprs;
    execute -.-> formula
    formula --> interpret

    idpparser --> Annotate
    Annotate --> interpret;
    Annotate --> rename_args;

    rename_args --> instantiate;
    instantiate_definition --> interpret;
    interpret --> instantiate;
    instantiate_definition --> instantiate;
    interpret --> instantiate_definition
    interpret --> update_exprs;

    update_exprs -.-> make;
    instantiate_definition --> make;
    update_exprs --> _change;
    interpret --> make;
    simplify1 --> update_exprs;
    make --> simplify1;
    Annotate --> annotate1;
    make --> annotate1;

    instantiate --> _change;
    interpret --> _change;

    Annotate --> make;
    instantiate --> update_exprs;

```

+ substitute → \_change


Possible performance improvement of substitute(), but is missing some substitutions !
```py
if todo is  not  None: \# not for expand_quantifiers, interpret
    if  all(e not  in  self.\_unknown\_symbols for e in e0.unknown_symbols()):
				        return  self
```

