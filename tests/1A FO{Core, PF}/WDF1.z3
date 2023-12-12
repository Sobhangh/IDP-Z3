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
    pp(c),
    p(c),
    p(c),
    col(c),
    p(c),
    Or(Not(col(c)), p(c)),
    Or(And(And(col(a), p(a)), a == c),
       And(And(col(b), p(b)), b == c)),
    2 == If(p(a), 1, 0) + If(p(b), 1, 0),
    2 ==
    If(And(col(a), p(a)), 1, 0) +
    If(And(col(b), p(b)), 1, 0),
    2 == __min(lambda x ∈ color : i(x) if col(x) ∧ p(x)),
    2 == __min(lambda x ∈ color : i(x) if p(x)),
    Or(And(col(a), 0 < 4/i(a)), And(col(b), 0 < 4/i(b))),
    Or(And(col(a), And(Not(0 == i(a)), 0 < 4/i(a))),
       And(col(b), And(Not(0 == i(b)), 0 < 4/i(b)))),
    d,
    q,
    d,
    Or(c == a, c == b),
    p(a),
    p(a),
    p(c),
    p(c),
    p(b),
    p(b),
    Or(And(And(col(a), p(a)),
           __min(lambda x ∈ color : i(x) if col(x) ∧ p(x)) ==
           i(a)),
       And(And(col(b), p(b)),
           __min(lambda x ∈ color : i(x) if col(x) ∧ p(x)) ==
           i(b))),
    Or(Not(And(col(a), p(a))),
       __min(lambda x ∈ color : i(x) if col(x) ∧ p(x)) <=
       i(a)),
    Or(Not(And(col(b), p(b))),
       __min(lambda x ∈ color : i(x) if col(x) ∧ p(x)) <=
       i(b)),
    Or(And(p(a),
           __min(lambda x ∈ color : i(x) if p(x)) == i(a)),
       And(p(b),
           __min(lambda x ∈ color : i(x) if p(x)) == i(b))),
    Or(Not(p(a)),
       __min(lambda x ∈ color : i(x) if p(x)) <= i(a)),
    Or(Not(p(b)),
       __min(lambda x ∈ color : i(x) if p(x)) <= i(b)),
    And(Or(Not(col(a)), p(a)), Or(Not(col(b)), p(b))),
    And(Or(Not(col(a)), p(a)), Or(Not(col(b)), p(b))))
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
col(c()) ∧ p(c())
col(c())
∀ x ∈ Concept[->color]: col($(x)())
true
true
true
∀ x ∈ color: col(x)
true
true
∀ x ∈ color: col(x) ∧ (¬(p(x)) ∨ col(x))
∀ x ∈ col: ¬(i(x) = 0)
true
q()
true
true
∀ x ∈ color: col(x)
