And(p(a),
    Or(next(a) == a, next(a) == b),
    Or(next(b) == a, next(b) == b),
    And(Or(Not(Or(And(next(a) == a,
                      Or(_8lvl_p(a) <= _8lvl_p(a), p(a))),
                  And(next(a) == b,
                      Or(_8lvl_p(a) <= _8lvl_p(b), p(b))))),
           p(a)),
        Or(Not(Or(And(next(b) == a,
                      Or(_8lvl_p(b) <= _8lvl_p(a), p(a))),
                  And(next(b) == b,
                      Or(_8lvl_p(b) <= _8lvl_p(b), p(b))))),
           p(b))),
    And(Or(Not(p(a)),
           Or(And(next(a) == a,
                  And(_8lvl_p(a) >= _8lvl_p(a), p(a))),
              And(next(a) == b,
                  And(_8lvl_p(a) >= _8lvl_p(b), p(b))))),
        Or(Not(p(b)),
           Or(And(next(b) == a,
                  And(_8lvl_p(b) >= _8lvl_p(a), p(a))),
              And(next(b) == b,
                  And(_8lvl_p(b) >= _8lvl_p(b), p(b)))))))

Model 1
==========
next := {a -> a, b -> a}.
p := {a, b}.


More models may be available.  Change the max argument to see them.
