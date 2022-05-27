And(p == pos(1, 1),
    q == p,
    is(pos, p),
    is(pos, q),
    is(pos, position(0)),
    is(pos, position(1)),
    is(pos, position(2)),
    ForAll(c!0,
           And(Or(Not(is(pos, c!0)),
                  (position(0) == c!0) == (c!0 == pos(0, 0))),
               Or(Not(is(pos, c!0)),
                  (position(1) == c!0) == (c!0 == pos(0, 0))),
               Or(Not(is(pos, c!0)),
                  (position(2) == c!0) == (c!0 == pos(0, 0))))))

Model 1
==========
p := pos(1, 1).
q := pos(1, 1).
position := {0->pos(0, 0), 1->pos(0, 0), 2->pos(0, 0)}.


No more models.
