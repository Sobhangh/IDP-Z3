Formula: 
And(Q(a),
    p(a),
    f(a, a) == a,
    Or(Not(And(Q(a), p(a))), f(a, a) == a),
    Or(Not(And(Q(b), p(b))), f(b, b) == b),
    Or(Not(Q(a)),
       And(Or(Not(p(a)), f(a, a) == a),
           Or(Not(p(b)), f(a, b) == a))),
    Or(Not(Q(b)),
       And(Or(Not(p(a)), f(b, a) == b),
           Or(Not(p(b)), f(b, b) == b))),
    Or(And(Q(a),
           And(Or(Not(p(a)), f(a, a) == a),
               Or(Not(p(b)), f(a, b) == a))),
       And(Q(b),
           And(Or(Not(p(a)), f(b, a) == b),
               Or(Not(p(b)), f(b, b) == b)))),
    Or(Not(And(Q(a), p(a))), Or(f(a, a) == a, f(a, a) == b)),
    Or(Not(And(Q(a), p(b))), Or(f(a, b) == a, f(a, b) == b)),
    Or(Not(And(Q(b), p(a))), Or(f(b, a) == a, f(b, a) == b)),
    Or(Not(And(Q(b), p(b))), Or(f(b, b) == a, f(b, b) == b)))
WDF: 
true
true
true
true
