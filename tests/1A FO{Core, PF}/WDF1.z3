Formula: 
And(p(c),
    col(c),
    p(c),
    col(c),
    Or(Not(col(c)), p(c)),
    Or(col(c), p(c)),
    Or(Not(col(c)), p(c)),
    Or(c == a, c == b))
WDF: 
col(c())
¬(col(c())) ∨ col(c())
true
¬(col(c())) ∨ col(c())
col(c()) ∨ col(c())
¬(col(c())) ∨ col(c())
