Formula: 
And(p(a),
    col(a),
    p(a),
    p(c),
    col(c),
    p(c),
    col(c),
    Or(Not(col(c)), p(c)),
    Or(col(c), p(c)),
    Or(Not(col(c)), p(c)),
    Or(c == a, c == b))
WDF: 
col(a)
true
col(c())
true
true
true
col(c()) ∨ col(c())
true
true
