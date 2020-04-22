–-
title: Substitute
tags: #documentation
   ID: Substitute
–-

## Call graph
(Partial) Call graph for Expression.substitute():

```mermaid
graph TD
    expand_quantifiers --> make;
    Annotate --> expand_quantifiers;
    Annotate --> interpret;
    Annotate --> instantiate_definition;
    Annotate --> rename_args;
    
    Case --> full_propagate;
    full_propagate --> propagate;
    propagate --> substitute;
    substitute --> update_exprs;
    
    expand_quantifiers --> instantiate;
    expand_quantifiers --> replace_by;
    interpret --> update_exprs;
    expand_quantifiers --> update_exprs;
    substitute --> replace_by;
    interpret --> replace_by;

    update_exprs --> replace_by;
    update_exprs --> _change;
    update_exprs -.-> make;
    make --> simplify1;
    Annotate --> annotate1;
    make --> annotate1;
    
    expand_quantifiers --> _change;

    instantiate_definition --> instantiate;
    instantiate --> _change;
		    rename_args --> instantiate;
    instantiate_definition --> interpret;
    Annotate --> make;
    instantiate_definition --> make;
    instantiate --> update_exprs;
    simplify1 --> update_exprs;

```

+ substitute → \_change


Possible performance improvement of substitute(), but is missing some substitutions !
```py
if todo is  not  None: \# not for expand_quantifiers, interpret
    if  all(e not  in  self.\_unknown\_symbols for e in e0.unknown_symbols()):
				        return  self
```

