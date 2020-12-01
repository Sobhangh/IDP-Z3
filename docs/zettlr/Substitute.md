–-
title: Substitute
tags: #analysis
Date: Substitute
–-

## Call graph
(Partial) Call graph for Idp.Substitute, Idp.Simplify modules:
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
    Annotate --> expand_quantifiers;
    Annotate --> interpret;
    Annotate --> rename_args;
    
    instantiate_definition --> instantiate;
    instantiate_definition --> expand_quantifiers;
    expand_quantifiers --> instantiate;
    interpret --> instantiate_definition
    interpret --> update_exprs;
    expand_quantifiers --> update_exprs;
    
    
    instantiate_definition --> make;
    update_exprs --> _change;
    update_exprs -.-> make;
    expand_quantifiers --> make;
    make --> simplify1;
    Annotate --> annotate1;
    make --> annotate1;
    
    expand_quantifiers --> _change;

    instantiate --> _change;
		    rename_args --> instantiate;
    instantiate_definition --> interpret;
    instantiate_definition --> expand_quantifiers
    Annotate --> make;
    simplify1 --> update_exprs;
    instantiate --> update_exprs;

```

+ substitute → \_change


Possible performance improvement of substitute(), but is missing some substitutions !
```py
if todo is  not  None: \# not for expand_quantifiers, interpret
    if  all(e not  in  self.\_unknown\_symbols for e in e0.unknown_symbols()):
				        return  self
```

