Formula: 
And(p(a),
    col(a),
    p(a),
    p(c),
    col(c),
    p(c),
    p(c),
    col(c),
    col(c),
    Or(Not(col(c)), p(c)),
    Or(col(c), p(c)),
    Or(Not(col(c)), p(c)),
    p(c),
    p(c),
    col(c),
    p(c),
    Or(Not(col(c)), p(c)),
    Or(And(And(col(a), p(a)), a == c),
       And(And(col(b), p(b)), b == c)),
    Or(c == a, c == b))
WDF: 
col(a)
true
col(c())
true
col(c())
true
true
col(c())
true
true
col(c())
∀ x ∈ Concept[->color]: col($(x)())
true
true
true
