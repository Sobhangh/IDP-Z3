Formula: 
And(Or(Not(has_p), And(p, 3 == c)), Or(Not(p), has_p))
WDF: 
true

Model 1
==========
has_p := false.
p := false.
// c := *.


Model 2
==========
has_p := true.
p := true.
c := 3.


No more models.
