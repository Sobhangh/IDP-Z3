No more consequences.
And(Or(Not(p), Or(Color == blue, Color == red)),
    Or(Color == red, Color == blue, Color == green))

Model 1
==========
Color := blue.
p := true.


Model 2
==========
Color := blue.
p := {}.


Model 3
==========
Color := green.
p := {}.


Model 4
==========
Color := red.
p := true.


Model 5
==========
Color := red.
p := {}.


No more models.
