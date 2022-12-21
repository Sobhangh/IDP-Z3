And(prime(1),
    prime(2),
    prime(3),
    6 == total,
    ForAll(c!0,
           prime(c!0) == Or(1 == c!0, 2 == c!0, 3 == c!0)))

Model 1
==========
prime := {1, 2, 3}.
total := 6.


No more models.
