And(p(a),
    Or(next(a) == a, next(a) == b),
    Or(next(b) == a, next(b) == b),
    p(a) ==
    Or(And(next(a) == a, p(a)), And(next(a) == b, p(b))),
    p(b) ==
    Or(And(next(b) == a, p(a)), And(next(b) == b, p(b))),
    And(Or(p(a),
           Not(Or(And(next(a) == a,
                      Or(_6lvl_p(a) <= _6lvl_p(a), p(a))),
                  And(next(a) == b,
                      Or(_6lvl_p(a) <= _6lvl_p(b), p(b)))))),
        Or(p(b),
           Not(Or(And(next(b) == a,
                      Or(_6lvl_p(b) <= _6lvl_p(a), p(a))),
                  And(next(b) == b,
                      Or(_6lvl_p(b) <= _6lvl_p(b), p(b))))))),
    And(Or(Not(p(a)),
           Or(And(next(a) == a,
                  And(_6lvl_p(a) >= _6lvl_p(a), p(a))),
              And(next(a) == b,
                  And(_6lvl_p(a) >= _6lvl_p(b), p(b))))),
        Or(Not(p(b)),
           Or(And(next(b) == a,
                  And(_6lvl_p(b) >= _6lvl_p(a), p(a))),
              And(next(b) == b,
                  And(_6lvl_p(b) >= _6lvl_p(b), p(b)))))))

Model 1
==========
next := {a -> a, b -> b}.
p := {a, b}.


More models may be available.  Change the max argument to see them.
