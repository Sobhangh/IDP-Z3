Proofs
=
20200410173444

Remaining Issues:
* isa.idp= asi() should be provable without Z3, by expansion of the first rule
    * as_substitution() should return a list, not just one substitution, like expr_to_literal
    * Expression.as_substitutions(), or as_assignments ?
* isa.idp: add type constraints for more inferences
* complex.idp: why are some proved by Z3, when others are not ?
* polygon.idp : Perimeter = 10 should have a proof (stash Perimeter)

#issues