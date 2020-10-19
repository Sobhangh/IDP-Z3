–-
title: Counterfactuals and null values
tags: 
   ID: 20201017102913
–-

Status: draft

Goal: allow reasoning about 1) hypothetical alternative to the state of affairs; 2) total functions with unknown values.

This IEP does not address partial functions, i.e., functions without values for some of its arguments (e.g., `1/0`).

# Counterfactuals

Every definition has a set of arguments (as specified in the vocabulary) and parameters (other constants and functions appearing in the body).  
A definition is applied by giving it arguments (e.g. `f(x)`); its parameters are supplied by the model, i.e., from the state of affairs.

Sometimes, we want to apply the definition for another state of affairs than the one we are modelling.  
We propose to denote this as `f(x|y=c)`, where y is a parameter of the definition and c an expression evaluated in the current state of affair.
This expression is evaluated by constructing a "shadow" definition where every occurrence of `y` is replaced by `c`.  If `f` refers to other definitions, they also need to be have a shadow definition.

# Null values

The enumeration of a function may be partial, without a default value specified in a `else` part.  In that case, the function may take any value.
`f(x)=null` is equivalent to `f(x)≠f(x|)`, where `f(x|)` is a shadow definition with the same parameters.


