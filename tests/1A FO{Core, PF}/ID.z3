Formula: 
And(Or(c == a, c == b),
    Or(Not(p(a)), col(a)),
    Or(Not(p(b)), col(b)),
    Or(Not(pp(a)), p(a)),
    Or(Not(pp(b)), p(b)),
    Or(Not(d), q),
    p(a),
    p(a),
    p(b),
    p(b),
    And(p(a), p(b)),
    And(p(a), p(b)),
    ForAll(c!0,
           And(Or(Not(And(And(col(a), p(a)), pp(a))),
                  (i(a) == c!0) == (1 == c!0)),
               Or(Not(And(And(col(b), p(b)), pp(b))),
                  (i(b) == c!0) == (1 == c!0)))),
    ForAll(c!0,
           And(Or(Not(And(And(col(a), p(a)), pp(a))),
                  (i(a) == c!0) == (1 == c!0)),
               Or(Not(And(And(col(b), p(b)), pp(b))),
                  (i(b) == c!0) == (1 == c!0)))),
    ForAll(c!1,
           And(Or(Not(And(And(col(a), p(a)), pp(a))),
                  (i(a) == c!1) == And(1 == c!1, pp(a))),
               Or(Not(And(And(col(b), p(b)), pp(b))),
                  (i(b) == c!1) == And(1 == c!1, pp(b))))))
WDF: 
true
true
∀ x ∈ col: pp(x)
true
true
