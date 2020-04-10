Subtences
=
20200402140335

question: how to determine subtences ?

Special cases:
* Perimeter = sum{…}  : aggregate could have quantified variables !

Principles:
* for constraints: determined after annotations, but before quantifier expansion
    * based on presence of quantified variables
    * an expression may contain several (nested) subtences
* for definitions: after instantiate (because are part of a justification, for relevance) 
    * use expr.instantiate, not [[substitute]], to avoid brackets and update expr.code
* .substitute() never changes the subtence status, nor the list of fresh_vars
* .make() expression is a subtence if it replaces a subtence (usually it does not)
    * passed as a parameter, default = false

DONE:
improve determination of subtences (expr.fresh_vars, .mark_subtences(), .instantiate())

instantiations of definitions: use expr.instantiate() instead of substitute():
* does not create bracket, does not simplify
* update expr.code
* calls mark_subtences()

TODO:
subtences for nested applied symbols: 
* desirable: itself + all compatible instances
* unnest locally and expand quantifier, using substitue (not instantiate)

#Analysis