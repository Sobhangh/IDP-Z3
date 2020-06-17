–-
title: Substitute
tags: #documentation
Date: Substitute
–-

## Call graph
(Partial) Call graph for Idp.Substitute, Idp.Simplify modules:

```mermaid
graph TD
    Annotate --> expand_quantifiers;
    Annotate --> interpret;
    Annotate --> instantiate_definition;
    Annotate --> rename_args;
    
    Case --> full_propagate;
    full_propagate --> propagate;
    propagate --> substitute;
    substitute --> update_exprs;
    
    instantiate_definition --> instantiate;
    expand_quantifiers --> instantiate;
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

