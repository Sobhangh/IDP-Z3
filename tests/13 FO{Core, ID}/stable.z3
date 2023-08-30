And(Q == Not(P),
    P == Not(Q),
    Or(Not(Not(Q)), P),
    Or(Not(P), Not(Q)),
    Or(Not(Not(P)), Q),
    Or(Not(Q), Not(P)))

Model 1
==========
P := true.
Q := false.


Model 2
==========
P := false.
Q := true.


No more models.
